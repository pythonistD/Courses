insert into humans (name, last_name) values
	('Yaroslav', 'Cheboksarov'),
	('Semen', 'Barabanov');
insert into humans (name, last_name) values
	('Иван', 'Петров'),
	('Дмитрий', 'Полежайкин');

insert into humans (name, last_name) values
	('Алексей', 'Иванов');

insert into teacher (fk_humans_id, department) VALUES
    (5, 'ПИКТ');

insert into student (fk_human_id, course, group_name) values
    (1, 3, 'P33091'),
    (2, 3, 'P33091');

insert into actual_group (group_name, mentor) values
    ('P33091', 1),
    ('P33081', 2);

insert into student_group (fk_student, fk_actual_group) values
    (1, 1),
    (2, 2);

insert into news (title, body, date_of_pub) values
    ('very first news', 'This is initial new', CURRENT_TIMESTAMP),
    ('very first news', 'This is initial new', CURRENT_TIMESTAMP);

insert into news_group (fk_news, fk_actual_group) values
    (1, 1),
    (2, 2);

insert into contacts (title, resource) values
    ('Mobile phone number', '+7(981)-534-12-02'),
    ('Reference to the useful article', 'http://useful.com/greate-article');

insert into contacts (title, resource) values
    ('Email for questions', 'lectormail@niuitmo.ru');

insert into group_contacts (fk_actual_group, fk_contacts) values
    (1, 1),
    (2, 2);

insert into subject (subject_name, term) VALUES
    ('ИСБД', 5),
    ('Архитектура компьютера', 5),
    ('Операционные системы', 5);

insert into course (fk_subject, lector) values
    (1, 3);

insert into contacts_course (fk_course, fk_contacts) VALUES
    (1, 3);


insert into course_group (fk_course, fk_group) VALUES
    (1, 1),
    (1, 2);

insert into educational_materials (title, material_type) VALUES
    ('Как устроена СУБД', 'book'),
    ('Как устроены распределённые базы данных', 'book');

insert into materials_course (fk_course, fk_materials) VALUES
    (1, 1),
    (1, 2);

insert into tasks (title, description, task_type, date_of_pub, deadline) VALUES
    ('Лабораторная работа №1', 'Первая лаба', 'lab', CURRENT_TIMESTAMP, timestamp '2024-03-12 15:00:0');

insert into tasks_course (fk_course, fk_tasks) VALUES
    (1, 1);