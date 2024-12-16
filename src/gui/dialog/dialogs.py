import os

from PyQt5 import QtCore, QtGui, QtWidgets


# - QMessageBox.Ok
# - QMessageBox.Open
# - QMessageBox.Save
# - QMessageBox.Cancel
# - QMessageBox.Close
# - QMessageBox.Yes
# - QMessageBox.No
# - QMessageBox.Abort
# - QMessageBox.Retry
# - QMessageBox.Ignore


def pop_up_window(text, entity='Information', errors='', details=''):
    """Popup window with consistent style and logo"""
    msg = QtWidgets.QMessageBox()
    if entity == 'Information':
        msg.setIcon(QtWidgets.QMessageBox.Information)
    elif entity == 'Warning':
        msg.setIcon(QtWidgets.QMessageBox.Warning)

    if errors != '' and details != '':
        message = f'{str(text)}\n\n{str(errors)}\n\n{str(details)}'
    elif errors != '' and details == '':
        message = f'{str(text)}\n\n{str(errors)}'
    else:
        message = f'{str(text)}'

    msg.setText(message)
    msg.setWindowTitle(entity)
    msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
    msg.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
    msg.resize(msg.size())
    msg.move(QtWidgets.QDesktopWidget().availableGeometry().center() - msg.frameGeometry().center())
    return msg.exec_()


def pop_up_window_forced_waiting(text, entity='Information', errors='', details=''):
    """Popup window with consistent style and logo, which can not be closed"""
    msg = QtWidgets.QMessageBox()
    if errors != '' and details != '':
        message = f'{str(text)}\n\n{str(errors)}\n\n{str(details)}'
    elif errors != '' and details == '':
        message = f'{str(text)}\n\n{str(errors)}'
    else:
        message = f'{str(text)}'

    msg.setText(message)
    msg.setWindowTitle(entity)
    msg.setIcon(QtWidgets.QMessageBox.Information)
    msg.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
    msg.setStandardButtons(QtWidgets.QMessageBox.NoButton)
    msg.resize(msg.size())
    msg.move(QtWidgets.QDesktopWidget().availableGeometry().center() - msg.frameGeometry().center())
    return msg


def restart_application_pop_up(widget, mw, text):
    """Informs the user that a restart is necessary in order to activate the latest settings"""

    def action(state):
        if 'ok' in state.text().lower():
            widget.config_file_handler.reset()
            widget.close()
            mw.close()

    msg = QtWidgets.QMessageBox()
    msg.setText(str(text))
    msg.setWindowTitle('Restart')
    msg.buttonClicked.connect(action)
    msg.setIcon(QtWidgets.QMessageBox.Question)
    msg.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
    msg.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
    msg.resize(msg.size())
    msg.move(QtWidgets.QDesktopWidget().availableGeometry().center() - msg.frameGeometry().center())
    msg.exec_()


def folder_load_dialog(core, title):
    """Opens dialog window on last visited folder, stores updated last visited folder"""

    last_visited_folder = core.path_master.get_last_visited_folder()
    dialog = QtWidgets.QFileDialog()
    dialog.setOption(QtWidgets.QFileDialog.DontUseNativeDialog, True)
    dialog.setFileMode(QtWidgets.QFileDialog.Directory)
    dialog.setWindowTitle(title)
    dialog.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
    dialog.setDirectory(last_visited_folder)
    dialog.resize(QtCore.QSize(800, 600))
    dialog.move(QtWidgets.QDesktopWidget().availableGeometry().center() - dialog.frameGeometry().center())
    if dialog.exec_():
        folder_path = ''.join(dialog.selectedFiles())
        if os.path.isdir(folder_path):
            return True, folder_path
        return False, None
    return False, None
