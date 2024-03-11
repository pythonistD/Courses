create or replace function get_courses(isu_id int)
returns table (course text) as 
$$
        select course_id, subject_name from course_group as c_g
        join course as c on c.course_id = c_g.fk_course
        join subject as sub on sub.subject_id = c.fk_subject
        where fk_group in
        (select fk_actual_group from student_group 
        where fk_student = isu_id);
$$language sql;

select subject from get_courses(1);

create or replace function get_courses_teacher(t_id int)
returns table (
    course_id int,
    course_name varchar,
    subject varchar,
    term smallint
    ) as 
$$
    declare

    begin
    return query
        select c.course_id, c.course_name, su.subject_name, c.term from teacher as tea
        join course as c on c.lector = tea.teacher_id
        join subject as su on c.fk_subject = su.subject_id
        where tea.teacher_id = t_id;
    end
$$ language plpgsql;

drop FUNCTION get_courses_teacher;

select * from get_courses_teacher(10);

drop FUNCTION get_courses;

create or replace function get_practice_teacher(t_id int)
returns table (
    actual_group_id int,
    group_name varchar,
    subject varchar,
    term smallint
    ) as 
$$
    declare

    begin
    return query
        select ac.actual_group_id, ac.group_name, sub.subject_name, c.term from actual_group as ac
        join course_group as cg on ac.actual_group_id = cg.fk_group
        join course as c on c.course_id = cg.fk_course
        join subject as sub on c.fk_subject = sub.subject_id 
        where ac.mentor = t_id;
    end
$$ language plpgsql;
select * from get_practice_teacher(1);

create or replace function create_ed_material(title char, url text, material_type material_type, course int)
returns int as
$$
    DECLARE
        materials_id int;
    BEGIN
        insert into educational_materials (title, url, material_type) VALUES
            (title, url, material_type);

        select ed_m_id into materials_id from educational_materials
        where ed_m_id = (select max(ed_m_id) from educational_materials);

        raise notice 'materials_id: %', materials_id;

        insert into materials_course (fk_course, fk_materials) VALUES
            (course, materials_id);
        return 1;
    END
$$ language plpgsql;

drop function create_ed_material;
select create_ed_material('test', null, 'book', 1);

create or replace function delete_all_material(ed_id int)
returns bool as
$$
    begin
        delete from educational_materials
        where ed_m_id = ed_id;
        return true;
    end
$$ language plpgsql;


select ed_m_id from educational_materials
where ed_m_id = (select max(ed_m_id) from educational_materials);

select delete_all_material(10);

create or replace function delete_material_from_course(ed_id int, course_id int)
returns bool as
$$
    BEGIN
        delete from materials_course
        where fk_course = course_id and fk_materials = ed_id;
        return true;
    END
$$ language plpgsql;

select * from materials_course;

create or replace function create_task(title text, description text, task_type task_type, date_of_pub timestamptz, deadline timestamp, course int)
returns bool as
$$
    DECLARE
        t_id int;
    BEGIN
        insert into tasks (title, description, task_type, date_of_pub, deadline) VALUES
            (title, description, task_type, date_of_pub, deadline);

        select tasks_id into t_id from tasks
        where tasks_id = (select max(tasks_id) from tasks);

        insert into tasks_course (fk_course, fk_tasks) VALUES
            (course, t_id);
        return TRUE;
    END
$$ language plpgsql;

select * from create_task('Lab1', 'Изучить, что такое heartbleed', 'lab', NOW(), '2024-02-20 15:20:0', 3);


create or replace function delete_all_task(t_id int)
returns bool as
$$
    begin
        delete from tasks
        where tasks_id = t_id;
        return true;
    end
$$ language plpgsql;

select delete_all_task(5);

create trigger new_student_new_group
after insert on student 
for each row execute procedure student_new_group();

create or replace function student_new_group()
returns trigger as
$$
    DECLARE
        gr student.group_name%type;
        st_id student.student_id%type;
        ac_gr_id int;
    begin
        gr := new.group_name;
        st_id := new.student_id;

        select actual_group_id into ac_gr_id from actual_group
        where group_name = gr;

        if not found then
        insert into actual_group (group_name) values
        (gr);

        select actual_group_id into ac_gr_id from actual_group
        where group_name = gr;
        end if;

        insert into student_group (fk_student, fk_actual_group) values
        (st_id, ac_gr_id);

        return new;
    end;
$$ language plpgsql;


create or replace function create_contact(title text, resource text, course int)
returns bool as
$$
    DECLARE
        t_id int;
    BEGIN
        insert into contacts (title, resource) VALUES
            (title, resource);

        select contacts_id into t_id from contacts
        where contacts_id = (select max(contacts_id) from contacts);

        insert into contacts_course (fk_course, fk_contacts) VALUES
            (course, t_id);
        return TRUE;
    END
$$ language plpgsql;


create or replace function delete_all_contacts(con_id int)
returns bool as
$$
    begin
        delete from contacts
        where contacts_id = con_id;
        return true;
    end
$$ language plpgsql;


create or replace function create_gr_contact(title text, resource text, ac_group int)

returns bool as
$$
    DECLARE
        t_id int;
    BEGIN
        insert into contacts (title, resource) VALUES
            (title, resource);

        select contacts_id into t_id from contacts
        where contacts_id = (select max(contacts_id) from contacts);

        insert into group_contacts (fk_actual_group, fk_contacts) VALUES
            (ac_group, t_id);
        return TRUE;
    END
$$ language plpgsql;


create or replace function create_news(title text, body text, date_of_pub timestamptz, author int, ac_gr int)
returns bool as
$$
    DECLARE
        t_id int;
    BEGIN
        insert into news (title, body, date_of_pub, author) VALUES
            (title, body, date_of_pub, author);

        select news_id into t_id from news
        where news_id = (select max(news_id) from news);

        insert into news_group (fk_news, fk_actual_group) VALUES
            (t_id, ac_gr);
        return TRUE;
    END
$$ language plpgsql;

