import os

from loguru import logger

from src.core.configs.config_file_handler import ConfigFileHandler
from src.core.configs.static_params import (
    SUPPORTED_DICOM_FILE_TYPES,
    SUPPORTED_IMAGE_FILE_TYPES,
    USED_MODALITY_NAMES,
)
from src.core.utils import NestedDefaultDict, dump_json


class DataAnalyzer(ConfigFileHandler):
    """Analyzes and maps recursively the folder structure"""

    def __init__(self, **kwargs) -> None:
        super().__init__()
        self._shared_state.update(kwargs)
        self.case_paths = None
        self.export_path = None
        self.search_dicom = True

    def append_to_store(
        self,
        root: str,
        file: str,
        case_name: str,
        sequence_type: str,
        path_to_file: bool = True,
    ) -> None:
        """Append case stare with found sequence path"""
        if path_to_file:
            path = os.path.join(root, file)
            if not os.path.isfile(path):
                path = None
        else:
            path = file
            if not os.path.isdir(path):
                path = None
        self.case_paths[case_name][sequence_type] = path

    def __call__(self, src: str, export_path: str or None = None) -> None or str:
        """Start the search"""
        logger.info(f'Run {self.__class__.__name__}')
        self.case_paths = NestedDefaultDict()
        self.export_path = export_path

        if os.path.isfile(src):
            root = os.path.dirname(src)
            file = os.path.basename(src)
            self.check_for_img_or_dicom(root, file)
        elif os.path.isdir(src):
            for root, _, files in os.walk(src):
                self.search_dicom = True
                for file in files:
                    if self.search_dicom:
                        self.check_for_img_or_dicom(root, file)

        if self.export_path:
            dump_json(self.case_paths, os.path.join(self.export_path, 'case_paths.json'))
            return None

        return self.case_paths

    def check_for_img_or_dicom(self, root: str, file: str) -> None:
        """We divide between dicom and medical images like nifti, since they come with different folder structures"""
        if self.check_file_type(file) and self.check_mri_tag(file):  # Checking for non dicom
            sequence_type = self.get_mri_tag(file)
            if sequence_type:
                case_name = os.path.basename(root)
                if self.check_dicom_folder_tag(case_name):
                    case_name = os.path.basename(os.path.dirname(root))
                self.append_to_store(root, file, case_name, sequence_type, path_to_file=True)

        folder_name = os.path.basename(root)
        if self.check_dicom_type(file) and self.check_dicom_folder_tag(folder_name):  # Checking for dicom
            sequence_type = self.get_dicom_folder_tag(os.path.basename(root))
            if sequence_type:
                self.search_dicom = False
                case_name = os.path.basename(os.path.dirname(root))
                self.append_to_store(root, root, case_name, sequence_type, path_to_file=False)

    @staticmethod
    @logger.catch()
    def check_dicom_type(file_name: str) -> bool:
        """Returns True if non dicom file type is supported"""
        state = False
        if [x.lower() for x in SUPPORTED_DICOM_FILE_TYPES if x in file_name.lower()]:
            state = True
        logger.trace(f'Check file type: {file_name}, {state}')
        return state

    @staticmethod
    @logger.catch()
    def check_file_type(file_name: str) -> bool:
        """Returns True if non dicom file type is supported"""
        state = False
        if [x.lower() for x in SUPPORTED_IMAGE_FILE_TYPES if x in file_name.lower()]:
            state = True
        logger.trace(f'Check file type: {file_name}, {state}')
        return state

    @logger.catch()
    def get_file_type(self, file_name: str) -> str:
        """Returns non-dicom file type"""
        search_tags = self.get_conf('data_reader', 'params', 'import_img_file_type')
        file_type = [x.lower() for x in search_tags if x in file_name.lower()]
        if len(file_type) == 1:
            file_type = file_type[0]
        else:
            logger.debug(f'file name: {file_type}')
        logger.trace(f'Get file type: {file_name} supported types: {search_tags} found type: {file_type}')
        return file_type

    @logger.catch()
    def check_mri_tag(self, file_name: str) -> bool:
        """Returns True if mri tag is supported"""
        state = False
        for mri_tag in USED_MODALITY_NAMES:
            search_tags = self.get_conf('data_reader', 'params', f'import_name_tag_{mri_tag}')
            if search_tags:
                if [x.lower() for x in search_tags if x in file_name.lower()]:
                    state = True
                logger.trace(f'Check mri tags: {file_name}, {mri_tag}, {state}')
        return state

    @logger.catch()
    def get_mri_tag(self, file_name: str) -> str:
        """Returns found mri tag"""
        store_tag = None
        for mri_tag in USED_MODALITY_NAMES:
            search_tags = self.get_conf('data_reader', 'params', f'import_name_tag_{mri_tag}')
            if search_tags:
                if [x.lower() for x in search_tags if x in file_name.lower()]:
                    store_tag = mri_tag
                    logger.trace(f'Get mri tag: {file_name} supported types: {search_tags} found type: {store_tag}')
        return store_tag

    @logger.catch()
    def check_dicom_folder_tag(self, folder_name: str) -> bool:
        """Returns True if mri tag is supported"""
        state = False
        for mri_tag in USED_MODALITY_NAMES:
            search_tags = self.get_conf('data_reader', 'params', f'dicom_folder_tag_{mri_tag}')
            if search_tags:
                if [x.lower() for x in search_tags if x in folder_name.lower()]:
                    state = True
                logger.trace(f'Check mri tags: {folder_name}, {mri_tag}, {state}')
        return state

    @logger.catch()
    def get_dicom_folder_tag(self, file_name: str) -> str:
        """Returns found mri tag"""
        store_tag = None
        for mri_tag in USED_MODALITY_NAMES:
            search_tags = self.get_conf('data_reader', 'params', f'dicom_folder_tag_{mri_tag}')
            if search_tags:
                if [x.lower() for x in search_tags if x in file_name.lower()]:
                    store_tag = mri_tag
                    logger.trace(f'Get mri tag: {file_name} supported types: {search_tags} found type: {store_tag}')
        return store_tag

    def reset(self):
        """Reset case paths"""
        self.case_paths = None
