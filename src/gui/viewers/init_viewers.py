# pylint: disable=duplicate-code


import copy
import os

from PyQt5 import QtCore, QtWidgets

from src.core.configs.static_params import USED_MODALITY_NAMES
from src.gui.dialog.case_presenter_widget import CasePresenterWidget
from src.gui.dialog.dialogs import pop_up_window
from src.gui.viewers.custom_view import (
    CustomQDockWidget,
    CustomSidePanelQTableWidget,
    CustomSidePanelQTabWidget,
    ViewerQLabel,
)


class InitViewers:
    """Initialize the viewers"""

    def __init__(self, mw, core, mw_viewers_updater):
        self.mw = mw
        self.core = core
        self.mw_viewers_updater = mw_viewers_updater
        self.case_path_presenter = None

        # Side panel viewer
        self.tab_widget = CustomSidePanelQTabWidget()
        self.stat_widget = CustomSidePanelQTableWidget()
        self.core.viewer_stats.left_panel_widget.setWidget(self.tab_widget)

        number_of_viewers = 4
        used_modalities = copy.deepcopy(USED_MODALITY_NAMES)
        if 'seg_mask' in used_modalities:
            used_modalities.remove('seg_mask')

        count_modalities = len(used_modalities)
        if 2 < count_modalities <= 4:
            number_of_viewers = 4
        elif 4 < count_modalities <= 6:
            number_of_viewers = 6
        elif 6 < count_modalities:
            number_of_viewers = 8

        if number_of_viewers == 4:
            # Viewer 1
            self.core.viewer_stats.viewer_1.qlabel_viewer = ViewerQLabel(
                self.core.viewer_stats.viewer_1,
                self.mw_viewers_updater.refresh_viewers,
                self.init_empty,
            )
            self.core.viewer_stats.viewer_1.docked_widget = CustomQDockWidget(
                viewer_stats=self.core.viewer_stats.viewer_1,
                cb_update_viewers=self.mw_viewers_updater.refresh_viewers,
                cb_drag_and_drop=self.callback_drag_and_drop_with_viewer_update,
                cb_qlabel_viewer=self.core.viewer_stats.viewer_1.qlabel_viewer,
            )
            self.core.viewer_stats.viewer_1.docked_widget.setWidget(self.core.viewer_stats.viewer_1.qlabel_viewer)
            #
            # # Viewer 2
            self.core.viewer_stats.viewer_2.qlabel_viewer = ViewerQLabel(
                self.core.viewer_stats.viewer_2,
                self.mw_viewers_updater.refresh_viewers,
                self.init_empty,
            )
            self.core.viewer_stats.viewer_2.docked_widget = CustomQDockWidget(
                viewer_stats=self.core.viewer_stats.viewer_2,
                cb_update_viewers=self.mw_viewers_updater.refresh_viewers,
                cb_drag_and_drop=self.callback_drag_and_drop_with_viewer_update,
                cb_qlabel_viewer=self.core.viewer_stats.viewer_2.qlabel_viewer,
            )
            self.core.viewer_stats.viewer_2.docked_widget.setWidget(self.core.viewer_stats.viewer_2.qlabel_viewer)

            # Viewer 3
            self.core.viewer_stats.viewer_3.qlabel_viewer = ViewerQLabel(
                self.core.viewer_stats.viewer_3,
                self.mw_viewers_updater.refresh_viewers,
                self.init_empty,
            )
            self.core.viewer_stats.viewer_3.docked_widget = CustomQDockWidget(
                viewer_stats=self.core.viewer_stats.viewer_3,
                cb_update_viewers=self.mw_viewers_updater.refresh_viewers,
                cb_drag_and_drop=self.callback_drag_and_drop_with_viewer_update,
                cb_qlabel_viewer=self.core.viewer_stats.viewer_3.qlabel_viewer,
            )
            self.core.viewer_stats.viewer_3.docked_widget.setWidget(self.core.viewer_stats.viewer_3.qlabel_viewer)

            # Viewer 4
            self.core.viewer_stats.viewer_4.qlabel_viewer = ViewerQLabel(
                self.core.viewer_stats.viewer_4,
                self.mw_viewers_updater.refresh_viewers,
                self.init_empty,
            )
            self.core.viewer_stats.viewer_4.docked_widget = CustomQDockWidget(
                viewer_stats=self.core.viewer_stats.viewer_4,
                cb_update_viewers=self.mw_viewers_updater.refresh_viewers,
                cb_drag_and_drop=self.callback_drag_and_drop_with_viewer_update,
                cb_qlabel_viewer=self.core.viewer_stats.viewer_4.qlabel_viewer,
            )
            self.core.viewer_stats.viewer_4.docked_widget.setWidget(self.core.viewer_stats.viewer_4.qlabel_viewer)

            # """Defines the order and orientation of 4 main viewers"""
            self.mw.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.core.viewer_stats.left_panel_widget)
            self.mw.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.core.viewer_stats.viewer_1.docked_widget)
            self.mw.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.core.viewer_stats.viewer_2.docked_widget)

            self.mw.splitDockWidget(
                self.core.viewer_stats.viewer_1.docked_widget,
                self.core.viewer_stats.viewer_2.docked_widget,
                QtCore.Qt.Horizontal,
            )

            self.mw.splitDockWidget(
                self.core.viewer_stats.viewer_1.docked_widget,
                self.core.viewer_stats.viewer_2.docked_widget,
                QtCore.Qt.Horizontal,
            )

            self.mw.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.core.viewer_stats.viewer_3.docked_widget)
            self.mw.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.core.viewer_stats.viewer_4.docked_widget)

            self.mw.splitDockWidget(
                self.core.viewer_stats.viewer_3.docked_widget,
                self.core.viewer_stats.viewer_4.docked_widget,
                QtCore.Qt.Horizontal,
            )

            self.core.float_left_panel = QtWidgets.QStackedWidget()
            self.core.float_left_panel.hide()

        elif number_of_viewers == 6:
            # Viewer 1
            self.core.viewer_stats.viewer_1.qlabel_viewer = ViewerQLabel(
                self.core.viewer_stats.viewer_1,
                self.mw_viewers_updater.refresh_viewers,
                self.init_empty,
            )
            self.core.viewer_stats.viewer_1.docked_widget = CustomQDockWidget(
                viewer_stats=self.core.viewer_stats.viewer_1,
                cb_update_viewers=self.mw_viewers_updater.refresh_viewers,
                cb_drag_and_drop=self.callback_drag_and_drop_with_viewer_update,
                cb_qlabel_viewer=self.core.viewer_stats.viewer_1.qlabel_viewer,
            )
            self.core.viewer_stats.viewer_1.docked_widget.setWidget(self.core.viewer_stats.viewer_1.qlabel_viewer)

            # Viewer 2
            self.core.viewer_stats.viewer_2.qlabel_viewer = ViewerQLabel(
                self.core.viewer_stats.viewer_2,
                self.mw_viewers_updater.refresh_viewers,
                self.init_empty,
            )
            self.core.viewer_stats.viewer_2.docked_widget = CustomQDockWidget(
                viewer_stats=self.core.viewer_stats.viewer_2,
                cb_update_viewers=self.mw_viewers_updater.refresh_viewers,
                cb_drag_and_drop=self.callback_drag_and_drop_with_viewer_update,
                cb_qlabel_viewer=self.core.viewer_stats.viewer_2.qlabel_viewer,
            )
            self.core.viewer_stats.viewer_2.docked_widget.setWidget(self.core.viewer_stats.viewer_2.qlabel_viewer)

            # Viewer 3
            self.core.viewer_stats.viewer_3.qlabel_viewer = ViewerQLabel(
                self.core.viewer_stats.viewer_3,
                self.mw_viewers_updater.refresh_viewers,
                self.init_empty,
            )
            self.core.viewer_stats.viewer_3.docked_widget = CustomQDockWidget(
                viewer_stats=self.core.viewer_stats.viewer_3,
                cb_update_viewers=self.mw_viewers_updater.refresh_viewers,
                cb_drag_and_drop=self.callback_drag_and_drop_with_viewer_update,
                cb_qlabel_viewer=self.core.viewer_stats.viewer_3.qlabel_viewer,
            )
            self.core.viewer_stats.viewer_3.docked_widget.setWidget(self.core.viewer_stats.viewer_3.qlabel_viewer)

            # Viewer 4
            self.core.viewer_stats.viewer_4.qlabel_viewer = ViewerQLabel(
                self.core.viewer_stats.viewer_4,
                self.mw_viewers_updater.refresh_viewers,
                self.init_empty,
            )
            self.core.viewer_stats.viewer_4.docked_widget = CustomQDockWidget(
                viewer_stats=self.core.viewer_stats.viewer_4,
                cb_update_viewers=self.mw_viewers_updater.refresh_viewers,
                cb_drag_and_drop=self.callback_drag_and_drop_with_viewer_update,
                cb_qlabel_viewer=self.core.viewer_stats.viewer_4.qlabel_viewer,
            )
            self.core.viewer_stats.viewer_4.docked_widget.setWidget(self.core.viewer_stats.viewer_4.qlabel_viewer)

            # Viewer 5
            self.core.viewer_stats.viewer_5.qlabel_viewer = ViewerQLabel(
                self.core.viewer_stats.viewer_5,
                self.mw_viewers_updater.refresh_viewers,
                self.init_empty,
            )
            self.core.viewer_stats.viewer_5.docked_widget = CustomQDockWidget(
                viewer_stats=self.core.viewer_stats.viewer_5,
                cb_update_viewers=self.mw_viewers_updater.refresh_viewers,
                cb_drag_and_drop=self.callback_drag_and_drop_with_viewer_update,
                cb_qlabel_viewer=self.core.viewer_stats.viewer_5.qlabel_viewer,
            )
            self.core.viewer_stats.viewer_5.docked_widget.setWidget(self.core.viewer_stats.viewer_5.qlabel_viewer)

            # Viewer 6
            self.core.viewer_stats.viewer_6.qlabel_viewer = ViewerQLabel(
                self.core.viewer_stats.viewer_6,
                self.mw_viewers_updater.refresh_viewers,
                self.init_empty,
            )
            self.core.viewer_stats.viewer_6.docked_widget = CustomQDockWidget(
                viewer_stats=self.core.viewer_stats.viewer_6,
                cb_update_viewers=self.mw_viewers_updater.refresh_viewers,
                cb_drag_and_drop=self.callback_drag_and_drop_with_viewer_update,
                cb_qlabel_viewer=self.core.viewer_stats.viewer_6.qlabel_viewer,
            )
            self.core.viewer_stats.viewer_6.docked_widget.setWidget(self.core.viewer_stats.viewer_6.qlabel_viewer)

            self.mw.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.core.viewer_stats.left_panel_widget)  # 6 viewers

            self.mw.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.core.viewer_stats.viewer_1.docked_widget)
            self.mw.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.core.viewer_stats.viewer_2.docked_widget)
            self.mw.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.core.viewer_stats.viewer_3.docked_widget)

            self.mw.splitDockWidget(
                self.core.viewer_stats.viewer_1.docked_widget,
                self.core.viewer_stats.viewer_2.docked_widget,
                QtCore.Qt.Horizontal,
            )

            self.mw.splitDockWidget(
                self.core.viewer_stats.viewer_2.docked_widget,
                self.core.viewer_stats.viewer_3.docked_widget,
                QtCore.Qt.Horizontal,
            )

            self.mw.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.core.viewer_stats.viewer_4.docked_widget)
            self.mw.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.core.viewer_stats.viewer_5.docked_widget)
            self.mw.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.core.viewer_stats.viewer_6.docked_widget)

            self.mw.splitDockWidget(
                self.core.viewer_stats.viewer_4.docked_widget,
                self.core.viewer_stats.viewer_5.docked_widget,
                QtCore.Qt.Horizontal,
            )

            self.mw.splitDockWidget(
                self.core.viewer_stats.viewer_5.docked_widget,
                self.core.viewer_stats.viewer_6.docked_widget,
                QtCore.Qt.Horizontal,
            )

            self.core.float_left_panel = QtWidgets.QStackedWidget()
            self.core.float_left_panel.hide()

        elif number_of_viewers == 8:
            # Viewer 1
            self.core.viewer_stats.viewer_1.qlabel_viewer = ViewerQLabel(
                self.core.viewer_stats.viewer_1,
                self.mw_viewers_updater.refresh_viewers,
                self.init_empty,
            )
            self.core.viewer_stats.viewer_1.docked_widget = CustomQDockWidget(
                viewer_stats=self.core.viewer_stats.viewer_1,
                cb_update_viewers=self.mw_viewers_updater.refresh_viewers,
                cb_drag_and_drop=self.callback_drag_and_drop_with_viewer_update,
                cb_qlabel_viewer=self.core.viewer_stats.viewer_1.qlabel_viewer,
            )
            self.core.viewer_stats.viewer_1.docked_widget.setWidget(self.core.viewer_stats.viewer_1.qlabel_viewer)

            # Viewer 2
            self.core.viewer_stats.viewer_2.qlabel_viewer = ViewerQLabel(
                self.core.viewer_stats.viewer_2,
                self.mw_viewers_updater.refresh_viewers,
                self.init_empty,
            )
            self.core.viewer_stats.viewer_2.docked_widget = CustomQDockWidget(
                viewer_stats=self.core.viewer_stats.viewer_2,
                cb_update_viewers=self.mw_viewers_updater.refresh_viewers,
                cb_drag_and_drop=self.callback_drag_and_drop_with_viewer_update,
                cb_qlabel_viewer=self.core.viewer_stats.viewer_2.qlabel_viewer,
            )
            self.core.viewer_stats.viewer_2.docked_widget.setWidget(self.core.viewer_stats.viewer_2.qlabel_viewer)

            # Viewer 3
            self.core.viewer_stats.viewer_3.qlabel_viewer = ViewerQLabel(
                self.core.viewer_stats.viewer_3,
                self.mw_viewers_updater.refresh_viewers,
                self.init_empty,
            )
            self.core.viewer_stats.viewer_3.docked_widget = CustomQDockWidget(
                viewer_stats=self.core.viewer_stats.viewer_3,
                cb_update_viewers=self.mw_viewers_updater.refresh_viewers,
                cb_drag_and_drop=self.callback_drag_and_drop_with_viewer_update,
                cb_qlabel_viewer=self.core.viewer_stats.viewer_3.qlabel_viewer,
            )
            self.core.viewer_stats.viewer_3.docked_widget.setWidget(self.core.viewer_stats.viewer_3.qlabel_viewer)

            # Viewer 4
            self.core.viewer_stats.viewer_4.qlabel_viewer = ViewerQLabel(
                self.core.viewer_stats.viewer_4,
                self.mw_viewers_updater.refresh_viewers,
                self.init_empty,
            )
            self.core.viewer_stats.viewer_4.docked_widget = CustomQDockWidget(
                viewer_stats=self.core.viewer_stats.viewer_4,
                cb_update_viewers=self.mw_viewers_updater.refresh_viewers,
                cb_drag_and_drop=self.callback_drag_and_drop_with_viewer_update,
                cb_qlabel_viewer=self.core.viewer_stats.viewer_4.qlabel_viewer,
            )
            self.core.viewer_stats.viewer_4.docked_widget.setWidget(self.core.viewer_stats.viewer_4.qlabel_viewer)

            # Viewer 5
            self.core.viewer_stats.viewer_5.qlabel_viewer = ViewerQLabel(
                self.core.viewer_stats.viewer_5,
                self.mw_viewers_updater.refresh_viewers,
                self.init_empty,
            )
            self.core.viewer_stats.viewer_5.docked_widget = CustomQDockWidget(
                viewer_stats=self.core.viewer_stats.viewer_5,
                cb_update_viewers=self.mw_viewers_updater.refresh_viewers,
                cb_drag_and_drop=self.callback_drag_and_drop_with_viewer_update,
                cb_qlabel_viewer=self.core.viewer_stats.viewer_5.qlabel_viewer,
            )
            self.core.viewer_stats.viewer_5.docked_widget.setWidget(self.core.viewer_stats.viewer_5.qlabel_viewer)

            # Viewer 6
            self.core.viewer_stats.viewer_6.qlabel_viewer = ViewerQLabel(
                self.core.viewer_stats.viewer_6,
                self.mw_viewers_updater.refresh_viewers,
                self.init_empty,
            )
            self.core.viewer_stats.viewer_6.docked_widget = CustomQDockWidget(
                viewer_stats=self.core.viewer_stats.viewer_6,
                cb_update_viewers=self.mw_viewers_updater.refresh_viewers,
                cb_drag_and_drop=self.callback_drag_and_drop_with_viewer_update,
                cb_qlabel_viewer=self.core.viewer_stats.viewer_6.qlabel_viewer,
            )
            self.core.viewer_stats.viewer_6.docked_widget.setWidget(self.core.viewer_stats.viewer_6.qlabel_viewer)

            # Viewer 7
            self.core.viewer_stats.viewer_7.qlabel_viewer = ViewerQLabel(
                self.core.viewer_stats.viewer_7,
                self.mw_viewers_updater.refresh_viewers,
                self.init_empty,
            )
            self.core.viewer_stats.viewer_7.docked_widget = CustomQDockWidget(
                viewer_stats=self.core.viewer_stats.viewer_7,
                cb_update_viewers=self.mw_viewers_updater.refresh_viewers,
                cb_drag_and_drop=self.callback_drag_and_drop_with_viewer_update,
                cb_qlabel_viewer=self.core.viewer_stats.viewer_7.qlabel_viewer,
            )
            self.core.viewer_stats.viewer_7.docked_widget.setWidget(self.core.viewer_stats.viewer_7.qlabel_viewer)

            # Viewer 8
            self.core.viewer_stats.viewer_8.qlabel_viewer = ViewerQLabel(
                self.core.viewer_stats.viewer_8,
                self.mw_viewers_updater.refresh_viewers,
                self.init_empty,
            )
            self.core.viewer_stats.viewer_8.docked_widget = CustomQDockWidget(
                viewer_stats=self.core.viewer_stats.viewer_8,
                cb_update_viewers=self.mw_viewers_updater.refresh_viewers,
                cb_drag_and_drop=self.callback_drag_and_drop_with_viewer_update,
                cb_qlabel_viewer=self.core.viewer_stats.viewer_8.qlabel_viewer,
            )
            self.core.viewer_stats.viewer_8.docked_widget.setWidget(self.core.viewer_stats.viewer_8.qlabel_viewer)

            self.mw.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.core.viewer_stats.left_panel_widget)  # 8 viewers

            self.mw.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.core.viewer_stats.viewer_1.docked_widget)
            self.mw.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.core.viewer_stats.viewer_2.docked_widget)
            self.mw.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.core.viewer_stats.viewer_3.docked_widget)
            self.mw.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.core.viewer_stats.viewer_4.docked_widget)

            self.mw.splitDockWidget(
                self.core.viewer_stats.viewer_1.docked_widget,
                self.core.viewer_stats.viewer_2.docked_widget,
                QtCore.Qt.Horizontal,
            )

            self.mw.splitDockWidget(
                self.core.viewer_stats.viewer_2.docked_widget,
                self.core.viewer_stats.viewer_3.docked_widget,
                QtCore.Qt.Horizontal,
            )

            self.mw.splitDockWidget(
                self.core.viewer_stats.viewer_3.docked_widget,
                self.core.viewer_stats.viewer_4.docked_widget,
                QtCore.Qt.Horizontal,
            )

            self.mw.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.core.viewer_stats.viewer_5.docked_widget)
            self.mw.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.core.viewer_stats.viewer_6.docked_widget)
            self.mw.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.core.viewer_stats.viewer_7.docked_widget)
            self.mw.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.core.viewer_stats.viewer_8.docked_widget)

            self.mw.splitDockWidget(
                self.core.viewer_stats.viewer_5.docked_widget,
                self.core.viewer_stats.viewer_6.docked_widget,
                QtCore.Qt.Horizontal,
            )

            self.mw.splitDockWidget(
                self.core.viewer_stats.viewer_6.docked_widget,
                self.core.viewer_stats.viewer_7.docked_widget,
                QtCore.Qt.Horizontal,
            )

            self.mw.splitDockWidget(
                self.core.viewer_stats.viewer_7.docked_widget,
                self.core.viewer_stats.viewer_8.docked_widget,
                QtCore.Qt.Horizontal,
            )

            self.core.float_left_panel = QtWidgets.QStackedWidget()
            self.core.float_left_panel.hide()

    def callback_drag_and_drop_with_viewer_update(self, data_path):
        """Allows drag and drop of a file or folder"""
        folder_path = None
        if os.path.isfile(data_path):
            folder_path = os.path.dirname(data_path)
        elif os.path.isdir(data_path):
            folder_path = data_path

        if folder_path:
            case_paths = self.core.folder_analyzer(folder_path)
            if len(case_paths.keys()) == 1:  # Assures that only one case is loaded
                self.case_path_presenter = CasePresenterWidget(case_paths, self.single_mode_callback)
                self.case_path_presenter.show()
                self.core.path_master.set_last_visited_folder(os.path.dirname(folder_path))
            else:
                text = 'The selected path contains to many options. \n Please try to be more specific'
                pop_up_window(text=text, entity='Information', errors='', details='')

    def single_mode_callback(self, case_paths):
        """Read and update viewer"""
        case_name = str(*case_paths)
        try:
            self.core.data_reader(case_name, case_paths)
            self.core.data_handler.copy_ephemeral_to_lasting_store()
            self.core.sync_viewers_stats.sync('native')
            self.mw_viewers_updater.refresh_viewers()
        except Exception as error:
            pop_up_window(text=error, entity='Warning', errors='', details='')

    def init_empty(self):
        """Init empty viewers, which will be loaded later on"""
