
from PySide2.QtCore import QAbstractTableModel
from PySide2.QtGui import Qt


class TableModel(QAbstractTableModel):

    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            return self._data[index.row()][index.column()]

    def rowCount(self, index):
        try:
            len(self._data) == 0
        except IndexError as e:
            return 0
        return len(self._data)

    def columnCount(self, index):
        try:
            len(self._data[0]) == 0
        except IndexError as e:
            return 0
        return len(self._data[0])
