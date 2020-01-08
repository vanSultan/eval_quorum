from PyQt5.QtCore import Qt

from main_view import MainView


class MainController:
    def __init__(self):
        self.c_view = MainView(self)
        self.c_view.show()

    def update_limits(self, state: int, begin_index: int = None, end_index: int = None):
        """
        Обновление пределов корпуса
        :param state: Состояние флага выбора всего корпуса
        :param begin_index: начальный индекс выбранных границ
        :param end_index: конечный индекс выбранных границ
        :return: None
        """
        # 0 - Qt::Unchecked, 2 - Qt::Checked
        state = False if state == 0 else True

        # Смена доступности изменения периода
        self.c_view.ui.spinBoxBeginLimit.setEnabled(not state)
        self.c_view.ui.spinBoxEndLimit.setEnabled(not state)

        table_model = self.c_view.ui.tableView.model()

        begin_limit = end_limit = 0

        if state:  # Если флаг установлен
            begin_limit, end_limit = table_model.limits
        elif begin_index and end_index:  # Если флаг не установлен и в таблицы выбраны пределы
            begin_limit = int(table_model.data(table_model.index(begin_index, 0), Qt.DisplayRole))
            if end_index == -1:
                end_limit = self.c_view.ui.spinBoxEndLimit.value()
            else:
                end_limit = int(table_model.data(table_model.index(end_index, 0), Qt.DisplayRole))

            if end_limit < begin_limit:
                end_limit = begin_limit

        if state or begin_index and end_index:
            self.c_view.ui.spinBoxBeginLimit.setValue(begin_limit)
            self.c_view.ui.spinBoxEndLimit.setValue(end_limit)

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
        self.update_limits(self.c_view.ui.checkBoxNoLimit.checkState())

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

    def load_data_from_csv(self, filename: str = 'spans.csv', sep: str = ','):
        from database import Database
        cursor = Database().connect()

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
        Database().connection.commit()
