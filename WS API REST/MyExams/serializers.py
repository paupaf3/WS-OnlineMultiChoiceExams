from rest_framework import serializers
from .models import Exam, User, Grade

#To return JSON
class ExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = ['id', 'description', 'time', 'date', 'location', 'exam_file']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'role']

class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = ['id', 'exam', 'user', 'grade_file']