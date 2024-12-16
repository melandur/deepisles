import os

from loguru import logger

from src.core.utils import create_folder, dump_json, load_json
from src.path_library import (
    LAST_VISITED_FOLDER_JSON,
    STORAGE_BASE_PATH,
    USER_SETTINGS_PATH,
)


class PathMaster:
    """Creates storage folder and keeps track of the last visited folder"""

    def __init__(self) -> None:
        logger.info('Init Path Master')
        folders = [STORAGE_BASE_PATH, USER_SETTINGS_PATH]

        for folder in folders:
            create_folder(folder)

        self.last_visited_folder_path = self._load_last_visited_folder_path()

    @staticmethod
    @logger.catch
    def _load_last_visited_folder_path() -> str:
        """Loads last visited folder path from json file from storage folder, if file is missing creates empty json"""
        last_visited_storage_path = os.path.join(USER_SETTINGS_PATH, LAST_VISITED_FOLDER_JSON)
        if os.path.isfile(last_visited_storage_path):
            user_data = load_json(last_visited_storage_path)
            init_folder_path = user_data
        else:
            init_folder_path = os.path.join(os.path.expanduser('~'), 'Desktop')
            dump_json(data=init_folder_path, path=last_visited_storage_path)
        return init_folder_path

    @logger.catch()
    def get_last_visited_folder(self) -> str:
        """Returns last visited folder, by default the Desktop when variable is empty"""
        logger.debug(f'get last visited folder: {self.last_visited_folder_path}')
        if not os.path.isdir(self.last_visited_folder_path):
            self.last_visited_folder_path = os.path.join(os.path.expanduser('~'), 'Desktop')
        return self.last_visited_folder_path

    @logger.catch()
    def set_last_visited_folder(self, path: str) -> None:
        """Checks for file and folder paths stores only the folder path"""
        if isinstance(path, str):
            if os.path.isdir(path):
                self.last_visited_folder_path = path
            else:
                head, _ = os.path.split(path)
                self.last_visited_folder_path = head
            self.save()
            logger.debug(f'set last visited folder: {self.last_visited_folder_path}')

    @logger.catch()
    def save(self) -> None:
        """Saves dictionary to storage folder"""
        dump_json(data=self.last_visited_folder_path, path=os.path.join(USER_SETTINGS_PATH, LAST_VISITED_FOLDER_JSON))
