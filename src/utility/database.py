import pandas
import psycopg2


class MetaSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(MetaSingleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class DatabasePostgres(metaclass=MetaSingleton):
    connection = None
    connection_string = None

    def __init__(self):
        self.cursor = None

    def __del__(self):
        if self.cursor:
            self.cursor.close()

    def connect(self):
        if self.connection is None:
            # self.connection = psycopg2.connect(dbname='inter_annotation_db', user='eval_quorum',
            #                                    password='eval_quorum', host='192.168.10.36')
            self.connection = psycopg2.connect(self.connection_string)
            self.cursor = self.connection.cursor()
        return self.cursor


class DatabaseCsvFile(metaclass=MetaSingleton):
    _data_frame = None
    file_path = None

    @property
    def data_frame(self):
        if self._data_frame is None:
            self._data_frame = pandas.read_csv(self.file_path, header=0)
            spans = self._data_frame[['tag_name', 'start_token', 'length']].drop_duplicates()
            spans = spans.reset_index().rename(columns={'index': 'span_id'})
            self._data_frame = pandas.merge(self._data_frame, spans, how='inner')
            self._data_frame = self._data_frame[['entity_id', 'user_id', 'par_id', 'span_id']]
            self._data_frame = self._data_frame.sort_values('entity_id')
        return self._data_frame
