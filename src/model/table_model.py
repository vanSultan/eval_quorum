import typing

from PyQt5.QtCore import QAbstractTableModel, QModelIndex, Qt

from table_storage import TableStorage


class TableModel(QAbstractTableModel):
    def __init__(self, row_offset: int = 0, row_count: int = 50, storage: TableStorage = None, table_data: list = None):
        super().__init__()
        self.table_data = table_data if table_data else []
        self._row_offset = row_offset
        self._row_count = row_count
        self._storage = storage if storage else TableStorage(self._row_offset, self._row_count)

    def rowCount(self, parent: QModelIndex = ...) -> int:
        return len(self.table_data)

    def columnCount(self, parent: QModelIndex = ...) -> int:
        return len(self.table_data[0]) if self.rowCount() > 0 else 0

    def data(self, index: QModelIndex, role: int = ...) -> typing.Any:
        if not index.isValid() or role != Qt.DisplayRole:
            return None
        value = self.table_data[index.row()][index.column()]
        return str(value)

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...) -> typing.Any:
        if role != Qt.DisplayRole:
            return None

        name = None
        if orientation == Qt.Horizontal:
            if section == 0:
                name = 'idVolSpan'
            elif section == 1:
                name = 'idVolunteer'
            elif section == 2:
                name = 'idSection'
            elif section == 3:
                name = 'idSpan'
        elif orientation == Qt.Vertical:
            name = str(section)

        return name

    def update_properties(self, new_offset: int, new_count: int):
        self._storage.row_offset = self._row_offset = new_offset
        self._storage.row_count = self._row_count = new_count

        self.beginResetModel()
        self.table_data = self._storage.get_table()
        self.endResetModel()

        # self.layoutChanged.emit()

    @property
    def row_total(self):
        return self._storage.get_total_count()

    @property
    def limits(self):
        return self._storage.get_limits()
