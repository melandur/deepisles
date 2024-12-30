import os

import SimpleITK as sitk
from loguru import logger
from PyQt5 import QtCore

import numpy as np
from src.core.data_manager import DataAnalyzer, DataReader, DataWriter, DataHandler
from src.core.utils import NestedDefaultDict, check_device_space, is_json, load_json
from src.modules.dockers.dockers import Dockers


class Pipeline(QtCore.QThread):
    """Welcome to the core, the heartbeat of the system. A config file based pipeline, which calls for each first order
    dictionary key the corresponding method. Processed in a sequential manner, top down."""

    started = QtCore.pyqtSignal()
    finished = QtCore.pyqtSignal()

    popup_message = QtCore.pyqtSignal(str, str, str)
    error_message = QtCore.pyqtSignal(str, str, str, str, str)

    viewer_synced = QtCore.pyqtSignal(str)
    state_message = QtCore.pyqtSignal(str)
    case_name_message = QtCore.pyqtSignal(str)
    state_index_message = QtCore.pyqtSignal(int)

    def __init__(
        self,
        mw: QtCore.QCoreApplication,
        case_paths: str or dict,
        config_file: str or dict = None,
        data_handler: object or None = None,
    ) -> None:
        super().__init__()
        self.mw = mw  # Keeps the threads alive
        self.case_paths = {}
        self.case_name = None
        self.data_handler = None

        self.alive = True
        self.state = None
        self.state_index = 0
        self.config_file = {}

        self.configure_case_paths(case_paths)
        self.configure_config_file(config_file)
        self.configure_data_handler(data_handler)

        logger.info(f'{self.__class__.__name__} started')

    def configure_case_paths(self, case_paths: str or dict) -> None:
        """Deals with case_paths and config_file as variable or json file"""
        if isinstance(case_paths, str):
            if os.path.isfile(case_paths):
                if is_json(case_paths):
                    self.case_paths = load_json(case_paths)
                    logger.info(f'Load case paths from json file: {case_paths}')
            if os.path.isdir(case_paths):
                self.case_paths = DataAnalyzer()(case_paths)
                logger.info(f'Create case paths file from path: {case_paths}')
        elif isinstance(case_paths, NestedDefaultDict):
            self.case_paths = case_paths
            logger.info(f'Load existing case paths: {case_paths}')
        else:
            logger.warning(f'Case paths is not a directory nor json file: {case_paths}')
            self.case_paths = {}

    def configure_config_file(self, config_file: str or dict) -> None:
        """Deals with case_paths and config_file as variable or json file"""
        if isinstance(config_file, str):
            if os.path.isfile(config_file):
                if is_json(config_file):
                    self.config_file = load_json(config_file)
                    logger.info(f'Load config from json file: {config_file}')
        elif isinstance(config_file, dict):
            self.config_file = config_file
            logger.info(f'Load existing config file: {config_file}')
        else:
            logger.warning(f'No valid config file found: {config_file}')
            self.config_file = {}
            logger.info(f'No valid config file found with input: {config_file}')

    def configure_data_handler(self, data_handler: object or None) -> None:
        """Deals with case_paths and config_file as variable or json file"""
        if data_handler:
            self.data_handler = data_handler
        else:
            self.data_handler = DataHandler()

    @QtCore.pyqtSlot()
    def run(self) -> None:
        """Looping and loading cases, processing each case in sub loop __next__"""
        self.started.emit()
        for self.case_name in self.case_paths.keys():
            logger.info(f'### Processing case: {self.case_name} ###')
            self.data_handler.reset()
            next(self)
        self.finished.emit()
        logger.info(f'{self.__class__.__name__} finished')

    def __next__(self) -> None:
        """Core part of the pipeline, calling all the functions dependent on the config file"""
        export_folder = self.config_file['data_writer']['params']['export_folder']
        self.state_index += 1
        for self.state in self.config_file:
            if self.state == 'file_version' or 'meta_' in self.state:
                continue

            if self.config_file[self.state]['active'] and self.alive:
                if hasattr(self, self.state):
                    capitalized_state = ' '.join([word.capitalize() for word in self.state.split('_')])
                    self.state_message.emit(capitalized_state)
                    self.state_index_message.emit(self.state_index)
                    self.case_name_message.emit(self.case_name.capitalize())

                    method = getattr(self, self.state)
                    try:
                        method()
                    except Warning as warning:
                        self.popup_message.emit(f'{capitalized_state}', 'Information', str(warning))
                        self.error_message.emit(
                            str(self.case_name),
                            str(capitalized_state),
                            str(warning),
                            str(export_folder),
                            'information',
                        )
                        break
                    except Exception as error:
                        self.popup_message.emit(f'{capitalized_state} failed', 'Warning', str(error))
                        self.error_message.emit(
                            str(self.case_name),
                            str(capitalized_state),
                            str(error),
                            str(export_folder),
                            'warning',
                        )
                        break

    def data_reader(self) -> None:
        """Read data"""
        check_device_space()
        DataReader(self.data_handler)(self.case_name, self.case_paths)
        self.data_handler.copy_ephemeral_to_lasting_store(state='native')

    def dockers(self) -> None:
        """Run dockers"""
        mask_path = Dockers(self.data_handler, self.config_file)()
        mask_sitk = sitk.ReadImage(mask_path, sitk.sitkInt8)
        self.data_handler.set_ephemeral_results('seg_mask_atlas_sitk', mask_sitk)
        seg_mask_ndarray = np.fliplr(sitk.GetArrayFromImage(mask_sitk))
        self.data_handler.set_ephemeral_results(key='seg_mask_atlas_ndarray', value=seg_mask_ndarray)
        self.data_handler.copy_ephemeral_input_to_ephemeral_output()
        self.data_handler.copy_ephemeral_to_lasting_store(state=self.state)
        self.viewer_synced.emit(self.state)

    def data_writer(self) -> None:
        """Call data writer"""
        DataWriter(self.data_handler, self.config_file, self.case_name)()
