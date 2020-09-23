drop table if exists moderator;
drop table if exists report_span;
drop table if exists category_agreement;
drop table if exists report_volunteer;
drop table if exists report;
drop table if exists volunteer_section;
drop table if exists volunteer_span;
drop table if exists span;
drop table if exists section;
drop table if exists volunteer;

create table category_agreement
(
    id_category    integer not null,
    name_agreement varchar not null,
    coefficient    float,
    constraint category_agreement_pk
        primary key (id_category autoincrement)
);

create unique index category_agreement_name_agreement_uindex
    on category_agreement (name_agreement);

create table report
(
    id_report   integer not null,
    create_dttm timestamp default current_timestamp not null,
    constraint report_pk
        primary key (id_report autoincrement)
);

create table section
(
    id_section integer not null,
    constraint section_pk
        primary key (id_section)
);

create table span
(
    id_span     integer not null,
    id_section  integer not null,
    tag_name    varchar not null,
    start_token integer not null,
    length      integer not null,
    constraint span_pk
        primary key (id_span autoincrement),
    foreign key (id_section) references section
        on update cascade on delete cascade
);

create table report_span
(
    id_report_span integer not null,
    id_report      integer not null,
    id_span        integer not null,
    id_category    integer,
    constraint report_span_pk
        primary key (id_report_span autoincrement),
    foreign key (id_report) references report
        on update cascade on delete cascade,
    foreign key (id_report) references span
        on update cascade on delete cascade,
    foreign key (id_category) references category_agreement
        on update cascade on delete cascade
);

create unique index report_span_id_report_id_span_uindex
    on report_span (id_report, id_span);

create unique index span_uindex
    on span (id_section, tag_name, start_token, length);

create table volunteer
(
    id_volunteer integer not null,
    constraint volunteer_pk
        primary key (id_volunteer)
);

create table moderator
(
    id_moderator integer not null,
    constraint moderator_pk
        primary key (id_moderator),
    foreign key (id_moderator) references volunteer
        on update cascade on delete cascade
);

create table report_volunteer
(
    id_rep_vol   integer not null,
    id_report    integer not null,
    id_volunteer integer not null,
    score        float default 0 not null,
    constraint report_volunteer_pk
        primary key (id_rep_vol autoincrement),
    foreign key (id_report) references report
        on update cascade on delete cascade,
    foreign key (id_volunteer) references volunteer
        on update cascade on delete cascade
);

create unique index report_volunteer_id_report_id_volunteer_uindex
    on report_volunteer (id_report, id_volunteer);

create table volunteer_section
(
    id_vol_sec   integer not null,
    id_volunteer integer not null,
    id_section   integer not null,
    constraint volunteer_section_pk
        primary key (id_vol_sec autoincrement),
    foreign key (id_volunteer) references volunteer
        on update cascade on delete cascade,
    foreign key (id_section) references section
        on update cascade on delete cascade
);

create unique index volunteer_section_id_volunteer_id_section_uindex
    on volunteer_section (id_volunteer, id_section);

create table volunteer_span
(
    id_vol_span  integer not null,
    id_volunteer integer not null,
    id_span      integer not null,
    create_dttm  timestamp default current_timestamp not null,
    constraint volunteer_section_pk
        primary key (id_vol_span autoincrement),
    foreign key (id_volunteer) references volunteer
        on update cascade on delete cascade,
    foreign key (id_span) references span
        on update cascade on delete cascade
);

create unique index volunteer_span_id_volunteer_id_span_uindex
    on volunteer_span (id_volunteer, id_span);
