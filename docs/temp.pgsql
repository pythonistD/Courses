select * from humans;
-- Student 
select * from student;
alter table student 
add COLUMN department varchar(300) not null DEFAULT 'ПИКТ',
add column curriculum varchar(300) not null default 'СППО';


select * from teacher;
select * from actual_group;

select * from student_group;
drop table student_group;

select * from news_group;
drop table news_group;

select * from news;
TRUNCATE news cascade;

alter table news
rename column data_of_pub to date_of_pub;

alter table news
add column author int not null references teacher; 

select * from contacts;

select * from subject;
select * from teacher;
-- Course DML
alter table actual_group alter column mentor drop not null;

select * from course;

select name, last_name, isu_id, teacher_id, course_id, subject_name from course as co
join teacher as tea on co.lector = tea.teacher_id
join humans as hum on tea.fk_humans_id = hum.isu_id
join subject as sub on co.fk_subject = sub.subject_id;

select * from contacts_course;
drop table contacts_course;

select * from course_group;
drop table course_group;

select course_name, actual_group_id from course as c
join course_group as c_g on c_g.fk_course = c.course_id
join actual_group as a_g on c_g.fk_group = a_g.actual_group_id; 
-- Human
select * from humans;

select * from humans as hum
join teacher as tea on tea.fk_humans_id = hum.isu_id;
-- Eduation materials
alter table educational_materials add column material_type material_type not null;

select * from educational_materials;

select * from educational_materials
where ed_m_id = (select max(ed_m_id) from educational_materials);

alter table course add column term smallint not null default 1;

alter table course add constraint valid_term check(term > 0 and term < 8);




alter table subject drop column term;


select course_name from course_group as c_g
join course as c on c.course_id = c_g.fk_course
where fk_group in
(select fk_actual_group from student_group 
where fk_student = 1);

CREATE UNIQUE INDEX CONCURRENTLY student_fk_human_id 
ON student (fk_human_id);

alter table student
add constraint unique_fk_human_id
unique using index student_fk_human_id;


CREATE UNIQUE INDEX CONCURRENTLY teacher_fk_human_id 
ON teacher (fk_humans_id);

alter table teacher
add constraint unique_fk_humans_id
unique using index teacher_fk_human_id;

select * from materials_course;
drop table materials_course;

select * from tasks_course;
select * from tasks;
select * from course;
drop table tasks_course;

select * from student_group
where fk_student = 12;

select * from contacts_course;

truncate table student cascade;

alter table humans add column
	password varchar(100) not null default '111';

select * from humans;