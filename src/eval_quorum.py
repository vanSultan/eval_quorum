import argparse
import os
import sys

from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication

from database import DatabasePostgres, DatabaseCsvFile
from main_controller import MainController


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--connection_string', '-c', type=str,
                        help='postgresql://[user[:password]@][netloc][:port][,...][/dbname][?param1=value1&...]')
    parser.add_argument('--file_path', '-f', type=str, help='Путь к csv файлу')

    return parser.parse_args()


def main():
    args = get_args()
    data_source = None

    if not args.connection_string and not args.file_path:
        print('Не указан источник данных')
    elif args.connection_string:
        DatabasePostgres.connection_string = args.connection_string
        data_source = True
        print('Используется подключение к бд')
    else:
        DatabaseCsvFile.file_path = args.file_path
        data_source = False
        print('Используется csv файл с данными')

    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"

    app = QApplication(sys.argv)
    app.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)

    controller = MainController(data_source)

    app.exec()


if __name__ == '__main__':
    sys.exit(main())
