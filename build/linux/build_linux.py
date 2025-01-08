import os
import shutil
import time
from subprocess import call

from loguru import logger

from src.core.utils import copytree
from src.path_library import BUILD_VERSION, PROJECT_BASE_PATH, APP_ICON


class LinuxBuild:
    """Common Errors
    I:   Clean / remove not needed SimpleITK classes/methods like example in folder SimpleITK cleaned
    II:  Numpy version
    III: class RegexFlag(enum.IntFlag): AttributeError: module 'enum' has no attribute 'IntFlag' --> pip uninstall -y enum34

    Using older gcc version to enhance backwards compatibility, need to test the lowest version that works!
    Linux install sudo apt install gcc-7 g++-7

    sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-7 7
    sudo update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-7 7

    gcc --version
    g++ --version

    build deb file:
        adjust version number for name and Debian/control
        cd to deepISLES_xxx_64bit folder and console dpkg-deb --build deepISLES_xxx_64bit
    """

    def __init__(self):
        """This depends on the user, may need some path adaption"""
        self.clean_simple_itk_file = os.path.join(os.path.dirname(os.getcwd()), 'SimpleITK.clean_txt')
        self.src_path = os.path.join(os.path.dirname(os.path.dirname(os.getcwd())), 'main.py')
        self.build_folder_path = os.path.join(
            os.path.normpath(os.path.expanduser('~/Downloads')), f'DeepISLES_{BUILD_VERSION.replace(".", "")}'
        )
        self.main_dist_path = os.path.join(self.build_folder_path, 'main.dist')
        self.user_env_path = os.path.join(
            os.path.expanduser('~'), 'miniconda3', 'envs', 'deepisles', 'lib', 'python3.12', 'site-packages'
        )

        assert os.path.isfile(self.src_path), f'No valid src main.py file -> {self.src_path}'
        assert os.path.isdir(self.user_env_path), f'No valid user env path folder -> {self.user_env_path}'

    def __call__(self):
        """Here we build"""
        start_clock = time.time()
        self.clean_simple_itk_wrapper()
        self.clean_build_folder()
        self.compile()
        self.static_file_copy()
        logger.info(f'U need that long in min --> {(time.time() - start_clock) / 60}')

    def clean_simple_itk_wrapper(self):
        """Avoid bloat and never ending optimization loops by cleaning out the unused wrapper Classes/Methods"""
        sitk_folder = os.path.join(self.user_env_path, 'SimpleITK')
        original_wrapper_file = os.path.join(sitk_folder, 'SimpleITK.py')
        if not os.path.isfile(os.path.join(sitk_folder, 'SimpleITK_original.txt')):
            os.rename(original_wrapper_file, os.path.join(sitk_folder, 'SimpleITK_original.txt'))
            shutil.copyfile(self.clean_simple_itk_file, original_wrapper_file)

    def clean_build_folder(self):
        """Removes already existing data for a clean start"""
        if os.path.isdir(self.build_folder_path):
            shutil.rmtree(self.build_folder_path)
        os.makedirs(self.build_folder_path, exist_ok=True)

    def compile(self):
        """With nuitka from python to C"""
        call(
            'python -m nuitka '
            '--show-scons '
            '--standalone '
            '--show-progress '
            '--follow-imports '
            f'--linux-onefile-icon={APP_ICON} '
            f'--output-dir={self.build_folder_path} '
            f'{self.src_path}',
            shell=True,
        )

    def static_file_copy(self):
        """Copies static gui related stuff to the build folder"""
        os.makedirs(self.main_dist_path, exist_ok=True)
        shutil.copyfile(
            os.path.join(PROJECT_BASE_PATH, 'resrc', 'gui', 'icons', 'deepISLES.ico'),
            os.path.join(self.main_dist_path, 'deepISLES.ico'),
        )
        os.makedirs(os.path.join(self.main_dist_path, 'resrc', 'gui'), exist_ok=True)
        copytree(os.path.join(PROJECT_BASE_PATH, 'resrc', 'gui'), os.path.join(self.main_dist_path, 'resrc', 'gui'))
        logger.warning('Copy merge PyQt5 an to build folder manually, not overwriting existing files')


if __name__ == '__main__':
    lb = LinuxBuild()
    lb()
