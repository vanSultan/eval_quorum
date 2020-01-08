import psycopg2


class MetaSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(MetaSingleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Database(metaclass=MetaSingleton):
    connection = None

    def __init__(self):
        self.cursor = None

    def connect(self):
        if self.connection is None:
            self.connection = psycopg2.connect(dbname='inter_annotation_db', user='eval_quorum',
                                               password='eval_quorum', host='192.168.10.36')
            self.cursor = self.connection.cursor()
        return self.cursor
