# pylint: disable=invalid-name

import os

from loguru import logger
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt

from src.path_library import ICONS_BASE_PATH


class ViewerQLabel(QtWidgets.QLabel):
    """Viewer main window"""

    def __init__(self, viewer_stats, cb_update_viewers, cb_scroll):
        super().__init__()
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setAcceptDrops(True)
        self.setScaledContents(False)
        self.setStyleSheet('QLabel {background : black;}')
        self.setMinimumSize(100, 100)
        self.setContextMenuPolicy(QtCore.Qt.PreventContextMenu)

        self.viewer_stats = viewer_stats
        self.cb_update_viewers = cb_update_viewers
        self.cb_scroll = cb_scroll

    @QtCore.pyqtSlot()
    def zoom(self, delta, pos):
        self.viewer_stats.zoom_factor -= delta
        self.viewer_stats.zoom_pos = (pos.x(), pos.y())

    @QtCore.pyqtSlot()
    def resizeEvent(self, event):
        self.cb_update_viewers()
        event.accept()

    @logger.catch()
    @QtCore.pyqtSlot()
    def wheelEvent(self, event) -> None:
        modifiers = QtWidgets.qApp.keyboardModifiers()
        delta = event.angleDelta()
        delta = int(QtCore.QPoint.y(delta) / 120)
        if delta == 0:
            pass
        else:
            if modifiers == QtCore.Qt.ShiftModifier:
                if self.viewer_stats.img_opacity is not None and self.viewer_stats.img_data is not None:
                    min_scroll_value = 0
                    max_scroll_value = 100
                    delta *= 10
                    if max_scroll_value >= self.viewer_stats.img_opacity + delta >= min_scroll_value:
                        self.viewer_stats.img_opacity += delta
                        self.cb_update_viewers()
            elif modifiers == QtCore.Qt.ControlModifier:
                try:
                    self.zoom(delta, event.pos())
                    self.cb_update_viewers()
                except:
                    pass
            else:
                if self.viewer_stats.img_index is not None and self.viewer_stats.img_data is not None:
                    if (
                        self.viewer_stats.img_index_max
                        > self.viewer_stats.img_index - delta
                        >= self.viewer_stats.img_index_min
                    ):
                        self.viewer_stats.img_index -= delta
                        self.cb_scroll()
                        self.cb_update_viewers()
        event.accept()


class SSELabel(ViewerQLabel):
    """Main window of smart segmentation editor, inherited from the main viewers"""

    def __init__(
        self,
        viewer_stats,
        cb_update_viewers,
        cb_mouse_moved,
        cb_mouse_pressed,
        cb_mouse_released,
        cb_scroll,
        core,
    ):
        super().__init__(viewer_stats, cb_update_viewers, cb_mouse_moved)
        self.setMouseTracking(True)
        self.viewer_stats = viewer_stats
        self.cb_update_viewers = cb_update_viewers
        self.cb_mouse_moved = cb_mouse_moved
        self.cb_mouse_pressed = cb_mouse_pressed
        self.cb_mouse_released = cb_mouse_released
        self.cb_scroll = cb_scroll
        self.core = core

    @QtCore.pyqtSlot()
    def enterEvent(self, _) -> None:
        QtWidgets.QApplication.setOverrideCursor(Qt.CrossCursor)

    @QtCore.pyqtSlot()
    def leaveEvent(self, _) -> None:
        QtWidgets.QApplication.setOverrideCursor(Qt.ArrowCursor)

    @QtCore.pyqtSlot()
    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        self.cb_mouse_pressed(event)

    @QtCore.pyqtSlot()
    def mouseReleaseEvent(self, _) -> None:
        self.cb_mouse_released()

    @QtCore.pyqtSlot()
    def mouseMoveEvent(self, event: QtGui.QMouseEvent) -> None:
        self.cb_mouse_moved(event)
        event.accept()


