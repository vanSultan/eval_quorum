from PyQt5.QtCore import Qt

from model.eval_model import EvalFrameModelSql, EvalFrameModelPandas, EvalVolunteerModelPandas, EvalSectionModelPandas, \
    EvalVolunteerModelSql, EvalSectionModelSql
from view.main_view import MainView
from model.table_model import TableModelSql, TableModelPandas


class MainController:
    def __init__(self, data_source: bool = False):
        """
        :param data_source: if True - из бд, else - из файла
        """
        self._data_source = data_source
        self.c_view = MainView(self)

        # Привязка отображения таблицы к ее модели
        self.c_view.ui.tableView.setModel(TableModelSql() if self._data_source else TableModelPandas())

        self.animation = None

        self.c_view.show()

    def change_state_no_limits(self, state: int):
        """
        Смена состояния флага "весь корпус или нет"
        :param state: Состояние флага выбора всего корпуса
        :return: None
        """
        # 0 - Qt::Unchecked, 2 - Qt::Checked
        state = False if state == 0 else True

        # Смена доступности изменения периода
        self.c_view.ui.spinBoxBeginLimit.setEnabled(not state)
        self.c_view.ui.spinBoxEndLimit.setEnabled(not state)

        table_model = self.c_view.ui.tableView.model()

        if state:  # Если флаг установлен
            begin_limit, end_limit = table_model.limits

            self.c_view.ui.spinBoxBeginLimit.setValue(begin_limit)
            self.c_view.ui.spinBoxEndLimit.setValue(end_limit)

    def change_state_fixed_limit(self, state: int):
        state = False if state == 0 else True

        self.c_view.ui.checkBoxNoLimit.setEnabled(not state)
        if not self.c_view.ui.checkBoxNoLimit.checkState():
            self.c_view.ui.spinBoxBeginLimit.setEnabled(not state)
            self.c_view.ui.spinBoxEndLimit.setEnabled(not state)
        else:
            self.change_state_no_limits(self.c_view.ui.checkBoxNoLimit.checkState())

    def change_state_fixed_section(self, state: int):
        state = False if state == 0 else True

        self.c_view.ui.spinBoxSection.setEnabled(not state)

    def change_state_fixed_volunteer(self, state: int):
        state = False if state == 0 else True

        self.c_view.ui.spinBoxVolunteer.setEnabled(not state)

    def click_table(self, begin_index: int, end_index: int = None):
        """
        Контроллер нажатия на таблицу, обрабатывает заполнение полей интерфейса
        :param begin_index: начальный индекс выделенных строк
        :param end_index: конечный индекс выделенных строк(если нет, то -1)
        :return: None
        """
        # Контроллер перегружен - знаю.
        table_model = self.c_view.ui.tableView.model()

        # Обработка выбора границ
        state = False if self.c_view.ui.checkBoxFixedLimit.checkState() == 0 else True
        if not state:
            begin_limit = int(table_model.data(table_model.index(begin_index, 0), Qt.DisplayRole))
            if end_index == -1:
                end_limit = self.c_view.ui.spinBoxEndLimit.value()
            else:
                end_limit = int(table_model.data(table_model.index(end_index, 0), Qt.DisplayRole))

            if end_limit < begin_limit:
                end_limit = begin_limit

            self.c_view.ui.spinBoxBeginLimit.setValue(begin_limit)
            self.c_view.ui.spinBoxEndLimit.setValue(end_limit)

        # Обработка выбора абзаца
        state = False if self.c_view.ui.checkBoxFixedSection.checkState() == 0 else True
        if not state:
            section_id = int(table_model.data(table_model.index(begin_index, 2), Qt.DisplayRole))
            self.c_view.ui.spinBoxSection.setValue(section_id)

        # Обработка выбора волонтера
        state = False if self.c_view.ui.checkBoxFixedVolunteer.checkState() == 0 else True
        if not state:
            volunteer_id = int(table_model.data(table_model.index(begin_index, 1), Qt.DisplayRole))
            self.c_view.ui.spinBoxVolunteer.setValue(volunteer_id)

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

        # Выводим общее количество записей
        # Нужно ли это делать при каждом обновлении отображения или достаточно одного раза? - хз
        self.c_view.ui.lineEditRowTotal.setText(str(table_model.row_total))

        # Обновляем границы, при условии, что прожат полного корпуса
        self.change_state_no_limits(self.c_view.ui.checkBoxNoLimit.checkState())

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
        self.c_view.ui.tabWidget.repaint()
        self.c_view.ui.tabEvalPlot.repaint()

        if self._data_source:
            self.c_view.evalPlotView.model = EvalSectionModelSql(id_section, begin_limit, end_limit)
        else:
            self.c_view.evalPlotView.model = EvalSectionModelPandas(id_section, begin_limit, end_limit)

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
        self.c_view.ui.tabWidget.repaint()
        self.c_view.ui.tabEvalPlot.repaint()

        if self._data_source:
            self.c_view.evalPlotView.model = EvalVolunteerModelSql(id_volunteer, begin_limit, end_limit)
        else:
            self.c_view.evalPlotView.model = EvalVolunteerModelPandas(id_volunteer, begin_limit, end_limit)

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
        self.c_view.ui.tabWidget.repaint()
        self.c_view.ui.tabEvalPlot.repaint()

        if self._data_source:
            self.c_view.evalPlotView.model = EvalFrameModelSql(begin_limit, end_limit)
        else:
            self.c_view.evalPlotView.model = EvalFrameModelPandas(begin_limit, end_limit)

        self.c_view.ui.statusbar.showMessage(f'Begin: {begin_limit}\tEnd: {end_limit}')

    def load_data_from_csv(self, filename: str = 'spans.csv', sep: str = ','):
        from database import DatabasePostgres
        cursor = DatabasePostgres().connect()

        with open(filename) as f_src:
            records = f_src.readlines()[1:]  # Первая строка - заголовок

        total = len(records)
        current = 0
        step = 50

        sections = set()
        volunteers = set()
        spans = set()
        vol_sec = set()
        vol_span = set()

        for rec in records:
            rec = rec.strip('\n')
            rec = rec.split(sep)

            # par_id,user_id,entity_id,tag_name,start_token,length
            section_id = rec[0]
            volunteer_id = rec[1]
            tag_name = rec[3]
            start_token = rec[4]
            length = rec[5]

            sections.add(section_id)
            volunteers.add(volunteer_id)
            spans.add(f'{section_id}{sep}{tag_name}{sep}{start_token}{sep}{length}')
            vol_sec.add(f'{volunteer_id}{sep}{section_id}')
            vol_span.add(f'{volunteer_id}{sep}{section_id}{sep}{tag_name}{sep}{start_token}{sep}{length}')

            current += 1
            if current % step == 0 or total - current < step:
                self.c_view.ui.statusbar.showMessage(f'Records: left={total - current}; current={current}')
                self.c_view.ui.statusbar.repaint()

        total = len(sections)
        current = 0
        for section in sections:
            cursor.execute(f"""
                insert into section (id_section) values ({section})
            """)
            current += 1
            if current % step == 0 or total - current < step:
                self.c_view.ui.statusbar.showMessage(f'Sections: left={total - current}; current={current}')
                self.c_view.ui.statusbar.repaint()

        total = len(volunteers)
        current = 0
        for volunteer in volunteers:
            cursor.execute(f"""
                insert into volunteer (id_volunteer) values ({volunteer})
            """)
            current += 1
            if current % step == 0 or total - current < step:
                self.c_view.ui.statusbar.showMessage(f'Volunteers: left={total - current}; current={current}')
                self.c_view.ui.statusbar.repaint()

        total = len(spans)
        current = 0
        for rec in spans:
            rec = rec.split(sep)
            cursor.execute(f"""
                insert into span (section_id, tag_name, start_token, length)
                values ({rec[0]}, '{rec[1]}', {rec[2]}, {rec[3]})
            """)
            current += 1
            if current % step == 0 or total - current < step:
                self.c_view.ui.statusbar.showMessage(f'Spans: left={total - current}; current={current}')
                self.c_view.ui.statusbar.repaint()

        total = len(vol_sec)
        current = 0
        for rec in vol_sec:
            rec = rec.split(sep)
            cursor.execute(f"""
                insert into volunteer_section (volunteer_id, section_id) values ({rec[0]}, {rec[1]})
            """)
            current += 1
            if current % step == 0 or total - current < step:
                self.c_view.ui.statusbar.showMessage(f'VolSec: left={total - current}; current={current}')
                self.c_view.ui.statusbar.repaint()

        total = len(vol_span)
        current = 0
        for rec in vol_span:
            rec = rec.split(sep)

            cursor.execute(f"""
                select id_span from span
                where section_id = {rec[1]} and tag_name = '{rec[2]}' and start_token = {rec[3]} and length = {rec[4]}
            """)
            span_id = cursor.fetchone()[0]

            cursor.execute(f"""
                insert into volunteer_span (volunteer_id, span_id) values ({rec[0]}, {span_id})
            """)
            current += 1
            if current % step == 0 or total - current < step:
                self.c_view.ui.statusbar.showMessage(f'VolSpan: left={total - current}; current={current}')
                self.c_view.ui.statusbar.repaint()

        cursor.close()
        DatabasePostgres().connection.commit()
