from PyQt5.QtWidgets import QMainWindow

from eval_plot_view import EvalPlot
from ui_main_widget import Ui_MainWindow


class MainView(QMainWindow):
    def __init__(self, controller, parent=None):
        super(QMainWindow, self).__init__(parent)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.v_controller = controller

        # Привязка событий к функциям
        self.ui.checkBoxNoLimit.stateChanged.connect(self.v_controller.change_state_no_limits)
        self.ui.checkBoxFixedLimit.stateChanged.connect(self.v_controller.change_state_fixed_limit)
        self.ui.checkBoxFixedSection.stateChanged.connect(self.v_controller.change_state_fixed_section)
        self.ui.checkBoxFixedVolunteer.stateChanged.connect(self.v_controller.change_state_fixed_volunteer)
        self.ui.pushButtonUpdateView.clicked.connect(self.click_update_table_view)
        self.ui.pushButtonEvalSection.clicked.connect(self.click_eval_section)
        self.ui.pushButtonEvalVolunteer.clicked.connect(self.click_eval_volunteer)
        self.ui.pushButtonEvalFrame.clicked.connect(self.click_eval_frame)
        self.ui.tableView.clicked.connect(self.click_table_view)

        self.ui.tableView.horizontalHeader().setSectionResizeMode(1)  # Таблица заполняет все пространство

        # Инициализация диграммы для оценки
        self.evalPlotView = EvalPlot(parent=self.ui.tabEvalPlot)
        self.ui.vLayoutEvalPlot.addWidget(self.evalPlotView)

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

        if not self.ui.checkBoxNoLimit.isChecked() and not self.ui.checkBoxFixedLimit.isChecked():
            self.v_controller.click_table(begin_index, end_index)
