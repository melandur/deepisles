from loguru import logger
from PyQt5 import QtCore, QtWidgets

from src.core.configs.static_params import USED_MODALITY_NAMES
from src.gui.viewers.custom_view import (
    CustomSidePanelQTableWidget,
    CustomSidePanelQTabWidget,
)


class MetaDataUpdater(QtWidgets.QMainWindow):
    """Gets meta data from data handler and shows it in the viewer"""

    def __init__(self, data_handler, viewer_stats):
        super().__init__()
        self.data_handler = data_handler
        self.viewer_stats = viewer_stats
        self.tab_widget = None
        logger.info('Init Meta Data Updater')

    @logger.catch
    def _get_meta_data(self):
        """Create meta data keys list"""
        modality_meta_store = {}
        for modality in USED_MODALITY_NAMES:
            if modality == 'seg_mask':
                continue
            if self.data_handler[f'{modality}_ephemeral_meta'] is not None:
                modality_meta_store[modality] = self.data_handler[f'{modality}_ephemeral_meta']
        return modality_meta_store

    @logger.catch
    def show_meta_data(self, state):
        """Creates for each modality a tab which holds the meta data in table form"""
        self.tab_widget = CustomSidePanelQTabWidget()
        self.viewer_stats.left_panel_widget.setWidget(self.tab_widget)
        modality_meta_store = self._get_meta_data()
        table_widget_store = []
        if modality_meta_store is not None:
            for modality in modality_meta_store:
                table_widget = CustomSidePanelQTableWidget()
                if self.data_handler.get_from_lasting_store(f'{modality}_{state}_meta'):
                    number_of_keys = len(self.data_handler.get_from_lasting_store(f'{modality}_{state}_meta').keys())
                    table_widget.setRowCount(number_of_keys)

                    index = 0
                    for key, value in self.data_handler.get_from_lasting_store(f'{modality}_{state}_meta').items():
                        item = QtWidgets.QTableWidgetItem(key)
                        item.setFlags(QtCore.Qt.ItemIsEnabled)
                        table_widget.setItem(index, 0, item)
                        item = QtWidgets.QTableWidgetItem(str(value))
                        item.setFlags(QtCore.Qt.ItemIsEnabled)
                        table_widget.setItem(index, 1, item)
                        index += 1

                    table_widget.resizeColumnsToContents()
                    table_widget.resizeRowsToContents()
                    table_widget.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)

                    table_widget_store.append(table_widget)

            for table, modality in zip(table_widget_store, modality_meta_store):
                tab_name = modality.split('_')[0].capitalize()
                self.tab_widget.addTab(table, tab_name)
                self.tab_widget.setTabPosition(0)
