import copy
import os
import typing as t
from collections import OrderedDict

from loguru import logger

from src.core.utils import dump_json, load_json
from src.path_library import (
    BUILD_VERSION,
    CONFIG_FILE_JSON,
    DEFAULT_EXPORT_FOLDER,
    USER_SETTINGS_PATH,
)

CONFIG_FILE = OrderedDict(
    {
        'file_version': BUILD_VERSION,
        'data_reader': {
            'active': True,
            'params': {
                'import_name_tag_dwi': [
                    'dwi.',
                    '-dwi',
                    '_dwi',
                ],
                'import_name_tag_adc': [
                    'adc.',
                    '-adc.',
                    '_adc.',
                ],
                'import_name_tag_flair': [
                    'flair.',
                    '-flair',
                    '_flair',
                ],
                'dicom_folder_tag_dwi': [
                    'dwi',
                ],
                'dicom_folder_tag_adc': [
                    'adc',
                ],
                'dicom_folder_tag_flair': [
                    'flair',
                    'fla',
                ],
            },
            '_add_sequence': 'system_place_holder',
        },
        'dockers': {
            'active': True,
            'image': 'isleschallenge/deepisles:latest',
            'params': {
                'skull_strip': False,
                'fast': False,
                'parallelize': True,
                'save_team_outputs': False,
                'results_mni': False,
            }


        },
        'data_writer': {
            'active': True,
            'params': {
                'export_folder': DEFAULT_EXPORT_FOLDER,
                'export_file_extension': '.nii.gz',
            }
        },
        'meta_gui': {
            'segmentation_label_color': [
                [0, 0, 0, 0],
                [255, 13, 34, 255],
                [0, 255, 60, 255],
                [0, 60, 255, 255],
                [255, 255, 0, 255],
                [20, 191, 235, 255],
                [158, 211, 154, 255],
                [190, 77, 38, 255],
                [0, 111, 76, 255],
                [55, 40, 51, 255],
                [247, 37, 108, 255],
                [185, 233, 9, 255],
                [50, 207, 218, 255],
                [210, 110, 206, 255],
                [215, 196, 45, 255],
                [251, 187, 168, 255],
                [16, 22, 144, 255],
                [120, 111, 76, 255],
            ],
            'show_intro_widget': True,
            'show_metadata_viewer': True,
        },
    },
)


class ConfigFileHandler:
    """Class for handling the configuration file"""

    _shared_state = {}  # borg pattern

    def __init__(self, default_file_path=os.path.join(USER_SETTINGS_PATH, CONFIG_FILE_JSON), file_path=None) -> None:
        super().__init__()

        self.__dict__ = self._shared_state

        self._template_dict = None
        self._file_path = file_path if file_path is not None else default_file_path
        self._reset_template = CONFIG_FILE

        self.load_conf()
        self.check_version()

    def get_conf(self, *keys: str, optional: t.Any = None) -> t.Any:
        """Nested dictionary getter, max depth of key is (XX, XX, XX, optional return value)"""
        try:
            logger.trace(f'{self.__class__.__name__}, called keys: {keys}')
            count_keys = len(keys)
            if count_keys == 1:
                return self._template_dict[keys[0]]
            if count_keys == 2:
                return self._template_dict[keys[0]][keys[1]]
            if count_keys == 3:
                return self._template_dict[keys[0]][keys[1]][keys[2]]
            logger.warning(f'{self.__class__.__name__}, called keys: {keys}, optional: {optional}')
            return optional
        except:
            return optional

    def set_conf(self, *keys: str, value: t.Any) -> None:
        """Nested dictionary setter, max depth of key is (XX, XX, XX, value)"""
        try:
            logger.debug(f'{self.__class__.__name__}, keys: {keys}')
            count_keys = len(keys)
            if count_keys == 1:
                self._template_dict[keys[0]] = value
            elif count_keys == 2:
                self._template_dict[keys[0]][keys[1]] = value
            elif count_keys == 3:
                self._template_dict[keys[0]][keys[1]][keys[2]] = value
        except KeyError:
            pass

    def remove_conf(self, *keys: str) -> None:
        """Nested dictionary remove, max depth of key is (XX, XX, XX)"""
        try:
            logger.debug(f'{self.__class__.__name__}, keys: {keys}')
            count_keys = len(keys)
            if count_keys == 1:
                del self._template_dict[keys[0]]
            elif count_keys == 2:
                del self._template_dict[keys[0]][keys[1]]
            elif count_keys == 3:
                del self._template_dict[keys[0]][keys[1]][keys[2]]
        except KeyError:
            pass

    @logger.catch
    def check_version(self) -> None:
        """Check current stats dict version, override local dict if version differs"""
        current_stats_version = self._template_dict.get('file_version', False)
        if current_stats_version:
            current_stats_version = list(map(int, current_stats_version.split('.')))
            current_build_version = list(map(int, BUILD_VERSION.split('.')))

            for current_number, latest_number in zip(current_stats_version, current_build_version):
                if current_number != latest_number:
                    logger.warning(f'base dictionary handler reset {self.__class__.__name__}')
                    self.reset_conf()
        else:
            logger.warning(f'base dictionary handler reset {self.__class__.__name__}')
            self.reset_conf()

    @logger.catch
    def load_conf(self) -> None:
        """Loads stored template from storage folder otherwise inits default values"""
        if os.path.isfile(self._file_path):
            self._template_dict = load_json(self._file_path)
            if not self._template_dict:
                self.reset_conf()
        else:
            self.reset_conf()

    @logger.catch
    def save_conf(self) -> None:
        """Saves dictionary to storage folder"""
        dump_json(data=self._template_dict, path=self._file_path)

    @logger.catch
    def reset_conf(self) -> None:
        """Saves dictionary to storage folder"""
        dump_json(data=self._reset_template, path=self._file_path)
        self.load_conf()

    def get_active_modalities(self) -> t.List[str]:
        """Returns a list of active modalities"""
        tags = self._template_dict['data_reader']['params']
        img_modalities = [key.replace('import_name_tag_', '') for key in tags if 'import_name_tag_' in key]
        dicom_modalities = [key.replace('dicom_folder_tag_', '') for key in tags if 'dicom_folder_tag_' in key]
        test_img_modalities = copy.deepcopy(img_modalities)
        if set(test_img_modalities) != set(dicom_modalities):
            self.reset_conf()
            raise Warning(
                'The import and folder tags do not match,'
                'check that each modality has an "import_name_tag_" and "dicom_folder_tag_"'
            )
        return img_modalities

    def get_conf_dict(self) -> dict:
        """Returns the configuration dictionary"""
        return copy.deepcopy(self._template_dict)
