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
        self.ui.checkBoxAllPeriod.stateChanged.connect(self.v_controller.all_period_change_state)
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
        begin_period = self.ui.dateTimeBeginPeriod.dateTime().toPyDateTime()
        end_period = self.ui.dateTimeEndPeriod.dateTime().toPyDateTime()
        id_section = int(self.ui.spinBoxSection.text())

        self.v_controller.eval_section(id_section, begin_period, end_period)

    def click_eval_volunteer(self):
        begin_period = self.ui.dateTimeBeginPeriod.dateTime().toPyDateTime()
        end_period = self.ui.dateTimeEndPeriod.dateTime().toPyDateTime()
        id_volunteer = int(self.ui.spinBoxVolunteer.text())

        self.v_controller.eval_volunteer(id_volunteer, begin_period, end_period)

    def click_eval_frame(self):
        begin_period = self.ui.dateTimeBeginPeriod.dateTime().toPyDateTime()
        end_period = self.ui.dateTimeEndPeriod.dateTime().toPyDateTime()

        self.v_controller.eval_frame(begin_period, end_period)
