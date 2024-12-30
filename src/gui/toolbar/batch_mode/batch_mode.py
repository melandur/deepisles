# pylint: disable=duplicate-code

import os

from loguru import logger
from PyQt5 import QtCore, QtWidgets, QtGui
from pyqtspinner.spinner import WaitingSpinner

from src.core.configs.static_params import USED_MODALITY_NAMES
from src.core.pipeline import Pipeline
from src.core.utils import dump_log
from src.gui.dialog.dialogs import pop_up_window, pop_up_window_forced_waiting
from src.gui.toolbar.batch_mode.tree_view import BMTreeView
from src.gui.toolbar.template import CheckBox
from src.path_library import DEFAULT_EXPORT_FOLDER


class BatchMode(QtWidgets.QWidget):
    """Search in folder for cases and perform registration, skull-stripping, segmentation on complete cases"""

    def __init__(self, mw, core, folder_path, cb_unblock):
        super().__init__()
        self.mw = mw
        self.core = core
        self.folder_path = folder_path
        self.cb_unblock = cb_unblock

        self.state = QtWidgets.QLabel('')
        self.spinner = None
        self.pipeline = None
        self.hint_text = None
        self.case_name = QtWidgets.QLabel('')
        self.progress = QtWidgets.QLabel('')
        self.block_popup = None
        self.progress_tot = None

        self.button_run = None
        self.button_stop = None
        self.button_1 = None
        self.button_2 = None
        self.button_3 = None
        self.button_4 = None
        self.button_5 = None
        self.button_6 = None

        self.case_paths = core.folder_analyzer(folder_path)
        case_paths = core.folder_analyzer(folder_path)
        self.checked_case_paths = self.check_for_completeness(case_paths)  # adds a completeness check tag per modality
        self.tree_view = BMTreeView(self.checked_case_paths)

        logger.info(f'Init {self.__class__.__name__}')
        self.init_layout(self.core)
        self.move(QtWidgets.QDesktopWidget().availableGeometry().center() - self.frameGeometry().center())

    def init_layout(self, core):
        """Defines the gui layout"""
        config_file = core.config_file_handler.get_conf_dict()

        self.setWindowTitle('Batch Mode')

        main_hb = QtWidgets.QHBoxLayout()
        main_hb.addWidget(self.tree_view)

        v_b = QtWidgets.QVBoxLayout()
        self.hint_text = QtWidgets.QLabel('')
        self.hint_text.setFixedWidth(200)

        self.button_1 = CheckBox('Skull strip', self)
        self.button_1.stateChanged.connect(self.check_box_1)
        if config_file['dockers']['params']['skull_strip']:
            self.button_1.setChecked(True)
        self.button_1.setEnabled(True)
        v_b.addWidget(self.button_1)

        self.button_2 = CheckBox('Fast', self)
        self.button_2.stateChanged.connect(self.check_box_2)
        if config_file['dockers']['params']['fast']:
            self.button_2.setChecked(True)
        self.button_2.setEnabled(True)
        v_b.addWidget(self.button_2)

        self.button_3 = CheckBox('Parallelize', self)
        self.button_3.stateChanged.connect(self.check_box_3)
        if config_file['dockers']['params']['parallelize']:
            self.button_3.setChecked(True)
        self.button_3.setEnabled(True)
        v_b.addWidget(self.button_3)

        self.button_4 = CheckBox('Save Team outputs', self)
        self.button_4.stateChanged.connect(self.check_box_4)
        if config_file['dockers']['params']['save_team_outputs']:
            self.button_4.setChecked(True)
        self.button_4.setEnabled(True)
        v_b.addWidget(self.button_4)

        self.button_5 = CheckBox('Results MNI', self)
        self.button_5.stateChanged.connect(self.check_box_5)
        if config_file['dockers']['params']['results_mni']:
            self.button_5.setChecked(True)
        self.button_5.setEnabled(True)
        v_b.addWidget(self.button_5)

        v_b.addWidget(self.hint_text)
        v_b.addStretch()

        sub_hb_1 = QtWidgets.QHBoxLayout()
        self.case_name = QtWidgets.QLabel('')
        sub_hb_1.addWidget(self.case_name)

        sub_hb_2 = QtWidgets.QHBoxLayout()
        self.state = QtWidgets.QLabel('')
        sub_hb_2.addWidget(self.state)

        sub_hb_3 = QtWidgets.QHBoxLayout()
        self.progress = QtWidgets.QLabel('')
        sub_hb_3.addWidget(self.progress)

        self.spinner = WaitingSpinner(
            self,
            center_on_parent=False,
            disable_parent_when_spinning=False,
            modality=QtCore.Qt.ApplicationModal,
            roundness=100.0,
            fade=80.0,
            lines=20,
            line_length=10,
            line_width=2,
            radius=4,
            color=QtGui.QColor(255, 255, 255),
        )
        self.spinner.stop()
        sub_hb_3.addWidget(self.spinner, alignment=QtCore.Qt.AlignHCenter)

        v_b.addItem(sub_hb_1)
        v_b.addItem(sub_hb_2)
        v_b.addItem(sub_hb_3)
        v_b.addSpacing(10)


        sub_hb_2 = QtWidgets.QHBoxLayout()
        self.button_run = QtWidgets.QPushButton('Run', self)
        self.button_run.setFixedWidth(100)
        self.button_run.clicked.connect(self.run_batch_mode)
        sub_hb_2.addWidget(self.button_run)
        sub_hb_2.addSpacing(5)
        self.button_stop = QtWidgets.QPushButton('Stop', self)
        self.button_stop.setDisabled(True)
        self.button_stop.setFixedWidth(100)
        self.button_stop.clicked.connect(self.stop_batch_mode)
        sub_hb_2.addWidget(self.button_stop)
        v_b.addItem(sub_hb_2)
        main_hb.addItem(v_b)
        self.setLayout(main_hb)
        self.resize(1200, 600)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.show()
        self.activateWindow()

    @staticmethod
    def check_box_1(checked):
        """Get checkbox state of registration button"""
        state = False
        if checked == QtCore.Qt.Checked:
            state = True
        return state

    @staticmethod
    def check_box_2(checked):
        """Get checkbox state of stripping button"""
        state = False
        if checked == QtCore.Qt.Checked:
            state = True
        return state

    @staticmethod
    def check_box_3(checked):
        """Get checkbox state of segmentation button"""
        state = False
        if checked == QtCore.Qt.Checked:
            state = True
        return state

    @staticmethod
    def check_box_4(checked):
        """Get checkbox state of registration button"""
        state = False
        if checked == QtCore.Qt.Checked:
            state = True
        return state

    @staticmethod
    def check_box_5(checked):
        """Get checkbox state of registration button"""
        state = False
        if checked == QtCore.Qt.Checked:
            state = True
        return state


    @staticmethod
    def show_main():
        """Show main gui again"""
        pop_up_window(
            f'Batch mode has successfully finished. The results are in: {DEFAULT_EXPORT_FOLDER}', 'Information'
        )

    def closeEvent(self, _):  # pylint: disable=invalid-name
        """Widget close behaviour"""
        self.cb_unblock()
        self.mw.show()
        self.core.folder_analyzer.reset()

    def stop_batch_mode(self):
        """Stop batch mode, killing threads, reset gui"""
        logger.debug('Stop batch mode')
        if self.pipeline:
            self.pipeline.alive = False
        self.button_stop.setDisabled(True)
        self.block_popup = pop_up_window_forced_waiting(
            'The software waits until the active process is finished. This may take a while depending on the process'
        )
        self.block_popup.show()

    def run_batch_mode(self):
        """Start batch mode"""
        logger.info('Run batch mode')
        self.mw.hide()
        self.clean_dict()

        # Get state of buttons
        state_btn_1 = self.button_1.checkState()
        state_btn_2 = self.button_2.checkState()
        state_btn_3 = self.button_3.checkState()
        state_btn_4 = self.button_4.checkState()
        state_btn_5 = self.button_5.checkState()

        # Assign button state to config file
        config_file = self.core.config_file_handler.get_conf_dict()
        config_file['dockers']['params']['skull_strip'] = state_btn_1
        config_file['dockers']['params']['fast'] = state_btn_2
        config_file['dockers']['params']['parallelize'] = state_btn_3
        config_file['dockers']['params']['save_team_outputs'] = state_btn_4
        config_file['dockers']['params']['results_mni'] = state_btn_5

        tot_cases = len(self.case_paths)
        self.progress_tot = tot_cases

        # Connect and start pipeline
        self.pipeline = Pipeline(self, self.case_paths, config_file, self.core.data_handler)
        self.pipeline.started.connect(self.start_condition)
        self.pipeline.case_name_message.connect(self.update_case_name_message)
        self.pipeline.state_message.connect(self.update_state_message)
        self.pipeline.state_index_message.connect(self.update_progress_message)
        self.pipeline.error_message.connect(dump_log)
        self.pipeline.finished.connect(self.finished)
        self.pipeline.start()

    def start_condition(self):
        """Will be executed at the start of the pipeline thread"""
        self.button_run.setDisabled(True)
        self.button_stop.setDisabled(False)
        self.spinner.start()

    def update_case_name_message(self, message):
        """Updates case name on emited signal from thread"""
        self.case_name.setText(message)

    def update_state_message(self, message):
        """Updates process state on emited signal from thread"""
        self.state.setText(message)

    def update_progress_message(self, message):
        """Updates state index on emited signal from thread"""
        self.progress.setText(f'Progress: {message}/{self.progress_tot}')

    def finished(self):
        """Will be executed when the pipeline finishes"""
        self.button_run.setDisabled(False)
        self.button_stop.setDisabled(True)
        self.progress.setText('')
        self.spinner.stop()
        self.reset_text()
        if self.block_popup:
            self.block_popup.done(1)

    def reset_text(self):
        """Set all the text output to default empty strings"""
        self.case_name.setText('')
        self.state.setText('')
        self.progress.setText('')

    def clean_dict(self):
        """Remove cases from dictionary with missing modalities entries"""
        cases_to_delete = []
        for case in self.checked_case_paths:
            for modality in self.checked_case_paths[case]:
                if 'flair' != modality:
                    if self.checked_case_paths[case][modality]['completeness_check_tag'] == 'no':
                        logger.debug(f'Clean dict removed case: {case}')
                        cases_to_delete.append(case)

        for del_case in cases_to_delete:
            self.case_paths.pop(del_case, None)

    @staticmethod
    def check_for_completeness(case_paths):
        """Check that all modalities have valid paths, then adds meta ok flag"""
        for case in case_paths:
            for modality in USED_MODALITY_NAMES:
                tmp_path_store = case_paths[case][modality]
                case_paths[case][modality] = {}
                case_paths[case][modality]['file_path'] = tmp_path_store
                case_paths[case][modality]['completeness_check_tag'] = 'no'
                if tmp_path_store:
                    if os.path.isfile(tmp_path_store) or os.path.isdir(tmp_path_store):
                        case_paths[case][modality]['completeness_check_tag'] = 'yes'
        return case_paths
