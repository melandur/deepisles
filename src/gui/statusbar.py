import os

from PyQt5 import QtGui, QtWidgets

from src.path_library import ICONS_BASE_PATH


class Statusbar(QtWidgets.QMainWindow):
    """Manages status bar at the bottom with the textfield left and the waiting bar on the right side"""

    def __init__(self, mw):
        super().__init__()
        self.mw = mw

        self.progress_init = 0
        self.progress_state = 0

        self.status_bar = self.mw.statusBar()  # Message bottom left
        self.message = QtWidgets.QLabel()
        self.status_bar.addWidget(self.message)

        self.waiting_bar_holder = QtWidgets.QLabel()  # Waiting bar bottom right
        self.waiting_bar = QtGui.QMovie(os.path.join(ICONS_BASE_PATH, 'waiting_bar.gif'))
        self.waiting_bar_holder.setMovie(self.waiting_bar)
        self.waiting_bar_holder.hide()
        self.waiting_bar.stop()
        self.status_bar.addPermanentWidget(self.waiting_bar_holder)

    def start_waiting(self):
        """Shows and starts waiting bar"""
        self.waiting_bar_holder.show()
        self.waiting_bar.start()

    def stop_waiting(self):
        """Hides and stops waiting bar"""
        self.waiting_bar_holder.hide()
        self.waiting_bar.stop()
