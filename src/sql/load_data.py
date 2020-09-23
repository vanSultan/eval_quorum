import datetime
import os
import random

from utility.database import DatabaseSqlite, DatabasePostgres


def load_data(csv_path: str,
              start_dttm: datetime.datetime = datetime.datetime(2019, 6, 1, 15, 32, 41),
              time_step: int = 360,
              first_head: bool = True):
    with open(csv_path) as f_src:
        # db = DatabaseSqlite()
        db = DatabasePostgres()
        cursor = db.connect()

        if first_head:
            f_src.readline()

        for line in f_src:
            sec_id, vol_id, _, tag_name, start_token, length = line.strip().split(',')
            sec_id = int(sec_id)
            vol_id = int(vol_id)
            start_token = int(start_token)
            length = int(length)

            cursor.execute('''
                insert into section(id_section)
                select %(id_section)s where not exists(
                    select 1 from section where id_section = %(id_section)s 
                )
            ''', {'id_section': sec_id})
            cursor.execute('''
                insert into volunteer(id_volunteer)
                select %(id_volunteer)s where not exists(
                    select 1 from volunteer where id_volunteer = %(id_volunteer)s
                )
            ''', {'id_volunteer': vol_id})
            cursor.execute('''
                insert into span(id_section, tag_name, start_token, length)
                select %(id_section)s, %(tag_name)s, %(start_token)s, %(length)s where not exists(
                    select 1 from span where 
                        id_section = %(id_section)s and tag_name = %(tag_name)s
                        and start_token = %(start_token)s and length = %(length)s 
                )
            ''', {'id_section': sec_id, 'tag_name': tag_name, 'start_token': start_token, 'length': length})

            cursor.execute('''
                select id_span from span where 
                    id_section = %s and tag_name = %s 
                    and start_token = %s and length = %s
            ''', (sec_id, tag_name, start_token, length))
            span_id = cursor.fetchone()[0]

            cursor.execute('''
                insert into volunteer_section(id_volunteer, id_section)
                select %(id_volunteer)s, %(id_section)s where not exists(
                    select 1 from volunteer_section where id_volunteer = %(id_volunteer)s and id_section = %(id_section)s
                )
            ''', {'id_volunteer': vol_id, 'id_section': sec_id})
            cursor.execute('''
                insert into volunteer_span(id_volunteer, id_span, create_dttm) 
                select %(id_volunteer)s, %(id_span)s, %(create_dttm)s where not exists(
                    select 1 from volunteer_span where id_volunteer = %(id_volunteer)s and id_span = %(id_span)s
                )
            ''', {'id_volunteer': vol_id, 'id_span': span_id, 'create_dttm': start_dttm.strftime('%Y-%m-%d %H:%M:%S')})
            start_dttm = start_dttm + datetime.timedelta(0, random.randint(2, time_step))
        db.connection.commit()


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    # DatabaseSqlite.db_path = '../../spans.db'
    load_data('../../spans.csv')
