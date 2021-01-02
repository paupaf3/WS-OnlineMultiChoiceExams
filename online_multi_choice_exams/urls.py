from django.urls import path, include
from .views import home, searchexam, uploadexam

urlpatterns = [
    path('', home, name="home"),
    path('searchexam/', searchexam, name="searchexam"), 
    path('uploadexam/', uploadexam, name="uploadexam"), 
]
