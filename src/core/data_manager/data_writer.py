import os
import typing as t

import SimpleITK as sitk
from loguru import logger

from src.core.utils import dump_json


class DataWriter:
    """Writes data from lasting store to local space"""

    def __init__(self, data_handler: t.Any, config_file: dict, case_name: str) -> None:
        self.data_handler = data_handler
        self.config_file = config_file
        self.case_name = case_name
        self.params = config_file['data_writer']['params']
        self.lasting_store = self.data_handler.get_lasting_store()

    def __call__(self) -> None:
        logger.info(f'Run {self.__class__.__name__}')
        # self._export_config_file()
        # self._export_original()


    def _create_folder_struct(
        self, key: str, folder_name: str, subfolder_name: str, set_file_name: str or None = None
    ) -> (str, str):
        """Creates export folder path for the writer methods. returns the paths and used methods"""
        if set_file_name:
            export_path = os.path.join(
                self.params['export_folder'], self.case_name, folder_name, subfolder_name, set_file_name
            )
        else:
            export_path = os.path.join(self.params['export_folder'], self.case_name, folder_name, subfolder_name)
        os.makedirs(export_path, exist_ok=True)
        modality = key.split('_')[0]
        return export_path, modality

    def _write_image(
        self,
        key: str,
        folder_name: str,
        subfolder_name: str,
        file_name: str or None = None,
        reorient: bool = False,
    ) -> None:
        """Write image data local storage"""
        export_path, modality = self._create_folder_struct(key, folder_name, subfolder_name)
        if file_name is None:
            file_name = f'{self.case_name}_{modality}{self.params["export_file_extension"]}'
        else:
            file_name = f'{self.case_name}_{modality}_{file_name}{self.params["export_file_extension"]}'
        file_path = os.path.join(export_path, file_name)
        logger.trace(f'export {key} -> {file_path}')
        img = self.lasting_store[key]
        if reorient:
            orientation = self.data_handler.get_from_lasting_store(f'{modality}_native_image_orientation')
            img = set_coordinate_orientation(img, orientation)
        sitk.WriteImage(img, file_path)

    def _write_segmentation(
        self,
        key: str,
        folder_name: str,
        subfolder_name: str,
        mask_name: str,
        use_modalities: bool = True,
        reorient: bool = False,
    ) -> None:
        """Write image data local storage"""
        export_path, modality = self._create_folder_struct(key, folder_name, subfolder_name)
        if use_modalities:
            file_name = f'{self.case_name}_{modality}_{mask_name}{self.params["export_file_extension"]}'
        else:
            file_name = f'{self.case_name}_{mask_name}{self.params["export_file_extension"]}'
        file_path = os.path.join(export_path, file_name)
        logger.trace(f'export {key} -> {file_path}')
        img = self.lasting_store[key]
        if reorient:
            orientation = self.data_handler.get_from_lasting_store('t1_native_image_orientation')
            img = set_coordinate_orientation(img, orientation)
        sitk.WriteImage(img, file_path)

    def _write_transformation(self, key: str, folder_name: str, subfolder_name: str) -> None:
        """Write transformation data  to local storage"""
        export_path, modality = self._create_folder_struct(key, folder_name, subfolder_name)
        file_path = os.path.join(export_path, f'{self.case_name}_{modality}.tfm')
        logger.trace(f'export {key} -> {export_path}')
        sitk.WriteTransform(self.lasting_store[key], file_path)

    def _write_json_file(self, key: str, folder_name: str, subfolder_name: str, file_name: str) -> None:
        """Write json file to local storage"""
        export_path, _ = self._create_folder_struct(key, folder_name, subfolder_name)
        file_path = os.path.join(export_path, f'{file_name}.json')
        logger.trace(f'export {key} -> {export_path}')
        dump_json(self.lasting_store[key], file_path)

    def _export_config_file(self) -> None:
        """Export config file"""
        if self.config_file['data_writer']['save_config_file']:  # config file
            configs_path = os.path.join(self.params['export_folder'], self.case_name, 'configs')
            os.makedirs(configs_path, exist_ok=True)
            file_path = os.path.join(configs_path, 'config_file.json')
            logger.trace(f'export config_file -> {file_path}')
            dump_json(self.config_file, file_path)

    def _export_original(self) -> None:
        """Export original images"""
        config = self.config_file['data_writer']
        for key, value in self.lasting_store.items():  # image data
            if isinstance(value, sitk.Image):
                if '_native_' in key and 'brain' not in key and 'seg_mask' not in key and config['save_native_images']:
                    self._write_image(key, 'native', 'original_data', reorient=True)
