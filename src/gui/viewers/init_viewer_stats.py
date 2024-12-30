from loguru import logger

from src.gui.viewers.custom_view import CustomSidePanelQDockWidget
from src.gui.viewers.viewer_stats import ViewerStats


class InitViewerStats:
    def __init__(self, app, path_master, config_file_handler):
        logger.info(f'Init {self.__class__.__name__}')

        self.sse_viewer = ViewerStats(path_master, config_file_handler)

        self.viewer_1 = ViewerStats(path_master, config_file_handler)
        self.viewer_2 = ViewerStats(path_master, config_file_handler)
        self.viewer_3 = ViewerStats(path_master, config_file_handler)
        self.viewer_4 = ViewerStats(path_master, config_file_handler)

        self.left_panel_widget = CustomSidePanelQDockWidget(app)
