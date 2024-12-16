# pylint: disable=duplicate-code

from loguru import logger
from PyQt5 import QtWidgets

from src.core.pipeline import Pipeline
from src.gui.dialog.dialogs import pop_up_window



class SingleMode(QtWidgets.QWidget):
    """Search in folder for cases and perform registration, skull-stripping, segmentation on complete cases"""

    def __init__(self, mw, core, case_paths, mw_viewers_updater, cb_unblock):
        super().__init__()
        self.mw = mw
        self.core = core
        self.case_paths = case_paths
        self.data_handler = core.data_handler
        self.mw_viewers_updater = mw_viewers_updater
        self.cb_unblock = cb_unblock

        self.pipeline = None
        self.hint_text = None
        self.progress_tot = None

        self.button_run = None
        self.button_stop = None


        logger.info(f'Init {self.__class__.__name__}')

        self.run_single_mode()


    def run_single_mode(self):
        """Start batch mode"""
        logger.info('Run single mode')
        config_file = self.core.config_file_handler.get_conf_dict()

        # Connect and start pipeline
        self.pipeline = Pipeline(self, self.case_paths, config_file, self.data_handler)
        self.pipeline.started.connect(self.start_condition)
        self.pipeline.state_message.connect(self.mw.mw_statusbar.message.setText)
        self.pipeline.viewer_synced.connect(self.sync_viewer)
        self.pipeline.popup_message.connect(pop_up_window)
        self.pipeline.finished.connect(self.finished)
        self.pipeline.start()
        self.hide()

    def start_condition(self):
        self.mw.mw_statusbar.start_waiting()

    def finished(self):
        self.cb_unblock()
        self.mw.mw_statusbar.stop_waiting()
        self.mw.mw_statusbar.message.setText('')
        self.close()

    def sync_viewer(self, state):
        self.core.sync_viewers_stats.sync(state)
        self.mw_viewers_updater.refresh_viewers()
