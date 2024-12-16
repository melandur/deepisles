import re

from PyQt5 import QtCore, QtWidgets

from src.gui.dialog.dialogs import pop_up_window


class BaseLineEdit(QtWidgets.QLineEdit):
    def __init__(self, handler, args, optional):
        super().__init__()
        self.handler = handler
        self.args = args
        self.optional = optional
        object_name = '.'.join(args)
        self.setObjectName(object_name)
        self.textChanged[str].connect(self.save_state)

    def check_for_none(self, state):
        if state == '':
            return False
        if state.lower() == 'none':
            self.handler.set_conf(*self.args, value=None)
        return True


class LineEditInt(BaseLineEdit):
    def __init__(self, handler, args, optional):
        super().__init__(handler, args, optional)
        self.optional = optional
        self.setText(str(self.handler.get_conf(*self.args, optional=self.optional)))

    def load_state(self, state):
        """Get line edit string"""
        self.setText(str(state))

    def save_state(self, state):
        """Set line edit string"""
        try:
            if self.check_for_none(state):
                self.handler.set_conf(*self.args, value=int(state))
        except:
            pop_up_window(text='Type error', entity='Warning', errors=self.optional, details='Check info')


class LineEditFloat(BaseLineEdit):
    def __init__(self, handler, args, optional):
        super().__init__(handler, args, optional)
        self.optional = optional
        self.setText(str(self.handler.get_conf(*self.args, optional=self.optional)))

    def load_state(self, state):
        """Get line edit string"""
        self.setText(str(state))

    def save_state(self, state):
        """Set line edit string"""
        try:
            if self.check_for_none(state):
                self.handler.set_conf(*self.args, value=float(state))
        except:
            pop_up_window(text='Type error', entity='Warning', errors=self.optional, details='Check info')


class LineEditNone(BaseLineEdit):
    def __init__(self, handler, args, optional):
        super().__init__(handler, args, optional)
        self.optional = optional
        self.setText(str(self.handler.get_conf(*self.args, optional=self.optional)))

    def load_state(self, state):
        """Get line edit string"""
        self.setText(str(state))

    def save_state(self, state):
        """Set line edit string"""
        try:
            if self.check_for_none(state):
                if state.isdigit():
                    digitized_state = float(state)
                    if digitized_state.is_integer():
                        self.handler.set_conf(*self.args, value=int(state))
                    else:
                        self.handler.set_conf(*self.args, value=digitized_state)
        except:
            pop_up_window(text='Type error', entity='Warning', errors=self.optional, details='Check info')


class LineEditString(BaseLineEdit):
    def __init__(self, handler, args, optional):
        super().__init__(handler, args, optional)
        self.optional = optional
        self.setText(str(self.handler.get_conf(*self.args, optional=self.optional)))

    def load_state(self, state):
        """Get line edit string"""
        self.setText(str(state))

    def save_state(self, state):
        """Set line edit string"""
        try:
            if self.check_for_none(state):
                if state.isdigit():
                    digitized_state = float(state)
                    if digitized_state.is_integer():
                        self.handler.set_conf(*self.args, value=int(state))
                    else:
                        self.handler.set_conf(*self.args, value=digitized_state)
                else:
                    self.handler.set_conf(*self.args, value=str(state))
        except:
            pop_up_window(text='Type error', entity='Warning', errors=self.optional, details='Check info')


class LineEditListOfInt(BaseLineEdit):
    def __init__(self, handler, args, optional):
        super().__init__(handler, args, optional)
        self.optional = optional
        values = self.handler.get_conf(*self.args, optional=self.optional)
        self.setText(str(', '.join(str(value) for value in values)))

    def load_state(self, states):
        """Get line edit string"""
        self.setText(', '.join(str(state) for state in states))

    def save_state(self, state):
        """Set line edit string"""
        try:
            if state != '':
                value = re.sub(r',\s+', ',', state)  # remove all whitespaces after any coma
                value = value.split(',')  # string to list
                value = [int(x) for x in value if x]
                self.handler.set_conf(*self.args, value=value)
        except:
            pop_up_window(text='Type error', entity='Warning', errors=self.optional, details='Check info')


class LineEditListOfFloat(BaseLineEdit):
    def __init__(self, handler, args, optional):
        super().__init__(handler, args, optional)
        self.optional = optional
        values = self.handler.get_conf(*self.args, optional=self.optional)
        self.setText(str(', '.join(str(value) for value in values)))

    def load_state(self, states):
        """Get line edit string"""
        self.setText(', '.join(str(state) for state in states))

    def save_state(self, state):
        """Set line edit string"""
        try:
            if state != '':
                value = re.sub(r',\s+', ',', state)  # remove all whitespaces after any coma
                value = value.split(',')  # string to list
                value = [float(x) for x in value if x]
                self.handler.set_conf(*self.args, value=value)
        except:
            pop_up_window(text='Type error', entity='Warning', errors=self.optional, details='Check info')


class LineEditListOfStrings(BaseLineEdit):
    def __init__(self, handler, args, optional):
        super().__init__(handler, args, optional)
        self.optional = optional
        values = self.handler.get_conf(*self.args, optional=self.optional)
        self.setText(str(', '.join(str(value) for value in values)))

    def load_state(self, states):
        """Get line edit string"""
        self.setText(', '.join(str(state) for state in states))

    def save_state(self, state):
        """Set line edit string"""
        try:
            if state != '':
                value = re.sub(r',\s+', ',', state)  # remove all whitespaces after any coma
                value = value.split(',')  # string to list
                self.handler.set_conf(*self.args, value=value)
        except:
            pop_up_window(text='Type error', entity='Warning', errors=self.optional, details='Check info')


class CheckBox(QtWidgets.QCheckBox):
    """Cleaner gui and brr"""

    def __init__(self, handler, args):
        super().__init__()
        self.handler = handler
        self.args = args
        object_name = '.'.join(args)
        self.setObjectName(object_name)
        self.setChecked(self.handler.get_conf(*self.args, optional=False))
        self.stateChanged.connect(self.save_checkbox_state)

    def load_state(self, states):
        """Get check box state, in case of an error the optional will be returned"""
        self.setChecked(states)

    def save_checkbox_state(self, state):
        """Set check box state"""
        if state == QtCore.Qt.Checked:
            self.handler.set_conf(*self.args, value=True)
        else:
            self.handler.set_conf(*self.args, value=False)
