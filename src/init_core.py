from loguru import logger
from PyQt5 import QtCore

from src.core.configs.config_file_handler import ConfigFileHandler
from src.core.data_manager import DataAnalyzer, DataHandler, DataReader
from src.core.path_master import PathMaster
from src.core.user import UserSpecsDetector
from src.gui.viewers import InitViewerStats, MetaDataUpdater, SyncViewerStats


class InitCore:
    """Initializes core classes before the gui"""

    def __init__(self, app: QtCore.QCoreApplication):
        self.app = app
        logger.info('Init Backend')

        self.path_master = PathMaster()

        self.data_handler = DataHandler()
        self.data_reader = DataReader(self.data_handler)

        self.config_file_handler = ConfigFileHandler()
        self.user_specifications = UserSpecsDetector(self.app)
        self.folder_analyzer = DataAnalyzer()

        self.viewer_stats = InitViewerStats(self.app, self.path_master, self.config_file_handler)
        self.meta_data_updater = MetaDataUpdater(self.data_handler, self.viewer_stats)
        self.sync_viewers_stats = SyncViewerStats(self.data_handler, self.viewer_stats, self.meta_data_updater)
