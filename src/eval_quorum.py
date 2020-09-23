import os
import sys
from datetime import datetime

from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlQueryModel, QSqlDatabase
from PyQt5.QtWidgets import QApplication, QMainWindow, QHeaderView, QSizePolicy, QComboBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from main_window import Ui_MainWindow
from utility.database import DatabaseSqlite


class PlotCanvas(FigureCanvas):
    def __init__(self, data, title, labels=None, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        self._labels = labels
        self._data = data if data else list()
        self._title = title

        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.plot()

    def plot(self):
        w, _, _ = self.axes.pie(
            self._data, colors=['#2ca02c', '#1f77b4', '#ff7f0e', '#d62728'], radius=1.25, textprops={'fontsize': 9},
            autopct=lambda pct: f'{int(pct / 100 * sum(self._data))}\n({round(pct, 2)}%)',
        )
        self.axes.set_title(self._title, fontsize=12)

        if self._labels:
            self.axes.legend(w, self._labels, loc='center left', fontsize='small',
                             title='Категории:', title_fontsize='medium', bbox_to_anchor=(1, 0.5))
            self.fig.subplots_adjust(left=0.0, bottom=0.1, right=0.45)
        self.draw()


class RatingTableModel(QSqlQueryModel):
    def __init__(self, database: QSqlQueryModel, report_id: int = -1, parent=None):
        super().__init__(parent)
        self.db = database
        self.report_id = report_id
        self.update_table(report_id)

    def update_table(self, report_id: int):
        self.report_id = report_id

        if self.report_id > -1:
            self.setQuery(f'''
                select dense_rank() over (order by score desc) rank,
                    id_volunteer, round(score, 2) score
                from report_volunteer
                where id_report = {self.report_id}
                order by rank
            ''', self.db)

        self.setHeaderData(0, Qt.Horizontal, 'Position')
        self.setHeaderData(1, Qt.Horizontal, 'Volunteer ID')
        self.setHeaderData(2, Qt.Horizontal, 'Score')


class MainTableModel(QSqlQueryModel):
    def __init__(self, database: QSqlDatabase, parent=None):
        super().__init__(parent)
        self.db = database

        con = DatabaseSqlite().connect()

        self.current_page = 1
        self.page_row_count = 50

        con.execute('select count(*) from volunteer_span')
        self.total_record_count = con.fetchone()[0]
        self.total_page_count = self.total_record_count // self.page_row_count + \
                                1 if self.total_record_count % self.page_row_count > 0 else 0
        con.execute('select min(create_dttm), max(create_dttm) from volunteer_span')
        self.min_dttm, self.max_dttm = con.fetchone()

        self.query_records()
        self.set_headers()

    def set_headers(self):
        self.setHeaderData(0, Qt.Horizontal, 'ID')
        self.setHeaderData(1, Qt.Horizontal, 'Paragraph ID')
        self.setHeaderData(2, Qt.Horizontal, 'Volunteer ID')
        self.setHeaderData(3, Qt.Horizontal, 'Span ID')
        self.setHeaderData(4, Qt.Horizontal, 'Create DTTM')

    def query_records(self, offset: int = 0):
        self.setQuery(f'''
            select id_vol_span id, id_section, 
                id_volunteer, vs.id_span, create_dttm 
            from volunteer_span vs
            inner join span s on vs.id_span = s.id_span
            where id_volunteer not in moderator
            order by create_dttm
            limit {offset}, {self.page_row_count}
        ''', self.db)


def eval_consensus(date_from: str, date_to: str):
    if date_to < date_from:
        date_from, date_to = date_to, date_from

    con = DatabaseSqlite().connect()

    con.execute('insert into report default values')
    id_report = con.lastrowid

    con.execute('select id_category, name_agreement from category_agreement')
    categories = {name_agreement: id_category for id_category, name_agreement in con.fetchall()}

    con.execute(f'''
        with vol_s as (
            select * from volunteer_span vs
            where id_volunteer not in moderator
                and create_dttm between '{date_from}' and '{date_to}'
        )
        select s.id_span, in_span, in_section from (
            select id_span, count(id_volunteer) over (partition by id_span) as in_span
            from vol_s
        ) vspan inner join span s
            on s.id_span = vspan.id_span
        inner join (
            select id_section, count(id_volunteer) over (partition by id_section) as in_section
            from (
                select distinct id_section, id_volunteer from vol_s vs 
                inner join span s on s.id_span = vs.id_span
            )
        ) vsec on vsec.id_section = s.id_section
        group by s.id_span;
    ''')

    for id_span, in_span, in_section in con.fetchall():
        id_category = None
        if in_section == 2:
            if in_span == 1:
                id_category = categories['Мнения разделились']
            elif in_span == 2:
                id_category = categories['Возможный кворум']
        elif in_section == 3:
            if in_span == 1:
                id_category = categories['Установленное меньшинство']
            elif in_span == 2:
                id_category = categories['Возможный кворум']
            elif in_span == 3:
                id_category = categories['Кворум']
        elif in_section >= 4:
            if in_span == 1:
                id_category = categories['Установленное меньшинство']
            elif in_span == 2:
                id_category = categories['Мнения разделились']
            elif in_span >= 3:
                id_category = categories['Кворум']

        con.execute('''
            insert into report_span(id_report, id_span, id_category)
            values (:id_report, :id_span, :id_category)
        ''', {'id_report': id_report, 'id_span': id_span, 'id_category': id_category})

    con.execute('''
        insert into report_volunteer(id_report, id_volunteer, score)
        select r.id_report, id_volunteer, sum(ifnull(ca.coefficient, 0.1)) score
        from (
            select * from volunteer_span
            where id_volunteer not in moderator
        ) vs
        inner join report_span rs
            on rs.id_span = vs.id_span
        left join category_agreement ca
            on rs.id_category = ca.id_category
        inner join report r
            on r.id_report = rs.id_report
        where r.id_report = ?
        group by id_volunteer;
    ''', (id_report, ))

    con.execute('''
        with volunteer_span_coefficient as (
            with span_volunteer_rank as (
                select rv.id_volunteer, vs.id_span, rv.volunteer_rank, rv.volunteers_count
                from (
                    select id_volunteer,
                           dense_rank() over (order by score desc) volunteer_rank,
                           count(id_volunteer) over () volunteers_count
                    from report_volunteer rv
                    inner join report r on r.id_report = rv.id_report
                    where r.id_report = :id_report
                ) rv
                inner join volunteer_span vs on vs.id_volunteer = rv.id_volunteer
                union
                select id_volunteer, rs.id_span, 0, 1
                from volunteer_span
                inner join report_span rs on volunteer_span.id_span = rs.id_span
                where id_volunteer in moderator and rs.id_report = :id_report
            )
            select vs.id_volunteer, vs.id_span,
                   (1 - min(volunteer_rank) * 1.0 / volunteers_count) coefficient
            from (
                select id_span, id_volunteer from volunteer_span
                where id_volunteer not in moderator
            ) vs inner join span_volunteer_rank svr on svr.id_span = vs.id_span and svr.id_volunteer != vs.id_volunteer
            group by vs.id_volunteer, vs.id_span
        )
        update report_volunteer
        set score = score + ifnull((
            select sum(coefficient) from volunteer_span_coefficient vsc
            where vsc.id_volunteer = report_volunteer.id_volunteer
            group by vsc.id_volunteer
        ), 0)
        where id_report = :id_report;
    ''', {'id_report': id_report})

    DatabaseSqlite().connection.commit()


class View(QMainWindow):
    def __init__(self, database: QSqlDatabase, parent=None):
        super(QMainWindow, self).__init__(parent, flags=Qt.Window)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.db = database

        self.main_table_model = None
        self.init_main_table()

        self.rating_table_model = None
        self.init_rating_table()

        self.block_chart = None
        self.volunteer_chart = None
        self.section_chart = None

        self.load_reports()

        self.set_up_connect()

    def init_main_table(self):
        self.main_table_model = MainTableModel(self.db)
        self.ui.spin_box_switch.setMaximum(self.main_table_model.total_page_count)
        self.on_all_period_click()
        self.ui.table_view_main.setModel(self.main_table_model)

        header = self.ui.table_view_main.horizontalHeader()
        header.setStretchLastSection(True)
        header.setSectionResizeMode(QHeaderView.Stretch)

    def init_rating_table(self):
        self.rating_table_model = RatingTableModel(self.db)
        self.ui.table_view_rating.setModel(self.rating_table_model)

        header = self.ui.table_view_rating.horizontalHeader()
        header.setStretchLastSection(True)
        header.setSectionResizeMode(QHeaderView.Stretch)

    def set_up_connect(self):
        self.ui.push_button_prev.clicked.connect(self.on_prev_page_click)
        self.ui.push_button_next.clicked.connect(self.on_next_page_click)
        self.ui.push_button_switch.clicked.connect(self.on_switch_page_click)

        self.ui.push_button_all_period.clicked.connect(self.on_all_period_click)

        self.ui.table_view_main.clicked.connect(self.on_main_table_click)
        self.ui.push_button_build_report.clicked.connect(self.on_build_report_click)

        self.ui.push_button_charts_report.clicked.connect(self.show_charts_categories)
        self.ui.push_button_charts_delete_report.clicked.connect(
            lambda: self.delete_report(self.ui.combo_box_charts_report)
        )

        self.ui.push_button_section.clicked.connect(
            lambda: self.build_section_chart(self.ui.spin_box_section.value())
        )
        self.ui.push_button_volunteer.clicked.connect(
            lambda: self.build_volunteer_chart(self.ui.spin_box_volunteer.value())
        )

        self.ui.push_button_rating_report.clicked.connect(self.show_rating)
        self.ui.push_button_rating_delete_report.clicked.connect(
            lambda: self.delete_report(self.ui.combo_box_rating_report)
        )

    def delete_report(self, combo_box: QComboBox):
        cur_rep_id = self.current_report_id(combo_box)
        if cur_rep_id > -1:
            con = DatabaseSqlite().connect()
            con.execute('delete from report_volunteer where id_report = ?', (cur_rep_id,))
            con.execute('delete from report_span where id_report = ?', (cur_rep_id,))
            con.execute('delete from report where id_report = ?', (cur_rep_id,))
            DatabaseSqlite().connection.commit()
            self.load_reports()
            self.ui.statusbar.showMessage(
                f'Удален отчет: {cur_rep_id} - {self.ui.combo_box_charts_report.currentText()}'
            )
        else:
            self.ui.statusbar.showMessage('Отчет не найден')

    @staticmethod
    def current_report_id(combo_box: QComboBox):
        con = DatabaseSqlite().connect()
        con.execute(
            f"select id_report from report where create_dttm = '{combo_box.currentText()}'"
        )
        res = con.fetchone()
        if res:
            return res[0]
        else:
            return -1

    def load_reports(self):
        con = DatabaseSqlite().connect()
        con.execute('select create_dttm from report order by create_dttm desc')
        reports_dttm = [r[0] for r in con.fetchall()]
        self.ui.combo_box_charts_report.clear()
        self.ui.combo_box_charts_report.addItems(reports_dttm)
        self.ui.combo_box_rating_report.clear()
        self.ui.combo_box_rating_report.addItems(reports_dttm)

    def build_block_chart(self, cur_rep_id: int = None):
        if not cur_rep_id:
            cur_rep_id = self.current_report_id(self.ui.combo_box_rating_report)
        if cur_rep_id < 0:
            self.ui.statusbar.showMessage('Необходимый отчет отсутствует')
            return
        con = DatabaseSqlite().connect()
        con.execute('''
            select ca.name_agreement category, count(id_span) count_spans
            from report_span rs
            inner join report r on rs.id_report = r.id_report
            inner join category_agreement ca on rs.id_category = ca.id_category 
            where r.id_report = ?
            group by rs.id_category
        ''', (cur_rep_id,))
        block_dict = {r[0]: r[1] for r in con.fetchall()}
        if self.block_chart is not None:
            self.ui.v_layout_block_chart.removeWidget(self.block_chart)
        self.block_chart = PlotCanvas(list(block_dict.values()), 'Оценка среза')
        self.ui.v_layout_block_chart.addWidget(self.block_chart)

    def build_volunteer_chart(self, vol_id: int, cur_rep_id: int = None):
        if not cur_rep_id:
            cur_rep_id = self.current_report_id(self.ui.combo_box_rating_report)
        if cur_rep_id < 0:
            self.ui.statusbar.showMessage('Необходимый отчет отсутствует')
            return
        con = DatabaseSqlite().connect()
        con.execute('''
            select ca.name_agreement category, count(rs.id_span) count_spans
            from volunteer_span vs
            inner join report_span rs on rs.id_span = vs.id_span
            inner join report r on rs.id_report = r.id_report
            inner join category_agreement ca on rs.id_category = ca.id_category
            where r.id_report = :rep_id and vs.id_volunteer = :vol_id
            group by rs.id_category
        ''', {'rep_id': cur_rep_id, 'vol_id': vol_id})
        vol_spans = {r[0]: r[1] for r in con.fetchall()}
        if self.volunteer_chart is not None:
            self.ui.v_layout_volunteer_chart.removeWidget(self.volunteer_chart)
        self.volunteer_chart = PlotCanvas(list(vol_spans.values()), 'Оценка волонтера')
        self.ui.v_layout_volunteer_chart.addWidget(self.volunteer_chart)

    def build_section_chart(self, sec_id: int, cur_rep_id: int = None):
        if not cur_rep_id:
            cur_rep_id = self.current_report_id(self.ui.combo_box_rating_report)
        if cur_rep_id < 0:
            self.ui.statusbar.showMessage('Необходимый отчет отсутствует')
            return
        con = DatabaseSqlite().connect()
        con.execute('''
            select ca.name_agreement category, count(rs.id_span) count_spans
            from span s
            inner join report_span rs on rs.id_span = s.id_span 
            inner join report r on rs.id_report = r.id_report
            inner join category_agreement ca on rs.id_category = ca.id_category
            where r.id_report = :rep_id and s.id_section = :sec_id
            group by rs.id_category
        ''', {'rep_id': cur_rep_id, 'sec_id': sec_id})
        sec_spans = {r[0]: r[1] for r in con.fetchall()}
        if self.section_chart is not None:
            self.ui.v_layout_section_chart.removeWidget(self.section_chart)
        self.section_chart = PlotCanvas(list(sec_spans.values()), 'Оценка абзаца')
        self.ui.v_layout_section_chart.addWidget(self.section_chart)

    def on_build_report_click(self):
        self.ui.tab_widget.setCurrentIndex(1)

        eval_consensus(self.ui.date_time_from.text(), self.ui.date_time_to.text())
        self.load_reports()
        self.show_charts_categories()

        self.ui.statusbar.showMessage(
            f'Построен отчет за период [{self.ui.date_time_from.text()}, {self.ui.date_time_to.text()}]'
        )

    def show_charts_categories(self):
        cur_rep_id = self.current_report_id(self.ui.combo_box_charts_report)
        self.build_block_chart(cur_rep_id)
        self.build_volunteer_chart(self.ui.spin_box_volunteer.value(), cur_rep_id)
        self.build_section_chart(self.ui.spin_box_section.value(), cur_rep_id)
        self.ui.statusbar.showMessage(f'Выбран отчет: {cur_rep_id} - {self.ui.combo_box_charts_report.currentText()}')

    def show_rating(self):
        cur_rep_id = self.current_report_id(self.ui.combo_box_rating_report)
        if cur_rep_id > -1:
            self.rating_table_model.update_table(cur_rep_id)
        else:
            self.ui.statusbar.showMessage('Отчета не существет')

    def on_main_table_click(self, index):
        self.ui.spin_box_section.setValue(index.siblingAtColumn(1).data())
        self.ui.spin_box_volunteer.setValue(index.siblingAtColumn(2).data())
        if QApplication.keyboardModifiers() == Qt.AltModifier:
            self.ui.date_time_to.setDateTime(
                datetime.strptime(index.siblingAtColumn(4).data(), '%Y-%m-%d %H:%M:%S')
            )
            date = self.ui.date_time_to.text()
        else:
            self.ui.date_time_from.setDateTime(
                datetime.strptime(index.siblingAtColumn(4).data(), '%Y-%m-%d %H:%M:%S')
            )
            date = self.ui.date_time_from.text()
        if self.ui.date_time_from.text() > self.ui.date_time_to.text():
            temp = self.ui.date_time_from.dateTime()
            self.ui.date_time_from.setDateTime(self.ui.date_time_to.dateTime())
            self.ui.date_time_to.setDateTime(temp)

        self.ui.statusbar.showMessage(
            f'Выбраны волонтер: {self.ui.spin_box_volunteer.value()} | '
            f'абзац: {self.ui.spin_box_section.value()} | '
            f'дата: {date}'
        )

    def on_all_period_click(self):
        self.ui.date_time_from.setDateTime(
            datetime.strptime(self.main_table_model.min_dttm, '%Y-%m-%d %H:%M:%S')
        )
        self.ui.date_time_to.setDateTime(
            datetime.strptime(self.main_table_model.max_dttm, '%Y-%m-%d %H:%M:%S')
        )
        self.ui.statusbar.showMessage('Выбран весь период')

    def on_prev_page_click(self):
        if self.main_table_model.current_page - 1 > 0:
            self.main_table_model.current_page -= 1
            self.main_table_model.query_records(
                (self.main_table_model.current_page - 1) * self.main_table_model.page_row_count
            )
            self.ui.spin_box_switch.setValue(self.main_table_model.current_page)
            self.ui.statusbar.showMessage(f'Текущая страница: {self.main_table_model.current_page}')
        else:
            self.ui.statusbar.showMessage('Достигнута минимальная страница')

    def on_next_page_click(self):
        if self.main_table_model.current_page + 1 < self.main_table_model.total_page_count:
            self.main_table_model.current_page += 1
            self.main_table_model.query_records(
                (self.main_table_model.current_page - 1) * self.main_table_model.page_row_count
            )
            self.ui.spin_box_switch.setValue(self.main_table_model.current_page)
            self.ui.statusbar.showMessage(f'Текущая страница: {self.main_table_model.current_page}')
        else:
            self.ui.statusbar.showMessage('Достигнута максимальная страница')

    def on_switch_page_click(self):
        self.main_table_model.current_page = self.ui.spin_box_switch.value()
        self.main_table_model.query_records(
            (self.main_table_model.current_page - 1) * self.main_table_model.page_row_count
        )
        self.ui.statusbar.showMessage(f'Текущая страница: {self.main_table_model.current_page}')


def main():
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"

    app = QApplication(sys.argv)
    app.setAttribute(Qt.AA_EnableHighDpiScaling)

    sqlite_database = QSqlDatabase.addDatabase('QSQLITE')
    sqlite_database.setDatabaseName('../spans.db')
    DatabaseSqlite.db_path = '../spans.db'
    if not sqlite_database.open():
        return -1

    view = View(sqlite_database)
    view.show()

    app.exec()


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    sys.exit(main())
