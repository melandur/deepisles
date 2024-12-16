from collections import OrderedDict

# Description, Options, Default
CONFIG_FILE_EXPLAINER = OrderedDict(
    {
        'data_reader': {
            'active': True,
            'params': {
                'import_name_tag_dwi': [
                    'Dwi sequence import tags for non dicom images\n(use only lower case tags)',
                    'extend depending on your naming structure',
                    "'dwi.,-dwi, _dwi",
                ],
                'import_name_tag_adc': [
                    'Adc sequence import tags for non dicom images\n(use only lower case tags)',
                    'extend depending on your naming structure',
                    "'adc., -adc., _adc.'",
                ],
                'import_name_tag_flair': [
                    'Flair sequence import tags for non dicom images\n(use only lower case tags)',
                    'extend depending on your naming structure',
                    "'flair.', 'flair_', 'flair-'",
                ],
                'dicom_folder_tag_dwi': [
                    'Dwi search tag of mri dicom sequence folder\n(use only lower case tags)',
                    'extend depending on your naming structure',
                    "'dwi'",
                ],
                'dicom_folder_tag_adc': [
                    'Adc search tag of mri dicom sequence folder\n(use only lower case tags)',
                    'extend depending on your naming structure',
                    "'adc'",
                ],
                'dicom_folder_tag_flair': [
                    'Flair search tag of mri dicom sequence folder\n(use only lower case tags)',
                    'extend depending on your naming structure',
                    "'flair', 'fla'",
                ],
            },
        },
        'dockers': {
            'active': True,
            'image': ['Docker image', 'Docker hub image path', 'isleschallenge/deepisles:1.0'],
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
                'export_folder': [
                    'The location where results get stored.',
                    'Check that your path has read/write access\nand avoid cloud storage when possible.',
                    'Downloads/DeepBraTumIA_export',
                ],
                'export_file_extension': [
                    'Defines the output file type',
                    '.nii, .nii.gz, .mha, .mhd, .hdr, .img, .img.gz, .nrrd, .nhdr, .vtk',
                    '.nii.gz',
                ],
            },
        },
        'meta_gui': {
            'show_intro_widget': ['Show intro widget on startup', '', True],
            'show_metadata_viewer': ['Show metadata viewer by default', '', True],
            'online_mode': ['Enable online mode', 'Disable in case you had to install the offline models', True],
        },
    }
)