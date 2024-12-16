from PyQt5 import QtCore, QtGui, QtWidgets

from src.core.configs.config_file_handler import ConfigFileHandler
from src.gui.menu.preferences.tab_filler import TabFiller


class UserPreferences(QtWidgets.QWidget, ConfigFileHandler):
    """Creates a user interface from the config file"""

    def __init__(self, mw, callback_preferences, **kwargs) -> None:
        super().__init__()
        self._shared_state.update(kwargs)

        self.mw = mw
        self.callback_preferences = callback_preferences
        self.config_file = self.get_conf_dict()
        self.user_specifications = mw.core.user_specifications

        self.setWindowTitle('Preferences')

        self.v_box = QtWidgets.QVBoxLayout(self)
        self.setLayout(self.v_box)

        self.tabs = QtWidgets.QTabWidget(self)

        for key in self.config_file:
            if key in ('file_version', 'quality_agent'):
                continue
            scroll_tab = QtWidgets.QScrollArea()
            scroll_tab.setWidgetResizable(True)
            tab = TabFiller(key, self, self.update_action)
            tab.setObjectName(key)
            tab_name = ' '.join([name_part.capitalize() for name_part in key.split('_')])
            scroll_tab.setWidget(tab)
            self.tabs.addTab(scroll_tab, tab_name)

        self.v_box.addWidget(self.tabs)

        self.h_box = QtWidgets.QHBoxLayout()
        self.h_box.addStretch()

        reset_button = QtWidgets.QPushButton('Reset')
        reset_button.clicked.connect(self.reset_action)
        self.h_box.addWidget(reset_button)

        save_button = QtWidgets.QPushButton('Save')
        save_button.clicked.connect(self.save_action)
        self.h_box.addWidget(save_button)
        self.v_box.addSpacing(10)
        self.v_box.addLayout(self.h_box)

        self.resize(1300, 600)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.move(QtWidgets.QDesktopWidget().availableGeometry().center() - self.frameGeometry().center())

    def reset_action(self) -> None:
        self.reset_conf()
        self.mw.rebirth()
        self.close()

    def save_action(self) -> None:
        self.save_conf()
        self.mw.rebirth()
        self.close()

    def update_action(self):
        self.save_conf()
        self.close()
        self.callback_preferences()
