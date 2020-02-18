class Eval:
    single = 1  # Одиночное мнение
    half = 2  # Мнения разделилсь
    p_quorum = 3  # Возможный кворум
    quorum = 4  # Кворум
    alone = 0  # Не имеет значения

    common_stat = {
        single: {'label': 'Одиночное мнение', 'count': 0},
        half: {'label': 'Мнения разделились', 'count': 0},
        p_quorum: {'label': 'Возможный кворум', 'count': 0},
        quorum: {'label': 'Кворум', 'count': 0}
    }

    flag_ignore = True

    def __init__(self, stat: dict):
        self._state = None
        self._p_quorum_to_quorum = 0
        self._p_quorum_to_half = 0
        self._half_to_p_quorum = 0
        self._half_to_single = 0
        self._single_to_half = 0
        self._stat = stat

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, new_state: int):
        if new_state != self._state:
            try:
                self._stat[self._state]['count'] -= 1
            except KeyError:
                pass
            try:
                self._stat[new_state]['count'] += 1
            except KeyError:
                pass
        # if self._state == Eval.p_quorum and new_state == Eval.quorum:
        #     self._p_quorum_to_quorum += 1
        # elif self._state == Eval.p_quorum and new_state == Eval.half:
        #     self._p_quorum_to_half += 1
        # elif self._state == Eval.half and new_state == Eval.p_quorum:
        #     self._half_to_p_quorum += 1
        # elif self._state == Eval.half and new_state == Eval.single:
        #     self._half_to_single += 1
        # elif self._state == Eval.single and new_state == Eval.half:
        #     self._single_to_half += 1
        self._state = new_state


class Span:
    def __init__(self, span_id: int, volunteer_id: int, e: Eval):
        self.span_id = span_id
        self.volunteers = {volunteer_id}
        self.eval = e

    def __eq__(self, other) -> bool:
        return self.span_id == other.span_id

    def update_eval(self, vol_in_sec: int) -> int:
        vol_in_span = len(self.volunteers)

        # self.eval.state = None  # Не имеет значения
        if vol_in_sec == 2:
            if vol_in_span == 1:
                self.eval.state = Eval.half  # Мнения разделились
            elif vol_in_span == 2:
                self.eval.state = Eval.p_quorum  # Возможный кворум
        elif vol_in_sec == 3:
            if vol_in_span == 1:
                self.eval.state = Eval.single  # Одиночное мнение
            elif vol_in_span == 2:
                self.eval.state = Eval.p_quorum  # Возможный кворум
            elif vol_in_span == 3:
                self.eval.state = Eval.quorum  # Кворум
        elif vol_in_sec == 4 or vol_in_sec > 4 and not Eval.flag_ignore:
            if vol_in_span == 1:
                self.eval.state = Eval.single  # Одиночное мнение
            elif vol_in_span == 2:
                self.eval.state = Eval.half  # Мнения разделились
            elif vol_in_span == 3:
                self.eval.state = Eval.quorum  # Кворум
            elif vol_in_span == 4 or vol_in_span > 4 and not Eval.flag_ignore:
                self.eval.state = Eval.quorum  # Кворум
        elif vol_in_sec > 4:
            # TODO: Флаг на игнор ложь - тогда есть два варианта поведения:
            # TODO: анализировать данные с учетом блэк-листа или с кворумом тоже сомнительно
            pass
        else:
            self.eval.state = Eval.alone  # Не имеет значения

        return self.eval.state


class Section:
    def __init__(self, section_id: int):
        self.section_id = section_id
        self._spans = list()
        self._volunteers = set()

    @property
    def spans(self):
        return self._spans

    @property
    def volunteers(self):
        return self._volunteers

    def update_eval(self, vol_in_sec: int = None):
        if not vol_in_sec:
            vol_in_sec = len(self._volunteers)

        for span in self._spans:
            span.update_eval(vol_in_sec)
