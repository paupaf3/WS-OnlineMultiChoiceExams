from django.db import models

# Create your models here.
class Exam(models.Model):
    description=models.CharField(max_length=250)
    time=models.TimeField()
    date=models.DateField()
    location=models.CharField(max_length=40)

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
    exam=models.OneToOneField(Exam, on_delete=models.PROTECT)
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    grade=models.IntegerField()