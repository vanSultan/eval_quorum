from PyQt5.QtWidgets import QMainWindow

from ui_main_widget import Ui_MainWindow


class MainView(QMainWindow):
    def __init__(self, controller, parent=None):
        super(QMainWindow, self).__init__(parent)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.v_controller = controller