class CustomQDockWidget(QtWidgets.QDockWidget):
    """Dock widgets are used for structuring the main window"""

    def __init__(self, viewer_stats, cb_update_viewers, cb_drag_and_drop, cb_qlabel_viewer):
        super().__init__()
        self.viewer_stats = viewer_stats
        self.cb_update_viewers = cb_update_viewers
        self.cb_drag_and_drop = cb_drag_and_drop
        self.cb_qlabel_viewer = cb_qlabel_viewer

        self.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea)
        self.setAllowedAreas(QtCore.Qt.RightDockWidgetArea)
        self.setAllowedAreas(QtCore.Qt.TopDockWidgetArea)
        self.setAllowedAreas(QtCore.Qt.BottomDockWidgetArea)
        self.setContextMenuPolicy(QtCore.Qt.PreventContextMenu)
        self.setFeatures(QtWidgets.QDockWidget.NoDockWidgetFeatures)  # prevents closing and undocking

        self.setFloating(False)
        self.setAcceptDrops(True)
        self.setAutoFillBackground(True)

        # Title bar settings
        self.title_label = QtWidgets.QLabel('', self)
        self.slice_number = QtWidgets.QLabel('', self)

        undock_button = QtWidgets.QToolButton(self)
        undock_button.setIcon(QtGui.QIcon(os.path.join(ICONS_BASE_PATH, 'arrows-maximize.png')))
        undock_button.clicked.connect(self.undock_widget)

        widget = QtWidgets.QWidget()
        css_viewers = """
            QWidget{
                background: #32414B;
                color:  #F0F0F0;
           }
        """
        widget.setStyleSheet(css_viewers)

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.title_label)
        # layout.addStretch()
        layout.addWidget(self.slice_number)
        # layout.addStretch()
        layout.addWidget(undock_button)
        layout.setContentsMargins(0, 0, 0, 0)

        widget.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        widget.setLayout(layout)
        layout.setSpacing(0)
        self.setTitleBarWidget(widget)

    @QtCore.pyqtSlot()
    def undock_widget(self):
        self.viewer_stats.float_widget = CustomQStackedWidget(
            viewer_stats=self.viewer_stats,
            cb_update_viewers=self.cb_update_viewers,
            cb_drag_and_drop=self.cb_drag_and_drop,
        )

        self.viewer_stats.float_widget.setGeometry(
            QtGui.QCursor.pos().x() - 830, QtGui.QCursor.pos().y() + 50, 800, 500
        )

        self.viewer_stats.float_widget.addWidget(self.viewer_stats.qlabel_viewer)
        self.viewer_stats.docked_widget.setFloating(False)
        self.viewer_stats.docked_widget.hide()
        self.viewer_stats.float_widget.show()
        self.set_title_float_widget()

    @QtCore.pyqtSlot()
    def set_title(self, title):
        self.title_label.setText(title)

    @QtCore.pyqtSlot()
    def set_slice_number(self, text=None):
        if text is not None:
            self.slice_number.setText(str(text))
        else:
            self.slice_number.setText(f'{self.viewer_stats.img_index + 1}/{self.viewer_stats.img_index_max}')

    @QtCore.pyqtSlot()
    def set_title_float_widget(self):
        if self.viewer_stats.title:
            self.viewer_stats.float_widget.setWindowTitle(self.viewer_stats.title)
        else:
            self.viewer_stats.float_widget.setWindowTitle('')

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
            first_url = event.mimeData().urls()[0]
            data_path = str(first_url.toLocalFile())
            self.cb_drag_and_drop(data_path)
            self.cb_update_viewers()
        else:
            event.ignore()


class CustomQStackedWidgetSlim(QtWidgets.QStackedWidget):
    """Reduced version, used for the smart segmentation editor"""

    def __init__(self, viewer_stats, cb_update_viewer):
        super().__init__()
        self.viewer_stats = viewer_stats
        self.cb_update_viewer = cb_update_viewer

        self.setWindowIcon(QtGui.QIcon(APP_ICON))
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setAcceptDrops(True)


class CustomQStackedWidget(QtWidgets.QStackedWidget):
    """Are used when the dock widget are undocked"""

    def __init__(self, viewer_stats, cb_update_viewers, cb_drag_and_drop):
        super().__init__()
        self.cb_update_viewers = cb_update_viewers
        self.viewer_stats = viewer_stats
        self.cb_drag_and_drop = cb_drag_and_drop

        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
            first_url = event.mimeData().urls()[0]
            data_path = str(first_url.toLocalFile())
            self.cb_drag_and_drop(data_path)
            self.cb_update_viewers()
        else:
            event.ignore()

    @QtCore.pyqtSlot()
    def closeEvent(self, _):
        self.viewer_stats.docked_widget.setFloating(False)
        self.viewer_stats.docked_widget.show()
        self.viewer_stats.docked_widget.setWidget(self.viewer_stats.qlabel_viewer)
        self.viewer_stats.float_widget.hide()


