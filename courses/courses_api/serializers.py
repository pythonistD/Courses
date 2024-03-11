from rest_framework import serializers

from .models import Student, Course, Tasks, Teacher, TasksCourse, EducationalMaterials, Contacts, News, NewsGroup, ContactsCourse, GroupContacts, ActualGroup


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = '__all__' 

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tasks
        fields = '__all__'
    
class TasksCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TasksCourse
        fields = '__all__'

class MaterialsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EducationalMaterials
        fields = '__all__'

class ContactsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contacts
        fields = '__all__'

class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'

class NewsGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsGroup
        fields = '__all__'

class ContactsCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactsCourse
        fields = '__all__'

class ContactsGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupContacts
        fields = '__all__'

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActualGroup
        fields = '__all__'