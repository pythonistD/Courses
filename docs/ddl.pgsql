create table humans(
	isu_id serial primary key,
	name varchar(100) not null,
	last_name varchar(100) not null,
	password varchar(100) not null default '111'
);
create table student (
	student_id serial primary key,
	fk_human_id int not null references humans on delete cascade,
    group_name varchar(100) not null,
	department varchar(300) not null DEFAULT 'ПИКТ',
	curriculum varchar(300) not null default 'СППО',
	course smallint not null,
	constraint course_limits check (course > 0 and course < 5),
	unique(fk_human_id)
);
create table teacher(
	teacher_id serial primary key,
	fk_humans_id int not null references humans on delete cascade,
	department varchar(300) not null,
	unique(fk_humans_id)
);

create table actual_group(
    actual_group_id serial primary key,
    group_name varchar(100) not null,
    mentor int references teacher on delete cascade
);

create table student_group(
	student_group_id serial primary key,
	fk_student int not null references student on delete cascade,
	fk_actual_group int not null references actual_group on delete cascade,
	unique(fk_student, fk_actual_group)
);

create table news(
	news_id serial primary key,
	title varchar(300) not null,
	body text not null,
	date_of_pub timestamp not null
);

create table news_group(
	news_group_id serial primary key,
	fk_news int not null references news on delete cascade,
	fk_actual_group int not null references actual_group on delete cascade,
	unique(fk_news, fk_actual_group)
);

create table contacts(
	contacts_id serial primary key,
	title varchar(300) not null,
	resource text not null
);

create table group_contacts(
	group_contacts_id serial primary key,
	fk_actual_group int not null references actual_group on delete cascade,
	fk_contacts int not null references contacts on delete cascade,
	unique(fk_actual_group, fk_contacts)
);

create table subject(
	subject_id serial primary key,
	subject_name varchar(200) not null,
	description text,
);

create table course(
	course_id serial primary key,
	course_name varchar(300),
	term smalliNewsListViewlt 1,
	fk_subject int not null references subject on delete cascade,
	lector int not null references teacher on delete cascade,

	constraint valid_term check(term > 0 and term < 8)
);

create table contacts_course(
	contacts_course_id serial primary key,
	fk_course int not null references course on delete cascade,
	fk_contacts int not null references contacts on delete cascade,
	unique(fk_course, fk_contacts)
);

create table course_group(
	course_group serial primary key,
	fk_course int not null references course on delete cascade,
	fk_group int not null references actual_group on delete cascade,
	unique(fk_course, fk_group)
);

create type material_type as enum ('book', 'article', 'video', 'other');

create table educational_materials(
	ed_m_id serial primary key,
	title varchar(300) not null,
	url text,
	material_type material_type not null
);

create table materials_course(
	materials_course_id serial primary key,
	fk_course int not null references course on delete cascade,
	fk_materials int not null references educational_materials on delete cascade,
	unique(fk_course, fk_materials)
);

create type task_type as enum ('course_work', 'home_work', 'lab');

create table tasks(
	tasks_id serial primary key,
	title varchar(300) not null,
	description text not null,
	task_type task_type not null,
	date_of_pub timestamp not null,
	deadline timestamp not null
);

create table tasks_course(
	tasks_course_id serial primary key,
	fk_course int not null references course on delete cascade,
	fk_tasks int not null references tasks on delete cascade,
	unique(fk_course, fk_tasks)
);