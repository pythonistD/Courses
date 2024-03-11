create index ind_stud_gr_studid on student_group using
hash (fk_student);

create index ind_gr_contacts_acgr on group_contacts using
hash (actual_group);


create index ind_news_gr_acgr on news_group using
hash (fk_actual_group);


create index ind_course_gr_course on course_group using
hash (course);


create index ind_contacts_course_course on contacts_course using
hash (fk_course);

create index ind_material_course_course on materials_course using
hash (fk_course);

create index ind_task_course_course on tasks_course using
hash (fk_course);


create index ind_news_date_of_pub on news using
btree (date_of_pub);

create index ind_tasks_date_of_pub on tasks using
btree (date_of_pub);

create index ind_tasks_deadline on tasks using
btree (deadline);