from src.core.configs.config_file_handler import ConfigFileHandler

config_file_handler = ConfigFileHandler()
USED_MODALITY_NAMES = config_file_handler.get_active_modalities()


SUPPORTED_IMAGE_FILE_TYPES = [
    '.nii',
    '.mha',
    '.mhd',
    '.hdr',
    '.img',
    '.nrrd',
    '.nhdr',
    '.vtk',
]
SUPPORTED_DICOM_FILE_TYPES = [
    '.dicom',
    '.dcm',
]
SUPPORTED_EXPORT_FILE_TYPES = [
    '.nii',
    '.nii.gz',
    '.mha',
    '.mhd',
    '.hdr',
    '.img',
    '.img.gz',
    '.nrrd',
    '.nhdr',
    '.vtk',
]
