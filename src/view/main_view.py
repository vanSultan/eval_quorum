from PyQt5.QtWidgets import QMainWindow

from eval_plot_view import EvalPlot
from table_model import TableModel
from ui_main_widget import Ui_MainWindow


class MainView(QMainWindow):
    def __init__(self, controller, parent=None):
        super(QMainWindow, self).__init__(parent)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.v_controller = controller

        # Привязка событий к функциям
        self.ui.checkBoxNoLimit.stateChanged.connect(self.v_controller.no_limit_change_state)
        self.ui.pushButtonUpdateView.clicked.connect(self.click_update_table_view)
        self.ui.pushButtonEvalSection.clicked.connect(self.click_eval_section)
        self.ui.pushButtonEvalVolunteer.clicked.connect(self.click_eval_volunteer)

        # Привязка отображения таблицы к ее модели
        self.ui.tableView.setModel(TableModel(0, 0))
        self.ui.tableView.horizontalHeader().setSectionResizeMode(1)  # Таблица заполняет все пространство

        # Инициализация диграммы для оценки
        self.evaPlotView = EvalPlot(parent=self.ui.tabEvalPlot)
        self.ui.vLayoutEvalPlot.addWidget(self.evaPlotView)

    def click_update_table_view(self):
        row_offset = int(self.ui.spinBoxRowOffset.text())
        row_count = int(self.ui.spinBoxRowCount.text())

        self.v_controller.update_table_view(row_offset, row_count)

    def click_eval_section(self):
        begin_limit = int(self.ui.spinBoxBeginLimit.text())
        end_limit = int(self.ui.spinBoxEndLimit.text())
        id_section = int(self.ui.spinBoxSection.text())

        self.v_controller.eval_section(id_section, begin_limit, end_limit)

    def click_eval_volunteer(self):
        begin_limit = int(self.ui.spinBoxBeginLimit.text())
        end_limit = int(self.ui.spinBoxEndLimit.text())
        id_volunteer = int(self.ui.spinBoxVolunteer.text())

        self.v_controller.eval_volunteer(id_volunteer, begin_limit, end_limit)

    def click_eval_frame(self):
        begin_limit = int(self.ui.spinBoxBeginLimit.text())
        end_limit = int(self.ui.spinBoxEndLimit.text())

        self.v_controller.eval_frame(begin_limit, end_limit)
