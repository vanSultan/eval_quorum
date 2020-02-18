import typing
from abc import abstractmethod

from PyQt5.QtCore import QAbstractTableModel, QModelIndex, Qt

from utility.database import DatabasePostgres, DatabaseCsvFile


class TableModel(QAbstractTableModel):
    def __init__(self, row_offset: int = 0, row_count: int = 50, table_data: list = None):
        super().__init__()
        self.table_data = table_data if table_data else []
        self._row_offset = row_offset
        self._row_count = row_count

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
        self._row_offset = new_offset
        self._row_count = new_count

        self.beginResetModel()
        self.table_data = self._get_data()
        self.endResetModel()

    @abstractmethod
    def _get_data(self) -> list:
        pass

    @property
    @abstractmethod
    def row_total(self) -> int:
        pass

    @property
    @abstractmethod
    def limits(self) -> tuple:
        pass


class TableModelSql(TableModel):
    def __init__(self, *args, **kwargs):
        self._connection = DatabasePostgres()
        self._cursor = self._connection.connect()
        super().__init__(*args, **kwargs)

    def _get_data(self) -> list:
        request = f"""
            select id_vol_span, volunteer_id, section_id, span_id 
            from volunteer_span 
            inner join span s 
            on volunteer_span.span_id = s.id_span
            order by id_vol_span
            offset {self._row_offset} limit {self._row_count}
        """
        self._cursor.execute(request)

        return self._cursor.fetchall()

    @property
    def row_total(self) -> int:
        request = """
            select count(id_vol_span) 
            from volunteer_span
        """
        self._cursor.execute(request)

        return self._cursor.fetchone()[0]

    @property
    def limits(self) -> tuple:
        request = """
            select min(id_vol_span), max(id_vol_span)
            from volunteer_span
        """
        self._cursor.execute(request)

        return self._cursor.fetchone()


class TableModelPandas(TableModel):
    def __init__(self, *args, **kwargs):
        self._connection = DatabaseCsvFile()
        self._data_frame = self._connection.data_frame
        super().__init__(*args, **kwargs)

    def _get_data(self) -> list:
        temp = self._data_frame[self._row_offset:self._row_offset + self._row_count].to_numpy()
        return [tuple(rec) for rec in temp]

    @property
    def row_total(self) -> int:
        return self._data_frame['entity_id'].count()

    @property
    def limits(self) -> tuple:
        return self._data_frame['entity_id'].min(), self._data_frame['entity_id'].max()