class CustomSidePanelQDockWidget(QtWidgets.QDockWidget):
    """Left side panel with meta data or other stats"""

    def __init__(self, app):
        super().__init__()

        self.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea)
        self.setAllowedAreas(QtCore.Qt.RightDockWidgetArea)
        self.setAllowedAreas(QtCore.Qt.TopDockWidgetArea)
        self.setAllowedAreas(QtCore.Qt.BottomDockWidgetArea)
        self.setContextMenuPolicy(QtCore.Qt.PreventContextMenu)
        self.setFeatures(QtWidgets.QDockWidget.DockWidgetClosable)
        self.setAutoFillBackground(True)
        self.setAcceptDrops(False)
        self.setFloating(False)
        self.title_label = QtWidgets.QLabel('Meta Data', self)

        widget = QtWidgets.QWidget()
        css_viewers = """
            QWidget{
                background: #32414B;
                color:  #F0F0F0;
            }
        """
        widget.setStyleSheet(css_viewers)

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.title_label)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addStretch()

        close_button = QtWidgets.QToolButton(self)
        close_button.setIcon(QtGui.QIcon(os.path.join(ICONS_BASE_PATH, 'close.png')))

        close_button.clicked.connect(self.hide)
        layout.addWidget(close_button)

        widget.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        widget.setLayout(layout)
        self.setTitleBarWidget(widget)
        screen = app.primaryScreen()
        self.setFixedWidth(int(int(int(QtCore.QRect.width(screen.availableGeometry())) + 1e-9) / 4.5))


class CustomSidePanelQTabWidget(QtWidgets.QTabWidget):
    """For structuring each mri modality in a own tab"""

    def __init__(self):
        super().__init__()
        self.tab_layout = QtWidgets.QGridLayout()
        self.setLayout(self.tab_layout)
        self.setContextMenuPolicy(QtCore.Qt.PreventContextMenu)
        self.setFocusPolicy(QtCore.Qt.NoFocus)


class CustomSidePanelQTableWidget(QtWidgets.QTableWidget):
    """Table widget to structuring meta data"""

    def __init__(self):
        super().__init__()
        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setVisible(False)
        self.setColumnCount(2)
        self.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        # self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        # self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.setContextMenuPolicy(QtCore.Qt.PreventContextMenu)
        self.setFocusPolicy(QtCore.Qt.NoFocus)

        css_viewers = """
            QTableWidget::item:hover {
                background: #19232D;
            }
              """
        self.setStyleSheet(css_viewers)


