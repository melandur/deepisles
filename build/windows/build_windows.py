import os
import shutil
import time
from subprocess import call

from loguru import logger
from nsis_file_system import create_nsis_installer_file

from src.core.utils import copytree
from src.path_library import APP_ICON, BUILD_VERSION, PROJECT_BASE_PATH


class WindowsBuild:
    def __init__(self):
        """This depends on the user, may need some path adaption"""
        self.clean_simple_itk_file = os.path.join(os.path.dirname(os.getcwd()), 'SimpleITK.clean_txt')
        self.src_path = os.path.join(os.path.dirname(os.path.dirname(os.getcwd())), 'main.py')
        self.build_folder_path = os.path.join(
            os.path.normpath(os.path.expanduser("~/Downloads")), 'deepISLES_100'
        )
        self.main_dist_path = os.path.join(self.build_folder_path, 'main.dist')
        self.user_env_path = r'C:\Users\melandur\miniconda3\envs\deepisles\Lib\site-packages'

        assert os.path.isfile(self.src_path), f'No valid src main.py file -> {self.src_path}'
        assert os.path.isdir(self.user_env_path), f'No valid user env path folder -> {self.user_env_path}'
        assert os.path.isdir(self.user_env_path) is True, 'Set correct user_env_path'

    def __call__(self):
        """Here we build"""
        start_clock = time.time()
        self.clean_build_folder()
        self.clean_simple_itk_wrapper()
        self.compile()
        self.static_file_copy()
        self.create_compiled_folder()
        self.create_nsis_installer_file()
        logger.info(f'U need that long in min --> {(time.time() - start_clock) / 60}')

    def clean_build_folder(self):
        """Removes already existing data for a clean start"""
        if os.path.isdir(self.build_folder_path):
            shutil.rmtree(self.build_folder_path)
            os.makedirs(self.build_folder_path, exist_ok=True)
        os.makedirs(self.build_folder_path, exist_ok=True)

    def clean_simple_itk_wrapper(self):
        """Avoid bloat and never ending optimization loops by cleaning out the unused wrapper Classes/Methods"""
        sitk_folder = os.path.join(self.user_env_path, 'SimpleITK')
        original_wrapper_file = os.path.join(sitk_folder, 'SimpleITK.py')
        if not os.path.isfile(os.path.join(sitk_folder, 'SimpleITK_original.txt')):
            os.rename(original_wrapper_file, os.path.join(sitk_folder, 'SimpleITK_original.txt'))
            shutil.copyfile(self.clean_simple_itk_file, original_wrapper_file)

    def compile(self):
        """With nuitka from python to C"""
        call(
            'python -m nuitka '
            '--show-scons '
            '--standalone '
            '--show-progress '
            '--follow-imports '
            f'--windows-icon-from-ico={APP_ICON} '
            '--windows-disable-console '
            f'--output-dir={self.build_folder_path} '
            '--mingw64 '
            f'{self.src_path}',
            shell=True,
        )

    def static_file_copy(self):
        """Copies static gui related stuff to the build folder"""
        os.makedirs(self.main_dist_path, exist_ok=True)
        os.rename(os.path.join(self.main_dist_path, 'main.exe'), os.path.join(self.main_dist_path, 'DeepISLES.exe'))
        shutil.copyfile(
            os.path.join(PROJECT_BASE_PATH, 'resrc', 'gui', 'icons', 'deepISLES.ico'),
            os.path.join(self.main_dist_path, 'deepISLES.ico'),
        )
        os.makedirs(os.path.join(self.main_dist_path, 'resrc', 'gui'), exist_ok=True)
        copytree(os.path.join(PROJECT_BASE_PATH, 'resrc', 'gui'), os.path.join(self.main_dist_path, 'resrc', 'gui'))

    def create_compiled_folder(self):
        """Copied to bin folder, which allows updating the software when installed in program files"""
        os.makedirs(os.path.join(self.build_folder_path, 'compiled', 'bin'), exist_ok=True)
        copytree(os.path.join(self.main_dist_path), os.path.join(self.build_folder_path, 'compiled', 'bin'))

    def create_nsis_installer_file(self):
        """Creates nsis installer file from compiled folder, which is used to create a windows installer .exe"""
        create_nsis_installer_file(os.path.join(self.build_folder_path, 'compiled'), BUILD_VERSION)


if __name__ == '__main__':
    wb = WindowsBuild()
    wb()
