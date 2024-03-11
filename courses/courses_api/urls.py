from django.urls import path, include

from .views import StudentsListView, TeacherCoursesList, TeacherPracticeList, TeacherCourseTasks, TeachersListView, \
                    TeacherDetailedView, TasksView, TasksCourseView, TeacherCourseEducationalMaterials, CoursesListView, \
                    MaterialView, MaterialsListView, ContactsView, NewsView, TeacherCourseContacts, TeacherPractNews, TeacherPractContacts, ContactsListView, \
                    NewsListView, NewsGroupCreateView,  ContactsCourseView, GroupsListView, StudentCoursesList, StudentPracticeList

urlpatterns = [
    path('students', StudentsListView.as_view()),
    path('teachers', TeachersListView.as_view()),
    path('courses', CoursesListView.as_view()),
    path('groups', GroupsListView.as_view()),
    path('materials', MaterialsListView.as_view()),
    path('contacts', ContactsListView.as_view()),
    path('news', NewsListView.as_view()),
    path('teacher/lec/<int:teacher_id>', TeacherCoursesList.as_view()),
    path('teacher/pract/<int:teacher_id>', TeacherPracticeList.as_view()),
    path('student/lec/<int:student_id>', StudentCoursesList.as_view()),
    path('student/pract/<int:student_id>', StudentPracticeList.as_view()),
    path('teacher/course/<int:course_id>/tasks', TeacherCourseTasks.as_view()),
    path('teacher/course/<int:course_id>/materials', TeacherCourseEducationalMaterials.as_view()),
    path('teacher/course/<int:course_id>/contacts', TeacherCourseContacts.as_view()),
    path('teacher/pract/<int:group_id>/news', TeacherPractNews.as_view()),
    path('teacher/pract/<int:group_id>/contacts', TeacherPractContacts.as_view()),
    path('tasks/<int:task_id>', TasksView.as_view()),
    path('materials/<int:material_id>', MaterialView.as_view()),
    path('contacts/<int:contact_id>', ContactsView.as_view()),
    path('news/<int:news_id>', NewsView.as_view()),
    path('news/add_to_group', NewsGroupCreateView.as_view()),
    path('tasks/add_to_course', TasksCourseView.as_view()),
    path('contacts/add_to_course', ContactsCourseView.as_view()),
    path('teacher/<int:teacher_id>', TeacherDetailedView.as_view())
]