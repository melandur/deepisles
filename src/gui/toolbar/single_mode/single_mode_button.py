# pylint: disable=duplicate-code

from PyQt5 import QtWidgets
from loguru import logger

from src.gui.toolbar.single_mode.single_mode import SingleMode
from src.core.pipeline import Pipeline
from src.gui.dialog.dialogs import pop_up_window


class SingleModeButton:

    def __init__(self, mw, core, mw_viewers_updater, cb_block, cb_unblock):
        self.mw = mw
        self.core = core
        self.data_handler = core.data_handler
        self.mw_viewers_updater = mw_viewers_updater
        self.cb_block = cb_block
        self.cb_unblock = cb_unblock
        self.button = QtWidgets.QAction('SingleMode', mw)
        self.button.triggered.connect(self._action)
        self.s_m = None

    def _action(self):
        """Start batch mode"""
        self.cb_block()
        self.run_single_mode()

    def run_single_mode(self):
        """Start batch mode"""
        logger.info('Run single mode')
        config_file = self.core.config_file_handler.get_conf_dict()

        self.pipeline = Pipeline(self, self.core.folder_analyzer.case_paths, config_file, self.data_handler)
        self.pipeline.started.connect(self.start_condition)
        self.pipeline.state_message.connect(self.mw.mw_statusbar.message.setText)
        self.pipeline.viewer_synced.connect(self.sync_viewer)
        self.pipeline.popup_message.connect(pop_up_window)
        self.pipeline.finished.connect(self.finished)
        self.pipeline.start()

    def start_condition(self):
        self.mw.mw_statusbar.start_waiting()

    def finished(self):
        self.cb_unblock()
        self.mw.mw_statusbar.stop_waiting()
        self.mw.mw_statusbar.message.setText('')

    def sync_viewer(self, state):
        self.core.sync_viewers_stats.sync(state)
        self.mw_viewers_updater.refresh_viewers()
