select * from student;
select * from actual_group;

select * from student_group;

select * from news_group;

select * from news;

alter table news
rename column data_of_pub to date_of_pub;

select * from contacts;

select * from subject;
-- Course DML
alter table course alter column course_name drop not null;

select * from course;

select name, last_name, isu_id, teacher_id, course_id, subject_name from course as co
join teacher as tea on co.lector = tea.teacher_id
join humans as hum on tea.fk_humans_id = hum.isu_id
join subject as sub on co.fk_subject = sub.subject_id;

select * from contacts_course;
-- Human
select * from humans;

select * from humans as hum
join teacher as tea on tea.fk_humans_id = hum.isu_id
-- Eduation materials
alter table educational_materials add column material_type material_type not null;