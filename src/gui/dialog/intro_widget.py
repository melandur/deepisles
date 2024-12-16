from PyQt5 import QtCore, QtGui, QtWidgets

from src.path_library import DEFAULT_EXPORT_FOLDER


class IntroWidget(QtWidgets.QWidget):
    """Show intro widget at start up with some brief information"""

    def __init__(self, mw, core):
        super().__init__()
        self.mw = mw
        self.config_file_handler = core.config_file_handler
        self.user_specifications = core.user_specifications
        self.export_folder = core.config_file_handler.get_conf(
            'data_writer', 'params', 'export_folder', optional=DEFAULT_EXPORT_FOLDER
        )

        self.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint, True)
        self.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)
        self.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint, False)
        self.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, False)

        self.activateWindow()

        self.setWindowTitle('Welcome')

        vbox_layout = QtWidgets.QVBoxLayout()
        grid_layout = QtWidgets.QGridLayout()
        vbox_layout.addLayout(grid_layout)

        grid_layout.setAlignment(QtCore.Qt.AlignTop)
        grid_layout.setColumnStretch(1, 17)

        header_1 = QtWidgets.QLabel('Shortcuts Viewers')
        header_1.setStyleSheet("font-weight: bold")
        grid_layout.addWidget(header_1, 1, 1)
        grid_layout.addWidget(QtWidgets.QLabel('Segmentation opacity'), 2, 1)
        grid_layout.addWidget(QtWidgets.QLabel('Shift + Mouse Scroll Wheel'), 2, 2)
        grid_layout.addWidget(QtWidgets.QLabel('Zoom function (Beta)'), 3, 1)
        grid_layout.addWidget(QtWidgets.QLabel('Ctrl + Mouse Scroll Wheel'), 3, 2)
        grid_layout.addWidget(QtWidgets.QLabel(''), 4, 1)

        header_2 = QtWidgets.QLabel('Folders')
        header_2.setStyleSheet("font-weight: bold")
        grid_layout.addWidget(header_2, 5, 1)
        grid_layout.setColumnStretch(5, 2)
        grid_layout.addWidget(QtWidgets.QLabel('Default Export Folder'), 6, 1)
        grid_layout.addWidget(QtWidgets.QLabel(self.export_folder), 6, 2)
        grid_layout.addWidget(QtWidgets.QLabel(''), 8, 1)

        header_3 = QtWidgets.QLabel('Hardware Detection')
        header_3.setStyleSheet("font-weight: bold")
        grid_layout.addWidget(header_3, 9, 1)
        grid_layout.addWidget(QtWidgets.QLabel('GPU'), 10, 1)
        found_gpu = self.user_specifications.get('GPU', None)

        grid_layout.addWidget(QtWidgets.QLabel(found_gpu_name), 10, 2)
        if found_gpu is None:
            if found_gpu is None:
                link = QtWidgets.QLabel(
                    '<a href="http://www.nvidia.com/Download/index.aspx">www.nvidia.com/Download/index.aspx</a>'
                )
                link.setOpenExternalLinks(True)
                grid_layout.addWidget(link, 11, 2)

        grid_layout.addWidget(QtWidgets.QLabel(''), 14, 1)

        label = QtWidgets.QLabel('This is not a medical device, only for research purposes!')
        label.setStyleSheet('background-color: red;' 'color: black;')

        hbox_layout = QtWidgets.QHBoxLayout()
        hbox_layout.addWidget(label)

        hbox_layout.addStretch()
        checkbox = QtWidgets.QCheckBox('Agree')
        checkbox.stateChanged.connect(self.hide_intro_widget)
        hbox_layout.addWidget(checkbox)

        check_button = QtWidgets.QPushButton('Check')
        check_button.clicked.connect(self.close_intro)
        hbox_layout.addWidget(check_button)
        cancel_button = QtWidgets.QPushButton('Cancel')
        cancel_button.clicked.connect(self.cancel)
        hbox_layout.addWidget(cancel_button)

        vbox_layout.addLayout(hbox_layout)
        self.setLayout(vbox_layout)

        self.move(QtWidgets.QDesktopWidget().availableGeometry().center() - self.frameGeometry().center())

    def hide_intro_widget(self, state):
        if state == QtCore.Qt.Checked:
            self.config_file_handler.set_conf('meta_gui', 'show_intro_widget', value=False)
        else:
            self.config_file_handler.set_conf('meta_gui', 'show_intro_widget', value=True)

    def cancel(self):
        self.config_file_handler.set_conf('meta_gui', 'show_intro_widget', value=True)
        self.close()
        self.mw.close()

    def close_intro(self):
        if not self.config_file_handler.get_conf('meta_gui', 'show_intro_widget', optional=False):
            self.close()

    def closeEvent(self, event):
        self.config_file_handler.save_conf()


if __name__ == '__main__':
    import sys

    from src.gui.mainwindow import MainWindow

    app = QtWidgets.QApplication(sys.argv)
    mw = MainWindow(app)
    mw.hide()

    volume = IntroWidget(mw, mw.core)
    volume.show()
    app.exec_()
