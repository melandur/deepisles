from PyQt5 import QtCore, QtWidgets


class CheckBox(QtWidgets.QCheckBox):
    """Code reduction goes brrrr"""

    def __init__(self, name, parent):
        super().__init__()
        self.setText(name)
        self.hint_box = parent.hint_text

    def enterEvent(self, event):  # pylint: disable=invalid-name
        """Returns hints for given process step"""
        if self.text() == 'Registration':
            self.hint_box.show_registration()
        elif self.text() == 'Skull Strip':
            self.hint_box.show_skull_stripping()
        elif self.text() == 'Segmentation':
            self.hint_box.show_segmentation()

    def leaveEvent(self, _):  # pylint: disable=invalid-name
        """Clear hint box in case of not hovering process step anymore"""
        self.hint_box.clear()


class MethodHints(QtWidgets.QLabel):
    """Give the user some insights"""

    def __init__(self, config_file):
        super().__init__()
        self.config_file = config_file
        self.setDisabled(True)
        self.setWordWrap(True)
        self.setAlignment(QtCore.Qt.AlignLeft)

    def clear(self):
        """Reset the hints text"""
        self.setText('\nThe order of processing is from top to bottom')

    def show_quality_agent(self):
        """shows quality agent hints"""
        self.clear()
        self.setText(
            '\nPerforms a brief quality check on the loaded data. Data which does not meet the expected data '
            'quality will be excluded. Deactivate the quality agent to process lower quality images at your '
            'own risk! (Alpha Feature)'
        )

    def show_registration(self):
        """shows registration hints"""
        self.clear()
        self.setText('\nRegisters the data to the default atlas MNI152_T1_1mm.')


    def show_skull_stripping(self):
        """shows skull strip hints"""
        self.clear()
        self.setText('\nPerforms skull stripping. Make sure to provide registered '
                     'data or select corresponding action above.')


    def show_segmentation(self):
        """shows segmentation hints"""
        self.clear()
        self.setText('\nDeactivated due to the use of an alternative atlas')
