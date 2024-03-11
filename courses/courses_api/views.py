from rest_framework import generics, views, serializers
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.utils import timezone
from django.db import transaction, models
from .models import Student, Tasks, Course, TasksCourse, Teacher, EducationalMaterials, MaterialsCourse, Contacts, News, NewsGroup, ContactsCourse, ActualGroup, GroupContacts, Subject
from .serializers import StudentSerializer, CourseSerializer, TaskSerializer, TeacherSerializer, TasksCourseSerializer, MaterialsSerializer, ContactsSerializer, NewsSerializer, NewsGroupSerializer, ContactsCourseSerializer, ContactsGroupSerializer, GroupSerializer
from .utils import get_courses_teacher, get_practice_teacher, make_teacher_detailed, get_name, one_to_many_find
# Create your views here.

class StudentsListView(generics.ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class TeachersListView(generics.ListAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

class CoursesListView(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class TeacherCoursesList(views.APIView):
    def get(self, request, teacher_id):
        courses = get_courses_teacher(teacher_id)
        return Response(courses)
    
class MaterialsListView(generics.ListAPIView):
    queryset = EducationalMaterials.objects.all()
    serializer_class = MaterialsSerializer

class ContactsListView(generics.ListAPIView):
    queryset = Contacts.objects.all()
    serializer_class = ContactsSerializer

class NewsListView(generics.ListAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer

class GroupsListView(generics.ListAPIView):
    queryset = ActualGroup.objects.all()
    serializer_class = GroupSerializer

class TeacherCourseContacts(views.APIView):
    def get(self, request, course_id):
        filter1 = {
            'fk_course': 0
        }
        filter2 = {
            'contacts_id__in': []
        }
        course_name = generics.get_object_or_404(Course, pk=course_id).course_name
        resp = one_to_many_find(Course, ContactsCourse, Contacts, ContactsSerializer,
                         course_id, 'fk_contacts_id', filter1, filter2)
        for r in resp:
            r['course_name'] = course_name
        return Response(resp)

    @transaction.atomic
    def post(self, request, course_id):
        course = generics.get_object_or_404(Course, pk=course_id)
        new_contact_ser = ContactsSerializer(data=request.data)
        new_contact_ser.is_valid()
        new_contact = new_contact_ser.save()

        new_contact_course = ContactsCourse(fk_course=course, fk_contacts=new_contact)
        new_contact_course.save()
        return Response(ContactsCourseSerializer(new_contact_course).data)

    def delete(self, request, course_id):
        if 'contacts_id' not in request.data:
            raise ValidationError('To delete contact from course you have to provide contact_id!')
        c_id = request.data['contacts_id']
        contact_course = generics.get_object_or_404(ContactsCourse, fk_course=course_id, fk_contacts=c_id)
        contact = contact_course.fk_contacts
        resp = ContactsSerializer(contact).data
        contact_course.delete()
        return Response(resp)

class TeacherPractContacts(views.APIView):
    def get(self, request, group_id):
        filter1 = {
            'fk_actual_group': 0
        }
        filter2 = {
            'contacts_id__in': []
        }
        group_name = generics.get_object_or_404(ActualGroup, pk=group_id).group_name
        resp = one_to_many_find(ActualGroup, GroupContacts, Contacts, ContactsSerializer,
                         group_id, 'fk_contacts_id', filter1, filter2)
        for r in resp:
            r['group_name'] = group_name
        return Response(resp)

    @transaction.atomic
    def post(self, request, group_id):
        group = generics.get_object_or_404(ActualGroup, pk=group_id)
        new_contact_ser = ContactsSerializer(data=request.data)
        new_contact_ser.is_valid()
        new_contact = new_contact_ser.save()

        new_contact_group = GroupContacts(fk_actual_group=group, fk_contacts=new_contact)
        new_contact_group.save()
        return Response(ContactsGroupSerializer(new_contact_group).data)

    def delete(self, request, group_id):
        if 'contacts_id' not in request.data:
            raise ValidationError('To delete contact from course you have to provide contact_id!')
        c_id = request.data['contacts_id']
        contact_group = generics.get_object_or_404(GroupContacts, fk_actual_group=group_id, fk_contacts=c_id)
        contact = contact_group.fk_contacts
        resp = ContactsSerializer(contact).data
        contact_group.delete()
        return Response(resp)
    
class ContactsCourseView(generics.CreateAPIView):
    queryset = ContactsCourse.objects.all()
    serializer_class= ContactsCourseSerializer

class TeacherCourseTasks(views.APIView):
    def get(self, request, course_id):
        course = generics.get_object_or_404(Course, course_id=course_id)
        task_course = TasksCourse.objects.filter(fk_course=course.course_id).values()
        task_ids = []
        for t in task_course:
            task_ids.append(t["fk_tasks_id"])
        tasks = Tasks.objects.filter(tasks_id__in=task_ids)
        ser = TaskSerializer(tasks, many=True)
        out_d = ser.data
        for d in out_d:
            d["course name"] = course.course_name
        return Response(out_d)

    @transaction.atomic
    def post(self, request, course_id):
        data = request.data
        if 'date_of_pub' not in data:
            data['date_of_pub'] = timezone.now()
            data['date_of_pub'].strftime('%Y-%m-%d %H:%M:%S')
        print(data['date_of_pub'])
        new_task = Tasks(title=data['title'], description=data['description'], task_type=data['task_type'],
                         date_of_pub=data['date_of_pub'], deadline=data['deadline'])
        new_task.save()
        course = generics.get_object_or_404(Course, pk=course_id)
        TasksCourse(fk_course=course, fk_tasks=new_task).save()
        return Response(TaskSerializer(new_task).data)

    def delete(self, request, course_id):
        if 'task_id' not in request.data:
            raise ValidationError('To delete task from course you have to provide task_id!')
        t_id = request.data['task_id']
        task_course = generics.get_object_or_404(TasksCourse, fk_course=course_id, fk_tasks=t_id)
        task = task_course.fk_tasks
        resp = TaskSerializer(task).data
        task_course.delete()
        return Response(resp)
    
class MyBaseView:
    model_object:models.Model 
    serializer:serializers.BaseSerializer 

    def __init__(self, model_object, serializer) -> None:
        self.model_object = model_object
        self.serializer = serializer

    def get(self, id) -> Response:
        obj = generics.get_object_or_404(self.model_object, pk=id)
        resp = self.serializer(obj).data
        return Response(resp)
    def post(self, data, *args, **kwargs) -> Response:
        new_obj = self.serializer(data=data)
        new_obj.is_valid(raise_exception=True)
        new_obj.save()
        return Response(new_obj.data)

    def put(self, data, id) -> Response:
        obj = generics.get_object_or_404(self.model_object, pk=id)
        ser = self.serializer(data=data, instance=obj)
        ser.is_valid()
        ser.save()
        return Response(ser.data)

    def delete(self, id) -> Response:
        obj = generics.get_object_or_404(self.model_object, pk=id)
        resp = self.serializer(obj).data
        obj.delete()
        return Response(resp)

class MaterialView(views.APIView):
# Как првильно работать с переопределением __init__ у классов наследников
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.mybase = MyBaseView(EducationalMaterials, MaterialsSerializer)

    def get(self, request, material_id):
        return self.mybase.get(material_id)
    def post(self, request, material_id):
        if 'url' not in request.data:
            request.data['url'] = ''
        return self.mybase.post(request.data)
    def put(self, request, material_id):
        return self.mybase.put(request.data, material_id)
    def delete(self, request, material_id):
        return self.mybase.delete(material_id)

class ContactsView(views.APIView):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.mybase = MyBaseView(Contacts, ContactsSerializer)

    def get(self, request, contact_id):
        return self.mybase.get(contact_id)
    def post(self, request, contact_id):
        return self.mybase.post(request.data)
    def put(self, request, contact_id):
        return self.mybase.put(request.data, contact_id)
    def delete(self, request, contact_id):
        return self.mybase.delete(contact_id)

class NewsView(views.APIView):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.mybase = MyBaseView(News, NewsSerializer)

    def get(self, request, news_id):
        return self.mybase.get(news_id)
    def post(self, request, news_id):
        if 'date_of_pub' not in request.data:
            request.data['date_of_pub'] = timezone.now()
            request.data['date_of_pub'].strftime('%Y-%m-%d %H:%M:%S')
        return self.mybase.post(request.data)
    def put(self, request, news_id):
        return self.mybase.put(request.data, news_id)
    def delete(self, request, news_id):
        return self.mybase.delete(news_id)
    
class NewsGroupCreateView(generics.CreateAPIView):
    queryset = NewsGroup.objects.all()
    serializer_class = NewsGroupSerializer

    
class TasksView(views.APIView):
    def get(self, request, task_id):
        task = generics.get_object_or_404(Tasks, tasks_id=task_id)
        resp = TaskSerializer(task).data
        return Response(resp)

    def post(self, request, task_id):
        if 'date_of_pub' not in request.data:
            request.data['date_of_pub'] = timezone.now()
            request.data['date_of_pub'].strftime('%Y-%m-%d %H:%M:%S')
        new_task = TaskSerializer(data=request.data)
        new_task.is_valid(raise_exception=True)
        new_task.save()
        return Response(new_task.data)

    def put(self, request, task_id):
        task = generics.get_object_or_404(Tasks, tasks_id=task_id)
        ser = TaskSerializer(data=request.data, instance=task)
        ser.is_valid()
        ser.save()
        return Response(ser.data)

    def delete(self, request, task_id):
        task = generics.get_object_or_404(Tasks, tasks_id=task_id)
        resp = TaskSerializer(task).data
        task.delete()
        return Response(resp)
    
class TasksCourseView(generics.CreateAPIView):
    queryset=TasksCourse.objects.all()
    serializer_class = TasksCourseSerializer

    


class TeacherCourseEducationalMaterials(views.APIView):
    def get(self, request, course_id):
        course = generics.get_object_or_404(Course, course_id=course_id)
        material_course = MaterialsCourse.objects.filter(fk_course=course.course_id).values()
        mat_ids = []
        for t in material_course:
            mat_ids.append(t["fk_materials"])
        materials = EducationalMaterials.objects.filter(ed_m_id__in=mat_ids)
        ser = MaterialsSerializer(materials, many=True)
        out_d = ser.data
        for d in out_d:
            d["course name"] = course.course_name
        return Response(out_d)

    @transaction.atomic
    def post(self, request, course_id):
        data = request.data
        if 'date_of_pub' not in data:
            data['date_of_pub'] = timezone.now()
            data['date_of_pub'].strftime('%Y-%m-%d %H:%M:%S')
        print(data['date_of_pub'])
        new_task = Tasks(title=data['title'], description=data['description'], task_type=data['task_type'],
                         date_of_pub=data['date_of_pub'], deadline=data['deadline'])
        new_task.save()
        course = generics.get_object_or_404(Course, pk=course_id)
        TasksCourse(fk_course=course, fk_tasks=new_task).save()
        return Response(TaskSerializer(new_task).data)

    def delete(self, request, course_id):
        if 'task_id' not in request.data:
            raise ValidationError('To delete task from course you have to provide task_id!')
        t_id = request.data['task_id']
        task_course = generics.get_object_or_404(TasksCourse, fk_course=course_id, fk_tasks=t_id)
        task = task_course.fk_tasks
        resp = TaskSerializer(task).data
        task_course.delete()
        return Response(resp)

    
class TasksView(views.APIView):
    def get(self, request, task_id):
        task = generics.get_object_or_404(Tasks, tasks_id=task_id)
        resp = TaskSerializer(task).data
        return Response(resp)

    def post(self, request, task_id):
        if 'date_of_pub' not in request.data:
            request.data['date_of_pub'] = timezone.now()
            request.data['date_of_pub'].strftime('%Y-%m-%d %H:%M:%S')
        new_task = TaskSerializer(data=request.data)
        new_task.is_valid(raise_exception=True)
        new_task.save()
        return Response(new_task.data)

    def put(self, request, task_id):
        task = generics.get_object_or_404(Tasks, tasks_id=task_id)
        ser = TaskSerializer(data=request.data, instance=task)
        ser.is_valid()
        ser.save()
        return Response(ser.data)

    def delete(self, request, task_id):
        task = generics.get_object_or_404(Tasks, tasks_id=task_id)
        resp = TaskSerializer(task).data
        task.delete()
        return Response(resp)
    
class TasksCourseView(generics.CreateAPIView):
    queryset=TasksCourse.objects.all()
    serializer_class = TasksCourseSerializer
        

class TeacherPracticeList(views.APIView):
    def get(self, request, teacher_id):
        practice = get_practice_teacher(teacher_id)
        return Response(practice)

class TeacherDetailedView(views.APIView):
    def get(self, request, teacher_id):
        teacher = Teacher.objects.get(pk=teacher_id)
        practice = get_practice_teacher(teacher_id)
        courses = get_courses_teacher(teacher_id)
        print(teacher.fk_humans.name)
        name = teacher.fk_humans.name
        last_name = teacher.fk_humans.last_name
        resp = make_teacher_detailed(name=name, last_name=last_name, courses=courses, practice=practice)
        return Response(resp)

class TeacherPractNews(views.APIView):
    def get(self, request, group_id):
        filter1 = {
            'fk_actual_group': 0
        }
        filter2 = {
            'news_id__in': []
        }
        group_name = generics.get_object_or_404(ActualGroup, pk=group_id).group_name
        resp = one_to_many_find(ActualGroup, NewsGroup, News, NewsSerializer,
                         group_id, 'fk_news_id', filter1, filter2)
        for r in resp:
            r['group_name'] = group_name
        return Response(resp)

    @transaction.atomic
    def post(self, request, group_id):
        group = generics.get_object_or_404(ActualGroup, pk=group_id)
        if 'date_of_pub' not in request.data:
            request.data['date_of_pub'] = timezone.now()
            request.data['date_of_pub'].strftime('%Y-%m-%d %H:%M:%S')
        new_news_ser = NewsSerializer(data=request.data)
        new_news_ser.is_valid(raise_exception=True)
        new_news = new_news_ser.save()

        new_news_group = NewsGroup(fk_actual_group=group, fk_news=new_news)
        new_news_group.save()
        return Response(NewsGroupSerializer(new_news_group).data)

    def delete(self, request, group_id):
        if 'news_id' not in request.data:
            raise ValidationError('To delete news from group you have to provide news_id!')
        n_id = request.data['news_id']
        group_news = generics.get_object_or_404(NewsGroup, fk_actual_group=group_id, fk_news=n_id)
        news = group_news.fk_news
        resp = NewsSerializer(news).data
        group_news.delete()
        return Response(resp)

class StudentCoursesList(views.APIView):
    def get(self, request, student_id):
        student = generics.get_object_or_404(Student, pk=student_id)
        student_groups = student.studentgroup_set.all()
        courses = []
        for s in student_groups:
            # На какие курсы записана текущая группа:
            course_group = s.fk_actual_group.coursegroup_set.all()
            if len(course_group) == 0:
                continue
            for c in course_group:
                courses.append(c.fk_course)
        resp = CourseSerializer(courses, many=True).data
        for r in resp:
            r['subject_name'] = Subject.objects.get(pk=r['fk_subject']).subject_name
        return Response(resp)

class StudentPracticeList(views.APIView):
    def get(self, request, student_id):
        student = generics.get_object_or_404(Student, pk=student_id)
        student_groups = student.studentgroup_set.all()
        groups = []
        for s in student_groups:
            groups.append(s.fk_actual_group)
        resp = GroupSerializer(groups, many=True).data
        return Response(resp)
