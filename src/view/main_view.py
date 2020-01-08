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
        self.ui.checkBoxNoLimit.stateChanged.connect(self.v_controller.update_limits)
        self.ui.pushButtonUpdateView.clicked.connect(self.click_update_table_view)
        self.ui.pushButtonEvalSection.clicked.connect(self.click_eval_section)
        self.ui.pushButtonEvalVolunteer.clicked.connect(self.click_eval_volunteer)
        self.ui.pushButtonEvalFrame.clicked.connect(self.click_eval_frame)
        self.ui.tableView.clicked.connect(self.click_table_view)

        # Привязка отображения таблицы к ее модели
        self.ui.tableView.setModel(TableModel(0, 0))
        self.ui.tableView.horizontalHeader().setSectionResizeMode(1)  # Таблица заполняет все пространство

        # Инициализация диграммы для оценки
        self.evaPlotView = EvalPlot(parent=self.ui.tabEvalPlot)
        self.ui.vLayoutEvalPlot.addWidget(self.evaPlotView)

        # Инициализация некоторых параметров
        self.ui.spinBoxRowCount.setValue(50)

    def click_update_table_view(self):
        row_offset = self.ui.spinBoxRowOffset.value()
        row_count = self.ui.spinBoxRowCount.value()

        self.v_controller.update_table_view(row_offset, row_count)
        # self.v_controller.load_data_from_csv()

    def click_eval_section(self):
        begin_limit = self.ui.spinBoxBeginLimit.value()
        end_limit = self.ui.spinBoxEndLimit.value()
        id_section = self.ui.spinBoxSection.value()

        self.v_controller.eval_section(id_section, begin_limit, end_limit)

    def click_eval_volunteer(self):
        begin_limit = self.ui.spinBoxBeginLimit.value()
        end_limit = self.ui.spinBoxEndLimit.value()
        id_volunteer = self.ui.spinBoxVolunteer.value()

        self.v_controller.eval_volunteer(id_volunteer, begin_limit, end_limit)

    def click_eval_frame(self):
        begin_limit = self.ui.spinBoxBeginLimit.value()
        end_limit = self.ui.spinBoxEndLimit.value()

        self.v_controller.eval_frame(begin_limit, end_limit)

    def click_table_view(self):
        selected = self.ui.tableView.selectedIndexes()

        begin_index = selected[0].row()
        if len(selected) == 1:
            end_index = -1
        else:
            end_index = selected[-1].row()

        self.v_controller.update_limits(self.ui.checkBoxNoLimit.checkState(), begin_index, end_index)
