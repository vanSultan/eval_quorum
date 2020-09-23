-- init categories of agreement
insert into category_agreement(name_agreement)
values ('Кворум'),
       ('Возможный кворум'),
       ('Мнения разделились'),
       ('Одиночное мнение');

-- set coefficient of category
with cat_coef as (
    select id_category, (1. - (id_category - 1.) / cnt) coef from (
        select id_category, count(*) over () cnt
        from category_agreement
    )
)
update category_agreement
set coefficient = (
    select coef from cat_coef
    where category_agreement.id_category = cat_coef.id_category
) where id_category > 0;

-- build moderators
insert into moderator (id_moderator)
select id_volunteer from volunteer_section
where id_section in (
    select id_section
    from volunteer_section
    group by id_section
    having count(id_volunteer) > 4
)
group by id_volunteer
having count(id_section) > 500
order by count(id_section);

-- evaluating
select distinct s.id_span, in_span, in_section from (
    select id_span, count(id_volunteer) over (partition by id_span) as in_span
    from volunteer_span
    where id_volunteer not in moderator
) vspan inner join span s
    on s.id_span = vspan.id_span
inner join (
    select id_section, id_volunteer, count(id_volunteer) over (partition by id_section) as in_section
    from volunteer_section
    where id_volunteer not in moderator
) vsec on vsec.id_section = s.id_section;

-- get rating
insert into report_volunteer(id_report, id_volunteer, score)
select r.id_report, id_volunteer, sum(ifnull(ca.coefficient, 0)) score
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
where r.create_dttm = (
    select max(create_dttm) from report
)
group by id_volunteer;
