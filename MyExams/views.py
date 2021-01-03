from django.shortcuts import render
from .models import Exam, User, Grade
from django.views import View
from django.http import JsonResponse
from django.forms import model_to_dict

# Create your views here.

class ExamListView(View):
    def get(self, request):
        examList = Exam.objects.all()
        return JsonResponse(list(examList.values()), safe=False) 
        #False per indicar que no tornem un objecte Json, tornem array dobjectes Json

class ExamView(View):
    def get(self, request, pk):
        exam = Exam.objects.get(pk=pk)
        return JsonResponse(model_to_dict(exam))

class ExamSearchView(View):
    #Búsqueda per paràmetres ex: /api/exam/search/?description=exam
    def get(self, request):
        examList = Exam.objects.filter(description__contains=request.GET['description'])
        return JsonResponse(list(examList.values()), safe=False) 