class UpdatePanelQDockWidget(QtWidgets.QDockWidget):
    """Update widget for showing updates progress"""

    def __init__(self, mw):
        super().__init__()

        self.mw = mw
        self.text_store_model = ''
        self.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea)
        self.setAllowedAreas(QtCore.Qt.RightDockWidgetArea)
        self.setAllowedAreas(QtCore.Qt.TopDockWidgetArea)
        self.setAllowedAreas(QtCore.Qt.BottomDockWidgetArea)
        self.setContextMenuPolicy(QtCore.Qt.PreventContextMenu)
        self.setFeatures(QtWidgets.QDockWidget.DockWidgetClosable)
        self.setAutoFillBackground(True)
        self.setAcceptDrops(False)
        self.setFloating(False)
        self.title_label = QtWidgets.QLabel('Update Client', self)

        widget = QtWidgets.QWidget()
        css_viewers = """
            QWidget{
                background: black;
                color:  #F0F0F0;
                border-color: black;
                }
            """
        widget.setStyleSheet(css_viewers)

        vbox = QtWidgets.QVBoxLayout()
        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(self.title_label)
        hbox.setContentsMargins(0, 0, 0, 0)
        hbox.addStretch()
        self.close_button = QtWidgets.QToolButton(self)
        self.close_button.setIcon(QtGui.QIcon(os.path.join(ICONS_BASE_PATH, 'close_orange.png')))
        self.close_button.hide()
        self.close_button.clicked.connect(self.pushed_close_button)
        hbox.addWidget(self.close_button)

        vbox.addItem(hbox)
        hbox_text = QtWidgets.QHBoxLayout()
        vbox_model = QtWidgets.QVBoxLayout()
        self.text_edit_model = QtWidgets.QTextEdit()
        vbox_model.addWidget(self.text_edit_model)
        hbox_bm = QtWidgets.QHBoxLayout()
        self.button_model_ok = QtWidgets.QPushButton('Update Models')
        self.button_model_ok.setStyleSheet("background-color : green")
        self.button_model_ok.clicked.connect(self.pushed_button_model_ok)
        self.button_model_ok.hide()
        self.button_model_no = QtWidgets.QPushButton('Cancel')
        self.button_model_no.setStyleSheet("background-color : green")
        self.button_model_no.clicked.connect(self.pushed_button_model_no)
        self.button_model_no.hide()
        hbox_bm.addStretch()
        hbox_bm.addWidget(self.button_model_ok)
        hbox_bm.addSpacing(5)
        hbox_bm.addWidget(self.button_model_no)
        hbox_bm.addStretch(100)
        vbox_model.addItem(hbox_bm)
        hbox_text.addItem(vbox_model)

        # Software updater # find_me_17
        # vbox_software = QtWidgets.QVBoxLayout()
        # self.text_edit_software = QtWidgets.QTextEdit()
        # vbox_software.addWidget(self.text_edit_software)
        # hbox_bs = QtWidgets.QHBoxLayout()
        # self.button_software_ok = QtWidgets.QPushButton('Update Software')
        # self.button_software_ok.setFixedWidth(300)
        # self.button_software_ok.setStyleSheet("background-color : green")
        # self.button_software_ok.clicked.connect(self.pushed_button_software_ok)
        # self.button_software_ok.hide()
        # self.button_software_no = QtWidgets.QPushButton('Cancel')
        # self.button_software_no.setStyleSheet("background-color : green")
        # self.button_software_no.clicked.connect(self.pushed_button_software_no)
        # self.button_software_no.hide()
        # hbox_bs.addStretch()
        # hbox_bs.addWidget(self.button_software_ok)
        # hbox_bs.addSpacing(5)
        # hbox_bs.addWidget(self.button_software_no)
        # hbox_bs.addStretch()
        # vbox_software.addItem(hbox_bs)
        # hbox_text.addItem(vbox_software)
        vbox.addItem(hbox_text)

        widget.setLayout(vbox)
        widget.setMinimumHeight(int(self.mw.height() / 2))
        self.setTitleBarWidget(widget)
        self.setMinimumHeight(int(self.mw.height() / 2))
        self.hide()  # default is hidden, only used for updates

    def set_text(self, text, entity):
        # if entity == 'software':
        #     self.text_store_software += text
        #     self.text_edit_software.setText(self.text_store_software)
        if entity == 'model':
            self.text_store_model += text
            self.text_edit_model.setText(self.text_store_model)

    def reset_text_model(self):
        self.text_edit_model.clear()

    def show_model_button(self):
        self.button_model_ok.show()
        self.button_model_no.show()

    def pushed_button_model_ok(self):
        self.button_model_ok.hide()
        self.button_model_no.hide()
        self.text_store_model = ''

    def pushed_button_model_no(self):
        self.button_model_ok.hide()
        self.button_model_no.hide()
        self.close_updater()

    def close_updater(self):
        if self.button_model_no.isHidden():
            self.hide()
            self.mw.mw_toolbar.enable()
            self.mw.mw_menu.enable()

    def show_close_button(self):
        self.close_button.show()

    def pushed_close_button(self):
        self.hide()
        self.mw.mw_toolbar.enable()
        self.mw.mw_menu.enable()

    def disable_main(self):
        self.mw.mw_toolbar.disable()
        self.mw.mw_menu.disable()
        self.mw.mw_viewers.update_widget.show()

    def enable_main(self):
        self.mw.mw_toolbar.disable()
        self.mw.mw_menu.disable()
        self.mw.mw_viewers.update_widget.show()
