from PyQt5 import QtCore, QtWidgets

from src.core.configs import CONFIG_FILE_EXPLAINER
from src.core.configs.config_file_handler import CONFIG_FILE
from src.gui.dialog.dialogs import pop_up_window
from src.gui.menu.preferences.helpers import (
    CheckBox,
    LineEditFloat,
    LineEditInt,
    LineEditListOfFloat,
    LineEditListOfInt,
    LineEditListOfStrings,
    LineEditNone,
    LineEditString,
)


class TabFiller(QtWidgets.QWidget):
    """Fill tabs with config file content"""

    def __init__(self, key_1, config_file_handler, rebirth_callback=None):
        super().__init__()
        self.key_1 = key_1
        self.config_file_handler = config_file_handler
        self.rebirth_callback = rebirth_callback
        self.config_file = config_file_handler.get_conf_dict()

        self.h_box = None
        self.label = None
        self.element = None
        self.default_button = None
        self.explain_button = None

        self.v_box = QtWidgets.QVBoxLayout()
        self._loop_over_dict()

    def _get_element(self, value, *args):
        """Returns checkbox or type specific line edit dependent on data type"""
        self.element = None
        if value is None:
            self.element = LineEditNone(self.config_file_handler, args, optional=None)
        elif isinstance(value, bool):
            self.element = CheckBox(self.config_file_handler, args)
        elif isinstance(value, int):
            optional = 'Invalid entry, expected single integer value like 0, 1, 2, 10, etc'
            self.element = LineEditInt(self.config_file_handler, args, optional=optional)
        elif isinstance(value, float):
            optional = 'Invalid entry, expected single float value like 0.0, 0.1, 2.0, 10.0, etc'
            self.element = LineEditFloat(self.config_file_handler, args, optional=optional)
        elif isinstance(value, str):
            optional = "Invalid entry, expected a string like a word or path /home/user/files, etc"
            self.element = LineEditString(self.config_file_handler, args, optional=optional)
        elif isinstance(value, list):
            if len(value) != 0:
                if isinstance(value[0], int):
                    optional = 'Invalid entry, expected coma separated integers like 0, 1, 2, 10, etc'
                    self.element = LineEditListOfInt(self.config_file_handler, args, optional=optional)
                if isinstance(value[0], float):
                    optional = 'Invalid entry, expected coma separated floats like 0.0, 1.0, 2.0, 10.0, etc'
                    self.element = LineEditListOfFloat(self.config_file_handler, args, optional=optional)
                if isinstance(value[0], str):
                    optional = 'Invalid entry, expected a string like a word or path /home/user/files, etc'
                    self.element = LineEditListOfStrings(self.config_file_handler, args, optional=optional)

        if self.element:
            self.element.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
            if len(args) == 2:
                self.element.setObjectName(f'{args[0]}.{args[1]}')
            elif len(args) == 3:
                self.element.setObjectName(f'{args[0]}.{args[1]}.{args[2]}')
            else:
                raise NotImplementedError('Not implemented for more than 3 arguments')

    def check_for_custom_placement(self, *args):
        if args[0] == 'segmentation' and args[2] == 'labels':
            self.label_colors()

        if args[0] == 'data_reader' and args[1] == '_add_sequence':
            self.add_sequence()
            self.remove_sequence()

    def label_colors(self):
        """Add custom elements"""
        self.h_box = QtWidgets.QHBoxLayout()

        spacer = QtWidgets.QLabel()
        spacer.setMinimumWidth(280)

        self.h_box.addWidget(spacer)
        self.h_box.setSpacing(5)

        labels = self.config_file_handler.get_conf('segmentation', 'params', 'labels')
        colors = self.config_file_handler.get_conf('meta_gui', 'segmentation_label_color')
        colors = [f'#{int(color[0]):02x}{int(color[1]):02x}{int(color[2]):02x}' for color in colors]  # to hex

        if len(labels) >= 1:
            label_1 = QtWidgets.QLabel(f'Enhancing Tumor = {labels[0]}')
            label_1.setStyleSheet(f'background-color: {colors[labels[0]]}; color: black')
            self.h_box.addWidget(label_1)
            self.h_box.setSpacing(5)

        if len(labels) >= 2:
            label_2 = QtWidgets.QLabel(f'Necrotic Core = {labels[1]}')
            label_2.setStyleSheet(f'background-color: {colors[labels[1]]}; color: black')
            self.h_box.addWidget(label_2)
            self.h_box.setSpacing(5)

        if len(labels) >= 3:
            label_3 = QtWidgets.QLabel(f'Edema Compartment = {labels[2]}')
            label_3.setStyleSheet(f'background-color: {colors[labels[2]]}; color: black')
            self.h_box.addWidget(label_3)
            self.h_box.setSpacing(5)

        self.h_box.setAlignment(QtCore.Qt.AlignLeft)
        self.v_box.addItem(self.h_box)

    def add_sequence(self):
        """Add new sequence search tags"""
        self.h_box = QtWidgets.QHBoxLayout()

        self.add_sequence_button = QtWidgets.QPushButton('+')
        self.add_sequence_button.clicked.connect(self.add_sequence_to_dict)
        self.add_sequence_button.setMinimumWidth(100)

        self.label = QtWidgets.QLineEdit()
        self.label.setMinimumWidth(175)
        self.label.setPlaceholderText('your_sequence_name')
        self.label.setObjectName('data_reader_sequence_label')

        self.h_box.addWidget(self.add_sequence_button)
        self.h_box.setSpacing(5)
        self.h_box.addWidget(self.label)
        self.h_box.addStretch(1)

        self.v_box.addStretch(1)
        self.v_box.addItem(self.h_box)

    def remove_sequence(self):
        """Add new sequence search tags"""
        self.h_box = QtWidgets.QHBoxLayout()

        self.add_sequence_button = QtWidgets.QPushButton('-')
        self.add_sequence_button.clicked.connect(self.remove_sequence_to_dict)
        self.add_sequence_button.setMinimumWidth(100)

        params = self.config_file_handler.get_conf('data_reader', 'params')
        key_names = [key.replace('dicom_folder_tag_', '') for key in params.keys() if 'dicom_folder_tag_' in key]

        self.combo_box = QtWidgets.QComboBox()
        self.combo_box.addItems(key_names)
        self.combo_box.setObjectName('drop_sequence_label_2')

        self.h_box.addWidget(self.add_sequence_button)
        self.h_box.setSpacing(5)
        self.h_box.addWidget(self.combo_box)
        self.h_box.addStretch(1)

        self.v_box.addItem(self.h_box)

    def add_sequence_to_dict(self):
        """Add new sequence search tags"""
        label = self.findChild(QtWidgets.QLineEdit, 'data_reader_sequence_label')
        label_name = label.text()
        if label_name != '' and 'seg' not in label_name:
            label_name = label_name.replace(' ', '_')
            tag_1 = [f'{label_name}.', f'{label_name}_', f'{label_name}-']
            tag_2 = [f'{label_name}']
            self.config_file_handler.set_conf('data_reader', 'params', f'import_name_tag_{label_name}', value=tag_1)
            self.config_file_handler.set_conf('data_reader', 'params', f'dicom_folder_tag_{label_name}', value=tag_2)
            self.rebirth_callback()

    def remove_sequence_to_dict(self):
        """Add new sequence search tags"""
        label = self.findChild(QtWidgets.QComboBox, 'drop_sequence_label_2')
        label_name = label.currentText()
        self.config_file_handler.remove_conf('data_reader', 'params', f'import_name_tag_{label_name}')
        self.config_file_handler.remove_conf('data_reader', 'params', f'dicom_folder_tag_{label_name}')
        self.rebirth_callback()

    def assign_qt_elements(self, element, *args, spacing=0):
        """Assign a row with name, button or text edit and an info button"""
        if element:
            self.h_box = QtWidgets.QHBoxLayout()
            self.h_box.setObjectName(f"h_box_{'.'.join(args)}")
            label_name = f"{spacing * ' '}{args[-1].replace('_', ' ').capitalize()}"
            self.label = QtWidgets.QLabel(label_name)
            self.label.setObjectName(f"label_{'.'.join(args)}")
            self.label.setMinimumWidth(280)
            self.h_box.addWidget(self.label)
            self.h_box.addWidget(element)

            self.h_box.setSpacing(5)
            self.default_button = QtWidgets.QPushButton()
            self.default_button.setText('default')
            self.default_button.setObjectName('.'.join(args))
            self.default_button.clicked.connect(self.set_default_value_action)
            self.h_box.addWidget(self.default_button)

            self.explain_button = QtWidgets.QPushButton()
            self.explain_button.setText('info')
            self.explain_button.setObjectName('.'.join(args))
            self.explain_button.clicked.connect(self.show_key_info_action)
            self.h_box.addWidget(self.explain_button)

    def _loop_over_dict(self):
        """Loop trough sub dictionary and set qt elements dependent on data type"""
        for key_2 in self.config_file[self.key_1]:
            if key_2 == 'active':
                continue

            if key_2 in ['features']:
                continue

            if key_2.startswith('_'):
                self.check_for_custom_placement(self.key_1, key_2, None)
                continue

            if isinstance(self.config_file[self.key_1][key_2], dict):
                label_name = key_2.replace('_', ' ').capitalize()
                label = QtWidgets.QLabel(label_name)
                self.v_box.addWidget(label)

                for key_3 in self.config_file[self.key_1][key_2]:
                    value = self.config_file[self.key_1][key_2][key_3]
                    self._get_element(value, self.key_1, key_2, key_3)
                    if self.element:
                        self.assign_qt_elements(self.element, self.key_1, key_2, key_3, spacing=7)
                        self.v_box.setAlignment(QtCore.Qt.AlignTop)
                        self.v_box.addItem(self.h_box)
                        self.check_for_custom_placement(self.key_1, key_2, key_3)
                self.v_box.addSpacing(20)
            else:
                value = self.config_file[self.key_1][key_2]
                self._get_element(value, self.key_1, key_2)
                if self.element:
                    self.assign_qt_elements(self.element, self.key_1, key_2, spacing=0)
                    self.v_box.setAlignment(QtCore.Qt.AlignTop)
                    self.v_box.addItem(self.h_box)
        self.setLayout(self.v_box)

    def set_default_value_action(self):
        """Set the menu field back to the default value"""
        object_name = self.sender().objectName()
        keys = object_name.split('.')
        count_keys = len(keys)

        try:
            if count_keys == 1:
                default_state = CONFIG_FILE[keys[0]]
                self.config_file_handler.set_conf(keys[0], value=default_state)
            elif count_keys == 2:
                default_state = CONFIG_FILE[keys[0]][keys[1]]
                self.config_file_handler.set_conf(keys[0], keys[1], value=default_state)
            elif count_keys == 3:
                default_state = CONFIG_FILE[keys[0]][keys[1]][keys[2]]
                if default_state is None:
                    default_state = str(default_state)
                self.config_file_handler.set_conf(keys[0], keys[1], keys[2], value=default_state)
            elif count_keys == 4:
                default_state = CONFIG_FILE[keys[0]][keys[1]][keys[2]][keys[3]]
                self.config_file_handler.set_conf(keys[0], keys[1], keys[2], keys[3], value=default_state)
            else:
                default_state = None

            self.config_file_handler.save_conf()
            self.set_element_default(object_name, default_state)
        except KeyError:
            pass

    def set_element_default(self, object_name, default_state):
        """Update elements by object name with default state"""
        if default_state is not None:
            element_line_edit = self.findChild(QtWidgets.QLineEdit, object_name)
            if element_line_edit:
                element_line_edit.load_state(default_state)

            element_check_box = self.findChild(QtWidgets.QCheckBox, object_name)
            if element_check_box:
                element_check_box.load_state(default_state)

    def show_key_info_action(self):
        """Create info button with to show the user some basic stuff about the parameter"""
        args = self.sender().objectName().split('.')
        try:
            if len(args) == 2:
                text = CONFIG_FILE_EXPLAINER[args[0]][args[1]][0]
            else:
                text = CONFIG_FILE_EXPLAINER[args[0]][args[1]][args[2]][0]
        except KeyError:
            text = 'Not found'
        try:
            if len(args) == 2:
                error = CONFIG_FILE_EXPLAINER[args[0]][args[1]][1]
            else:
                error = CONFIG_FILE_EXPLAINER[args[0]][args[1]][args[2]][1]
        except KeyError:
            error = ''
        try:
            if len(args) == 2:
                details = CONFIG_FILE_EXPLAINER[args[0]][args[1]][2]
            else:
                details = CONFIG_FILE_EXPLAINER[args[0]][args[1]][args[2]][2]
        except KeyError:
            details = ''

        pop_up_window(text=text, entity='Info', errors=f'options:\n{error}', details=f'default:\n{details}')
