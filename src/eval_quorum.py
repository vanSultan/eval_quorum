import os
import sys

from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication

from main_controller import MainController


def main():
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"

    app = QApplication(sys.argv)
    app.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)

    MainController()

    app.exec()


if __name__ == '__main__':
    sys.exit(main())
