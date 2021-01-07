from django.db import models

# Create your models here.
class Exam(models.Model):
    description=models.CharField(max_length=250)
    time=models.TimeField()
    date=models.DateField()
    location=models.CharField(max_length=40)
    exam_file=models.FileField(upload_to="exam_files/", unique=True)
    #exam_file=models.FileField(default='example_files/exam_files/noexam.csv')

class User(models.Model):
    STUDENT = 'student'
    PROFESSOR = 'professor'
    ROLES = (
        (STUDENT, 'Student'),
        (PROFESSOR, 'Professor'),
    )
    name=models.CharField(max_length=60)
    role=models.TextField(choices=ROLES, default=STUDENT)

class Grade(models.Model):
    exam=models.ForeignKey(Exam, on_delete=models.PROTECT)
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    grade_file=models.FileField(upload_to="grade_files/")
    #grade_file=models.FileField(default='example_files/exam_files/nograde.csv')
    class Meta:
        unique_together = ('exam', 'user',)
