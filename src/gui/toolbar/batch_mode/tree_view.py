import os

from PyQt5 import QtCore, QtGui, QtWidgets

from src.core.configs.static_params import USED_MODALITY_NAMES
from src.path_library import ICONS_BASE_PATH


class StandardItem(QtGui.QStandardItem):
    """Inherit from QStandardItem and added some new default settings"""

    def __init__(self, *args):
        super().__init__(*args)
        self.setEditable(False)
        self.setCheckable(False)
        self.setSelectable(False)


class BMTreeView(QtWidgets.QTreeView):
    """Creates tree view with found cases for the batch loader gui"""

    def __init__(self, case_paths):
        super().__init__()
        self.case_paths = case_paths

        self.table_width = None
        self.model = QtGui.QStandardItemModel()
        column_labels = ['Cases', 'States', 'Paths']
        self.model.setHorizontalHeaderLabels(column_labels)
        self.root_node = self.model.invisibleRootItem()
        self.setModel(self.model)
        self.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)

        css = """
            QTreeView {
                border: 1px solid #32414B;
                padding: 0px;
            }
            QTreeView::item:hover {
                background-color: #19232D;
            }
            QTreeView::item:selected {
                background-color: #19232D;
            }
        """
        self.setStyleSheet(css)

        expand_indexes = []
        for case_index, case_name in enumerate(case_paths):
            sub_tree = StandardItem(case_name)
            for modality in USED_MODALITY_NAMES:  # Set check, uncheck, or ignore for expected input sequence
                item = StandardItem('')
                if 'seg_mask' == modality:
                    continue
                if case_paths[case_name][modality]['completeness_check_tag'] == 'yes':
                    child_1 = StandardItem(modality.capitalize())
                    item.setIcon(QtGui.QIcon(os.path.join(ICONS_BASE_PATH, 'check.png')))
                    child_2 = StandardItem(item)
                    child_3 = StandardItem(case_paths[case_name][modality]['file_path'])
                    child_3.setTextAlignment(QtCore.Qt.AlignLeft)
                elif case_paths[case_name][modality]['completeness_check_tag'] == 'no':
                    child_1 = StandardItem(modality.capitalize())
                    item.setIcon(QtGui.QIcon(os.path.join(ICONS_BASE_PATH, 'uncheck.png')))
                    child_2 = StandardItem(item)
                    child_3 = StandardItem('No valid path or missing sequence | This subject will be exclude')
                    child_3.setTextAlignment(QtCore.Qt.AlignLeft)
                    expand_indexes.append(case_index)
                else:
                    child_1 = StandardItem(modality)
                    item.setIcon(QtGui.QIcon(os.path.join(ICONS_BASE_PATH, 'minus.png')))
                    child_2 = StandardItem(item)
                    child_3 = StandardItem(case_paths[case_name][modality]['file_path'])
                    child_3.setTextAlignment(QtCore.Qt.AlignLeft)
                sub_tree.appendRow([child_1, child_2, child_3])
            self.root_node.appendRow(sub_tree)

            for expand_index in set(expand_indexes):  # Expand tree view where data is missing
                self.expand(self.model.index(expand_index, 0))

        for column_index in range(len(column_labels)):  # Some optical tweaking
            self.resizeColumnToContents(column_index)
            self.adjustSize()
            self.setColumnWidth(column_index, self.columnWidth(column_index))
        self.adjustSize()
