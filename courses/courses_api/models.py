from django.db import models


class ActualGroup(models.Model):
    actual_group_id = models.AutoField(primary_key=True)
    group_name = models.CharField(max_length=100)
    mentor = models.ForeignKey('Teacher', models.CASCADE, db_column='mentor', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'actual_group'


class Contacts(models.Model):
    contacts_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=300)
    resource = models.TextField()

    class Meta:
        managed = False
        db_table = 'contacts'


class ContactsCourse(models.Model):
    contacts_course_id = models.AutoField(primary_key=True)
    fk_course = models.ForeignKey('Course', models.CASCADE, db_column='fk_course')
    fk_contacts = models.ForeignKey(Contacts, models.CASCADE, db_column='fk_contacts')

    class Meta:
        managed = False
        db_table = 'contacts_course'
        unique_together = (('fk_course', 'fk_contacts'),)


class Course(models.Model):
    course_id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=300, blank=True, null=True)
    fk_subject = models.ForeignKey('Subject', models.CASCADE, db_column='fk_subject')
    lector = models.ForeignKey('Teacher', models.CASCADE, db_column='lector')
    term = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'course'


class CourseGroup(models.Model):
    course_group = models.AutoField(primary_key=True)
    fk_course = models.ForeignKey(Course, models.CASCADE, db_column='fk_course')
    fk_group = models.ForeignKey(ActualGroup, models.CASCADE, db_column='fk_group')

    class Meta:
        managed = False
        db_table = 'course_group'
        unique_together = (('fk_course', 'fk_group'),)


class EdMId(models.Model):

    class Meta:
        managed = False
        db_table = 'ed_m_id'


class EducationalMaterials(models.Model):
    ed_m_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=300)
    url = models.TextField(blank=True, null=True)
    material_type = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'educational_materials'


class GroupContacts(models.Model):
    group_contacts_id = models.AutoField(primary_key=True)
    fk_actual_group = models.ForeignKey(ActualGroup, models.CASCADE, db_column='fk_actual_group')
    fk_contacts = models.ForeignKey(Contacts, models.CASCADE, db_column='fk_contacts')

    class Meta:
        managed = False
        db_table = 'group_contacts'


class Humans(models.Model):
    isu_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'humans'


class MaterialsCourse(models.Model):
    materials_course_id = models.AutoField(primary_key=True)
    fk_course = models.ForeignKey(Course, models.CASCADE, db_column='fk_course')
    fk_materials = models.ForeignKey(EducationalMaterials, models.CASCADE, db_column='fk_materials')

    class Meta:
        managed = False
        db_table = 'materials_course'
        unique_together = (('fk_course', 'fk_materials'),)


class News(models.Model):
    news_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=300)
    body = models.TextField()
    date_of_pub = models.DateTimeField()
    author = models.ForeignKey('Teacher', models.CASCADE, db_column='author')

    class Meta:
        managed = False
        db_table = 'news'


class NewsGroup(models.Model):
    news_group_id = models.AutoField(primary_key=True)
    fk_news = models.ForeignKey(News, models.CASCADE, db_column='fk_news')
    fk_actual_group = models.ForeignKey(ActualGroup, models.CASCADE, db_column='fk_actual_group')

    class Meta:
        managed = False
        db_table = 'news_group'
        unique_together = (('fk_news', 'fk_actual_group'),)


class Student(models.Model):
    student_id = models.AutoField(primary_key=True)
    fk_human = models.OneToOneField(Humans, models.CASCADE)
    course = models.SmallIntegerField()
    group_name = models.CharField(max_length=100)
    department = models.CharField(max_length=300)
    curriculum = models.CharField(max_length=300)

    class Meta:
        managed = False
        db_table = 'student'


class StudentGroup(models.Model):
    student_group_id = models.AutoField(primary_key=True)
    fk_student = models.ForeignKey(Student, models.CASCADE, db_column='fk_student')
    fk_actual_group = models.ForeignKey(ActualGroup, models.CASCADE, db_column='fk_actual_group')

    class Meta:
        managed = False
        db_table = 'student_group'
        unique_together = (('fk_student', 'fk_actual_group'),)


class Subject(models.Model):
    subject_id = models.AutoField(primary_key=True)
    subject_name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'subject'


class Tasks(models.Model):
    tasks_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=300)
    description = models.TextField()
    task_type = models.TextField()  # This field type is a guess.
    date_of_pub = models.DateTimeField()
    deadline = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'tasks'


class TasksCourse(models.Model):
    tasks_course_id = models.AutoField(primary_key=True)
    fk_course = models.ForeignKey(Course, models.CASCADE, db_column='fk_course')
    fk_tasks = models.ForeignKey(Tasks, models.CASCADE, db_column='fk_tasks')

    class Meta:
        managed = False
        db_table = 'tasks_course'
        unique_together = (('fk_course', 'fk_tasks'),)


class Teacher(models.Model):
    teacher_id = models.AutoField(primary_key=True)
    fk_humans = models.OneToOneField(Humans, models.CASCADE)
    department = models.CharField(max_length=300)

    class Meta:
        managed = False
        db_table = 'teacher'
