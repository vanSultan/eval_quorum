from utility.database import DatabaseSqlite, DatabasePostgres

if __name__ == '__main__':
    DatabaseSqlite.db_path = '../spans.db'
    # con = DatabaseSqlite().connect()
    con = DatabasePostgres().connect()

    # con.execute('insert into report default values')
    id_report = 6

    con.execute('select id_category, name_agreement from category_agreement')
    categories = {name_agreement: id_category for id_category, name_agreement in con.fetchall()}

    con.execute(f'''
            with vol_s as (
                select * from volunteer_span vs
                where id_volunteer not in (select id_moderator from moderator)
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
                ) t
            ) vsec on vsec.id_section = s.id_section
            group by s.id_span, in_span, in_section;
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
                values (%(id_report)s, %(id_span)s, %(id_category)s)
            ''', {'id_report': id_report, 'id_span': id_span, 'id_category': id_category})

    con.execute('''
            insert into report_volunteer(id_report, id_volunteer, score)
            select r.id_report, id_volunteer, sum(coalesce(ca.coefficient, 0)) score
            from (
                select * from volunteer_span
                where id_volunteer not in (select id_moderator from moderator)
            ) vs
            inner join report_span rs
                on rs.id_span = vs.id_span
            left join category_agreement ca
                on rs.id_category = ca.id_category
            inner join report r
                on r.id_report = rs.id_report
            where r.id_report = %s
            group by r.id_report, id_volunteer;
        ''', (id_report,))

    DatabasePostgres().connection.commit()
