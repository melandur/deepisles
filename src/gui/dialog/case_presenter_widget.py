import os

from PyQt5 import QtCore, QtGui, QtWidgets

from src.core.configs.static_params import USED_MODALITY_NAMES
from src.gui.dialog.dialogs import pop_up_window


class LineEdit(QtWidgets.QLineEdit):
    """Cleaner gui"""

    def __init__(self, object_name, text):
        super().__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.setText(text)
        self.object_name = object_name
        self.setAlignment(QtCore.Qt.AlignLeft)
        self.setObjectName(object_name)
        x = self.fontMetrics()
        text_width = int(x.averageCharWidth() * len(text))
        self.setMinimumWidth(text_width)
        self.adjustSize()


class CasePresenterWidget(QtWidgets.QWidget):
    """Shows the found image paths to the user, which can check and adjust them before they got loaded"""

    def __init__(self, case_paths, callback):
        super().__init__()
        self.case_paths = case_paths
        self.callback = callback
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.setWindowTitle('Preload View - Check Paths')
        grid = QtWidgets.QGridLayout()
        grid.setAlignment(QtCore.Qt.AlignCenter)
        self.resize(1000, 100)

        # Case name
        grid.addWidget(QtWidgets.QLabel(''), 0, 0)
        grid.addWidget(QtWidgets.QLabel('Case:'), 0, 1)
        grid.addWidget(QtWidgets.QLabel(''), 0, 2)
        self.case_name = str(*self.case_paths)
        label_case_name = QtWidgets.QLabel(str(*self.case_paths))
        grid.addWidget(label_case_name, 0, 3)
        grid.addWidget(QtWidgets.QLabel(''), 0, 4)
        grid.addWidget(QtWidgets.QLabel(''), 1, 0)

        # Modality names with text editor
        index_tracker = 1
        for modality_name in USED_MODALITY_NAMES:
            if modality_name not in self.case_paths[self.case_name]:
                message = f'Set file path for {modality_name}'
                if 'seg' in modality_name:
                    message = f'Set file path for {modality_name} (optional)'
                self.case_paths[self.case_name][modality_name] = message

        for modality_name in sorted(self.case_paths[self.case_name]):
            index_tracker += 1
            label_modality_name = QtWidgets.QLabel(f'{modality_name.capitalize()}:')
            grid.addWidget(label_modality_name, index_tracker, 1)
            self.line_edit = LineEdit(modality_name, self.case_paths[self.case_name][modality_name])
            grid.addWidget(self.line_edit, index_tracker, 3)
            grid.addWidget(QtWidgets.QLabel(''), index_tracker + 1, 0)
            index_tracker += 1

        v_box = QtWidgets.QHBoxLayout()
        v_box.setAlignment(QtCore.Qt.AlignRight)

        # Button Cancel
        self.btn_cancel = QtWidgets.QPushButton(self)
        self.btn_cancel.setText('Cancel')
        self.btn_cancel.setMinimumWidth(200)
        self.btn_cancel.clicked.connect(self.close)
        v_box.addWidget(self.btn_cancel)

        v_box.addSpacing(10)

        # Button Ok
        self.btn_ok = QtWidgets.QPushButton(self)
        self.btn_ok.setText('Ok')
        self.btn_ok.setMinimumWidth(200)
        self.btn_ok.clicked.connect(self.ok_action)
        v_box.addWidget(self.btn_ok)

        box = QtWidgets.QVBoxLayout()
        box.addItem(grid)
        box.addItem(v_box)
        self.setLayout(box)
        self.move(QtWidgets.QDesktopWidget().availableGeometry().center() - self.frameGeometry().center())

    def ok_action(self):
        """Checks and updates user changes of the current case paths"""
        check = True
        for modality_name in self.case_paths[self.case_name]:
            line_edit = self.findChild(QtWidgets.QLineEdit, f'{modality_name}')
            if (
                not os.path.isfile(line_edit.text())
                and not os.path.isdir(line_edit.text())
                and 'seg' not in modality_name
            ):
                pop_up_window(
                    text=f'{modality_name.capitalize()} file path/dir does not exist',
                    entity='WARNING',
                    errors=f'Please check file path: \n\n{line_edit.text()}\n',
                    details='',
                )
                check = False
            else:
                line_edit_path = self.findChild(QtWidgets.QLineEdit, f'{modality_name}').text()
                self.case_paths[self.case_name][modality_name] = line_edit_path
        if check:
            try:
                self.callback(self.case_paths)
            except RuntimeError as e:
                raise e
            self.close()


if __name__ == '__main__':
    import sys

    from src.core.configs.config_file_handler import ConfigFileHandler
    from src.core.data_manager import DataAnalyzer

    app = QtWidgets.QApplication(sys.argv)

    folder_analyzer = DataAnalyzer()
    case_paths = folder_analyzer('/home/melandur/Data/Molab/molab_trainset_clean/cleaned/good/12OCT383474')
    cpw = CasePresenterWidget(case_paths)
    cpw.show()
    sys.exit(app.exec_())
