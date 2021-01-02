from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'online_multi_choice_exams/home.html')

def searchexam(request):
    return render(request, 'online_multi_choice_exams/searchexam.html')

def uploadexam(request):
    return render(request, 'online_multi_choice_exams/uploadexam.html')