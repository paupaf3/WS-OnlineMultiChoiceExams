from django.contrib import admin
from .models import Exam, User, Grade

# Register your models here.

admin.site.register(User)
admin.site.register(Exam)
admin.site.register(Grade)