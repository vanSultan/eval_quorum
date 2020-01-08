from database import Database


class TableStorage:
    def __init__(self, row_offset: int = 0, row_count: int = 50):
        self._cursor = Database().connect()

        self.row_offset = row_offset
        self.row_count = row_count

    def get_table(self, row_offset: int = None, row_count: int = None) -> list:
        offset = row_offset if row_offset else self.row_offset
        count = row_count if row_count else self.row_count

        request = f"""
            select id_vol_span, volunteer_id, section_id, span_id 
            from volunteer_span inner join span s on volunteer_span.span_id = s.id_span
            offset {offset} limit {count}
        """
        self._cursor.execute(request)

        return self._cursor.fetchall()

    def get_total_count(self):
        request = """
            select count(id_vol_span) 
            from volunteer_span
        """
        self._cursor.execute(request)

        return self._cursor.fetchone()[0]

    def get_limits(self):
        request = """
            select min(id_vol_span), max(id_vol_span)
            from volunteer_span
        """
        self._cursor.execute(request)

        return self._cursor.fetchone()

    def __del__(self):
        self._cursor.close()
