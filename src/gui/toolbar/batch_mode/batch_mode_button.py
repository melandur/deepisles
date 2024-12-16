# pylint: disable=duplicate-code

from loguru import logger
from PyQt5 import QtWidgets

from src.gui.dialog.dialogs import folder_load_dialog
from src.gui.toolbar.batch_mode.batch_mode import BatchMode


class BatchModeButton:
    def __init__(self, mw, core, mw_viewers_updater, cb_block, cb_unblock):
        self.mw = mw
        self.core = core
        self.mw_viewers_updater = mw_viewers_updater
        self.cb_block = cb_block
        self.cb_unblock = cb_unblock

        self.batch_mode_widget = None
        self.button = QtWidgets.QAction('BatchMode', mw)
        self.button.triggered.connect(self._action)

    def _action(self):
        """Start batch mode"""
        self.cb_block()
        load_check, folder_path = folder_load_dialog(self.core, 'Batch Mode - Select Top Level Folder')
        logger.debug(f'load_check: {load_check}, path: {folder_path}')
        if load_check:
            self.core.path_master.set_last_visited_folder(folder_path)
            self.batch_mode_widget = BatchMode(self.mw, self.core, folder_path, self.cb_unblock)
            self.batch_mode_widget.show()
        else:
            self.cb_unblock()
