from abc import abstractmethod, ABC

from utility.database import DatabasePostgres, DatabaseCsvFile
from utility.entitys import Eval, Span, Section


class EvalModel:
    def __init__(self, begin_limit: int, end_limit: int):
        self._begin_limit = begin_limit
        self._end_limit = end_limit

        self.statistic = dict()
        for key in Eval.common_stat.keys():
            self.statistic.update({key: Eval.common_stat[key].copy()})

        self._total = self.get_total()
        self._processed = 0
        self._step = round(self._total / 100) if self._total > 100 else 1

        self.labels = [val['label'] for val in self.statistic.values()]

    @property
    def data(self):
        sections = list()
        self._processed = 0

        for section_id, span_id, volunteer_id in self.records_generator():
            section = next((sec for sec in sections if sec.section_id == section_id), None)

            if section is None:
                section = Section(section_id)
                sections.append(section)

            new_volunteer = volunteer_id not in section.volunteers

            span = next((s for s in section.spans if s.span_id == span_id), None)

            if span is None:
                span = Span(span_id, volunteer_id, Eval(self.statistic))
                section.spans.append(span)
            else:
                span.volunteers.add(volunteer_id)

            if new_volunteer:
                section.volunteers.add(volunteer_id)
                section.update_eval()

            self._processed += 1
            # print(self.statistic)

            if self._processed % self._step == 0 or self._processed == self._total:
                yield [val['count'] for val in self.statistic.values()]

    @abstractmethod
    def records_generator(self):
        pass

    @abstractmethod
    def get_total(self):
        pass

    @property
    @abstractmethod
    def title(self):
        pass


class EvalModelSql(EvalModel, ABC):
    def __init__(self, *args, **kwargs):
        self._connection = DatabasePostgres()
        self._cursor = self._connection.connect()
        super().__init__(*args, **kwargs)

    def records_generator(self):
        self._cursor.execute(self.get_request())

        for record in self._cursor.fetchall():
            yield record

    @abstractmethod
    def get_request(self):
        pass


class EvalModelPandas(EvalModel, ABC):
    def __init__(self, *args, **kwargs):
        self._connection = DatabaseCsvFile()
        self._data_frame = self._connection.data_frame
        super().__init__(*args, **kwargs)

    def records_generator(self):
        df = self.prepare_data_frame()
        data = df[['par_id', 'span_id', 'user_id']].to_numpy()

        for rec in data:
            rec = tuple(rec)
            yield rec

        # data = [(1, 1, 1), (1, 2, 2), (1, 3, 3), (1, 4, 4),
        #         (2, 5, 1), (2, 5, 2), (2, 5, 3), (2, 5, 4),
        #         (3, 6, 1), (3, 6, 2), (3, 6, 3), (3, 7, 4),
        #         (4, 8, 1), (4, 8, 2), (4, 9, 3), (4, 9, 4),
        #         (5, 10, 1), (5, 10, 2), (5, 11, 3), (5, 12, 4)]
        # for d in data:
        #     yield d

    def get_total(self):
        df = self.prepare_data_frame()
        total = df['span_id'].count()
        return total

    @abstractmethod
    def prepare_data_frame(self):
        pass


class EvalFrameModelSql(EvalModelSql):
    @property
    def title(self):
        return 'Оценка корпуса'

    def get_request(self):
        request = f"""
            select section_id, span_id, volunteer_id from volunteer_span
            inner join span s on volunteer_span.span_id = s.id_span
            where id_vol_span between {self._begin_limit} and {self._end_limit}
        """

        return request

    def get_total(self):
        request = f"""
            select count(span_id) from volunteer_span
            where id_vol_span between {self._begin_limit} and {self._end_limit}
        """
        self._cursor.execute(request)

        return self._cursor.fetchone()[0]


class EvalFrameModelPandas(EvalModelPandas):
    @property
    def title(self):
        return 'Оценка корпуса'

    def prepare_data_frame(self):
        df = self._data_frame
        return df[(df['entity_id'] >= self._begin_limit) & (df['entity_id'] <= self._end_limit)]


class EvalVolunteerModelSql(EvalModelSql):
    def __init__(self, id_volunteer: int, *args, **kwargs):
        self._id_volunteer = id_volunteer
        super().__init__(*args, **kwargs)

    @property
    def title(self):
        return 'Оценка волонтера'

    def get_request(self):
        request = f"""
            select section_id, span_id, volunteer_id from volunteer_span
            inner join span s on volunteer_span.span_id = s.id_span
            where id_vol_span between {self._begin_limit} and {self._end_limit}
            and span_id in (select span_id from volunteer_span where volunteer_id = {self._id_volunteer})
        """

        return request

    def get_total(self):
        request = f"""
            select count(span_id) from volunteer_span
            where id_vol_span between {self._begin_limit} and {self._end_limit}
            and volunteer_id = {self._id_volunteer}
        """
        self._cursor.execute(request)

        return self._cursor.fetchone()[0]


class EvalVolunteerModelPandas(EvalModelPandas):
    @property
    def title(self):
        return 'Оценка волонтера'

    def __init__(self, id_volunteer: int, *args, **kwargs):
        self._id_volunteer = id_volunteer
        super().__init__(*args, **kwargs)

    def prepare_data_frame(self):
        df = self._data_frame
        df = df[(df['entity_id'] >= self._begin_limit) & (df['entity_id'] <= self._end_limit)]
        spans = df[df['user_id'] == self._id_volunteer]['span_id']
        return df[df['span_id'].isin(spans)]


class EvalSectionModelSql(EvalModelSql):
    def __init__(self, id_section: int, *args, **kwargs):
        self._id_section = id_section
        super().__init__(*args, **kwargs)

    @property
    def title(self):
        return 'Оценка абзаца'

    def get_request(self):
        request = f"""
            select section_id, span_id, volunteer_id from volunteer_span
            inner join span s on volunteer_span.span_id = s.id_span
            where id_vol_span between {self._begin_limit} and {self._end_limit}
            and section_id = {self._id_section}
        """

        return request

    def get_total(self):
        request = f"""
            select count(span_id) from volunteer_span
            inner join span s on volunteer_span.span_id = s.id_span
            where id_vol_span between {self._begin_limit} and {self._end_limit}
            and section_id = {self._id_section}
        """
        self._cursor.execute(request)

        return self._cursor.fetchone()[0]


class EvalSectionModelPandas(EvalModelPandas):
    def __init__(self, id_section: int, *args, **kwargs):
        self._id_section = id_section
        super().__init__(*args, **kwargs)

    @property
    def title(self):
        return 'Оценка абзаца'

    def prepare_data_frame(self):
        df = self._data_frame
        df = df[(df['entity_id'] >= self._begin_limit) & (df['entity_id'] <= self._end_limit)]
        spans = df[df['par_id'] == self._id_section]['span_id']
        return df[df['span_id'].isin(spans)]
