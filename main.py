import sys

import PyQt5.sip  # needed by nuitka for building
from PyQt5 import QtWidgets
from loguru import logger

from src.gui.mainwindow import MainWindow
from src.gui.style.style_settings import StyleSheetModifier


if __name__ == '__main__':

    logger.info('Start main')

    # Init app
    app = QtWidgets.QApplication(sys.argv)

    # Load and apply style sheet
    style_sheet = StyleSheetModifier()
    app.setStyleSheet(style_sheet.dark_stylesheet)

    # Init main window
    main_window = MainWindow(app)
    main_window.show()
    sys.exit(app.exec_())
