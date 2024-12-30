import os
import sys

# Defines the name and activated features of the software
BUILD_VERSION = '1.0.0'

PROJECT_BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

RESRC_BASE_PATH = os.path.join(PROJECT_BASE_PATH, 'resrc')
ICONS_BASE_PATH = os.path.join(RESRC_BASE_PATH, 'gui', 'icons')
USER_SETTINGS_PATH = os.path.join(RESRC_BASE_PATH, 'user_settings')
STORAGE_BASE_PATH = RESRC_BASE_PATH

LAST_VISITED_FOLDER_JSON = 'last_visited_folder.json'
USER_STORAGE_SETTINGS_JSON = 'user_settings.json'
USER_SPECIFICATION = 'user_specifications.json'
CONFIG_FILE_JSON = 'config_file.json'

DEFAULT_EXPORT_FOLDER = os.path.join(os.path.expanduser('~'), 'Downloads', 'DeepIsles_export')