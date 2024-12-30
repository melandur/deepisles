import os

from copy import deepcopy
from typing import TypeVar
import SimpleITK as sitk

from loguru import logger
import docker

from src.gui.dialog.dialogs import pop_up_window_forced_waiting
from src.path_library import DEFAULT_EXPORT_FOLDER

DataHandler = TypeVar('DataHandler')


class Dockers:

    def __init__(self, data_handler: DataHandler, config_file: dict) -> None:
        super().__init__()
        self.data_handler = data_handler
        self.config_file = config_file['dockers']
        self.tmp_path = None
        self.modalities = self.data_handler.get_active_modalities('ephemeral_sitk')
        self.case_name = self.data_handler.case_name
        self.pop_up = None

        self.is_docker_available()
        self.is_nvidia_docker_available()


    def __call__(self) -> None:
        file_paths = self._ephemeral_to_tmp_local_store()
        self.client = docker.from_env()

        command = ''  # init empty command

        for modality in file_paths:
            command += f'--{modality}_file_name={self.case_name}_{modality}.nii.gz '

        for key, values in self.config_file['params'].items():
            if values:
                command += f'--{key} '

        try:  # Run container
            logger.info(f'Using: {self.config_file["image"]}')

            if self.check_image_exists(self.config_file['image']):
                logger.info('Image locally available')
            else:
                logger.info('Image not locally available, pulling image')
                self.pop_up = pop_up_window_forced_waiting(f'Pulling docker image, this may take a while. '
                                                           f'\nThis is only done once. Alternatively, you can pull the '
                                                           f'image manually using the terminal '
                                                           f'-> docker pull {self.config_file["image"]}')
                self.pop_up.show()
                self.client.images.pull(self.config_file['image'])
                self.pop_up.done(0)

            self.client.containers.run(
                image=f'{self.config_file["image"]}',
                command=command,
                detach=False,
                remove=True,
                volumes={self.tmp_path: {'bind': '/app/data', 'mode': 'rw'}},
                device_requests=[
                    docker.types.DeviceRequest(device_ids=["0"], capabilities=[['gpu']])
                ],

            )

            for key, values in file_paths.items():
                os.remove(values)

            seg_mask_path = os.path.join(self.tmp_path, 'results', 'lesion_msk.nii.gz')

        except Exception as e:
            seg_mask_path = None
            logger.error(f'Container error: {e}')

        return seg_mask_path



    def _write_tmp_image(self, modality: str, export_path: str) -> str:
        """Writes image to local path"""
        case_name = self.data_handler.case_name
        os.makedirs(export_path, exist_ok=True)
        image_data = deepcopy(self.data_handler[f'{modality}_ephemeral_sitk'])
        file_path = os.path.join(export_path, f'{case_name}_{modality}.nii.gz')
        sitk.WriteImage(image_data, file_path)
        return file_path

    def _ephemeral_to_tmp_local_store(self) -> dict:
        """Writes all ephemeral images to local tmp folder"""

        self.tmp_path = os.path.join(DEFAULT_EXPORT_FOLDER, self.case_name)
        os.makedirs(self.tmp_path, exist_ok=True, mode=0o777)

        tmp_image_paths = {}
        for modality in self.modalities:
            if self.data_handler.check_ephemeral_input(modalities=[modality], extensions=['sitk']):
                tmp_image_paths[modality] = self._write_tmp_image(modality=modality, export_path=self.tmp_path)

        for modality in self.modalities:
            if not os.path.isfile(tmp_image_paths[modality]):
                raise FileNotFoundError

        return tmp_image_paths

    @staticmethod
    def is_docker_available():
        try:
            client = docker.from_env()
            client.ping()
            logger.info('Docker available')
        except Exception as e:
            raise Exception(f'Docker not available')


    @staticmethod
    def is_nvidia_docker_available():
        try:
            client = docker.from_env()
            client.containers.run(
                image='ubuntu',
                command='nvidia-smi',
                detach=True,
                remove=True,
                device_requests=[
                    docker.types.DeviceRequest(device_ids=["0"], capabilities=[['gpu']])
                ]
            )
            logger.info('Nvidia docker available')
        except Exception as e:
            raise Exception(f'Nvidia docker not available')

    @staticmethod
    def check_image_exists(image_name):
        client = docker.from_env()
        try:
            client.images.get(image_name)
            return True
        except docker.errors.ImageNotFound:
            return False
