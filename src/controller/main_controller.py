from main_view import MainView


class MainController:
    def __init__(self):
        self.c_view = MainView(self)
        self.c_view.show()

    def no_limit_change_state(self, state: int):
        """
        Обработка установки/сброса флага выбора всего периода
        :param state: Состояние флага
        :return: None
        """
        # 0 - Qt::Unchecked, 2 - Qt::Checked
        state = False if state == 0 else True

        # Смена доступности изменения периода
        self.c_view.ui.spinBoxBeginLimit.setEnabled(not state)
        self.c_view.ui.spinBoxEndLimit.setEnabled(not state)

    def update_table_view(self, row_offset: int, row_count: int):
        """
        Обновление таблицы с данными
        :param row_offset: смещние строк
        :param row_count: количество строк для отображения
        :return: None
        """
        # Переключаемся на вкладку с таблицей
        self.c_view.ui.tabWidget.setCurrentIndex(0)

        table_model = self.c_view.ui.tableView.model()
        table_model.update_properties(row_offset, row_count)

        self.c_view.ui.statusbar.showMessage(f'Offset: {row_offset}\tCount: {row_count}')

    def eval_section(self, id_section: int, begin_limit: int, end_limit: int):
        """
        Оценка абзаца
        :param id_section: id абзаца
        :param begin_limit: начало границы
        :param end_limit: конец границы
        :return: None
        """
        # Переключаемся на вкладку с диаграммой
        self.c_view.ui.tabWidget.setCurrentIndex(1)

        # TODO попросить у модели оценку
        # TODO отобразить оценку

        self.c_view.ui.statusbar.showMessage(f'IdSection: {id_section}\tBegin: {begin_limit}\tEnd: {end_limit}')

    def eval_volunteer(self, id_volunteer: int, begin_limit: int, end_limit: int):
        """
        Оценка волонтера
        :param id_volunteer: id абзаца
        :param begin_limit: начало границы
        :param end_limit: конец границы
        :return: None
        """
        # Переключаемся на вкладку с диаграммой
        self.c_view.ui.tabWidget.setCurrentIndex(1)

        # TODO попросить у модели оценку
        # TODO отобразить оценку

        self.c_view.ui.statusbar.showMessage(f'IdVolunteer: {id_volunteer}\tBegin: {begin_limit}\tEnd: {end_limit}')

    def eval_frame(self, begin_limit: int, end_limit: int):
        """
        Оценка корпуса
        :param begin_limit: начало границы
        :param end_limit: конец границы
        :return: None
        """
        # Переключаемся на вкладку с диаграммой
        self.c_view.ui.tabWidget.setCurrentIndex(1)

        # TODO попросить у модели оценку
        # TODO отобразить оценку

        self.c_view.ui.statusbar.showMessage(f'Begin: {begin_limit}\tEnd: {end_limit}')
