from PyQt5 import QtCore, QtWidgets

from src.gui.toolbar.batch_mode.batch_mode_button import BatchModeButton
from src.gui.toolbar.single_mode.single_mode_button import SingleModeButton


class Toolbar(QtWidgets.QMainWindow):
    """Toolbar interface, which holds the buttons for single mode"""

    def __init__(self, mw, core, mw_viewers_updater):
        super().__init__()
        self.mw = mw
        self.toolbar = QtWidgets.QToolBar()
        self.toolbar.setMovable(False)
        self.toolbar.setContextMenuPolicy(QtCore.Qt.PreventContextMenu)
        mw.addToolBar(self.toolbar)

        self.single_mode_button = SingleModeButton(mw, core, mw_viewers_updater, self.block, self.unblock)
        self.toolbar.addAction(self.single_mode_button.button)

        self.batch_mode_button = BatchModeButton(mw, core, mw_viewers_updater, self.block, self.unblock)
        self.toolbar.addAction(self.batch_mode_button.button)

    def block(self):
        self.single_mode_button.button.setEnabled(False)
        self.batch_mode_button.button.setEnabled(False)
        self.mw.mw_menu.open_files_button.setEnabled(False)

    def unblock(self):
        self.single_mode_button.button.setEnabled(True)
        self.batch_mode_button.button.setEnabled(True)
        self.mw.mw_menu.open_files_button.setEnabled(True)

    def hide(self):
        """Hide toolbar"""
        self.toolbar.hide()

    def show(self):
        """Show toolbar"""
        self.toolbar.show()

    def disable(self):
        """Disable toolbar"""
        self.toolbar.setDisabled(True)

    def enable(self):
        """Enable toolbar"""
        self.toolbar.setEnabled(True)
