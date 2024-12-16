from loguru import logger
from PyQt5 import QtCore, QtWidgets

from src.gui.dialog.case_presenter_widget import CasePresenterWidget
from src.gui.dialog.dialogs import folder_load_dialog, pop_up_window
from src.gui.menu import UserPreferences
from src.path_library import BUILD_VERSION


class Menu(QtWidgets.QMainWindow):
    """Contains menu button layouts and connects those to functions"""

    def __init__(self, _mw, core, mw_viewers_updater):
        super().__init__()
        self.mw = _mw
        self.core = core
        self.mw_viewers_updater = mw_viewers_updater

        self.doc = None
        self.about = None
        self.user_pref_dialog = None
        self.case_path_presenter = None
        self.smart_segmentation_editor = None

        self.mw.menu = self.mw.menuBar()
        self.mw.menu.setContextMenuPolicy(QtCore.Qt.PreventContextMenu)

        file_menu = self.mw.menu.addMenu('File')  # File Menu
        self.open_files_button = QtWidgets.QAction('Load Case', self)
        self.open_files_button.triggered.connect(self.single_mode)
        file_menu.addAction(self.open_files_button)

        file_menu.addSeparator()

        self.preferences_button = QtWidgets.QAction('Preferences', self)
        self.preferences_button.triggered.connect(self.preferences_clicked)
        file_menu.addAction(self.preferences_button)

    def hide(self):
        """Hide menu"""
        self.mw.menu.hide()

    def show(self):
        """Show menu"""
        self.mw.menu.show()

    def disable(self):
        """Disable menu"""
        self.open_files_button.setEnabled(False)
        self.sse_button.setEnabled(False)
        self.meta_data_panel_button.setEnabled(False)

    def enable(self):
        """Enable menu"""
        self.open_files_button.setEnabled(True)
        self.sse_button.setEnabled(True)
        self.meta_data_panel_button.setEnabled(True)

    def preferences_clicked(self):
        """Opens user preference widget"""
        self.user_pref_dialog = UserPreferences(self.mw, self.preferences_clicked)
        self.user_pref_dialog.show()

    def single_mode(self):
        """Lets user pick a folder of files to show (searches also for the segmentation mask)"""
        self.core.data_handler.reset()
        load_check, folder_path = folder_load_dialog(self.core, 'Single Mode - Select a Case Folder')
        logger.debug(f'load_check: {load_check}, path: {folder_path}')
        if load_check:
            case_paths = self.core.folder_analyzer(folder_path)
            if len(case_paths.keys()) == 1:  # Assures that only one case is loaded
                self.case_path_presenter = CasePresenterWidget(case_paths, self.single_mode_callback)
                self.case_path_presenter.show()
                self.core.path_master.set_last_visited_folder(folder_path)
            else:
                text = 'The selected path contains to many options. \n Please try to be more specific'
                pop_up_window(text=text, entity='Information', errors='', details='')

    def single_mode_callback(self, case_paths):
        """Read and update viewer"""
        case_name = str(*case_paths)
        try:
            self.core.data_reader(case_name, case_paths)
            self.core.data_handler.copy_ephemeral_to_lasting_store(state='native')
            self.core.sync_viewers_stats.sync('native')
            self.mw_viewers_updater.refresh_viewers()
        except Exception as error:
            print(f'Error: {error}')
            pop_up_window(text=error, entity='Warning', errors='', details='')


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    mw = QtWidgets.QMainWindow()

    user_pref_dialog = UserPreferences(mw, None)
    user_pref_dialog.show()
    mw.show()
    exit_code = app.exec_()
