import os
import sys

from PyQt5 import QtCore, QtWidgets

from src.gui import Header, Menu, Statusbar, Toolbar
from src.gui.dialog.intro_widget import IntroWidget
from src.gui.viewers import InitViewers, ViewerUpdater
from src.init_core import InitCore

# https://stackoverflow.com/questions/39247342/pyqt-gui-size-on-high-resolution-screens
if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):  # Handle high resolution displays:
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, app):
        super().__init__()

        self.app = app
        self.core = InitCore(self.app)
        mw_viewers_updater = ViewerUpdater(self, self.core)

        self.mw_header = Header(self, self.core.user_specifications)
        self.mw_statusbar = Statusbar(self)
        self.mw_viewers = InitViewers(self, self.core, mw_viewers_updater)
        self.mw_menu = Menu(self, self.core, mw_viewers_updater)
        self.mw_toolbar = Toolbar(self, self.core, mw_viewers_updater)

        self.intro_widget = None
        if self.core.config_file_handler.get_conf('meta_gui', 'show_intro_widget', optional=True):
            QtCore.QTimer.singleShot(0, self.maybe_show_intro_widget)

    def maybe_show_intro_widget(self):
        """Maybe show intro widget"""
        self.intro_widget = IntroWidget(self, self.core)
        self.intro_widget.show()

    def rebirth(self):
        """This will restart the application"""
        self.close()
        python = sys.executable
        os.execl(python, python, *sys.argv)
