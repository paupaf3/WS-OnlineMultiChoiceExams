from django.urls import path
from .views import ExamView, ExamListView, ExamSearchView

urlpatterns = [
    path('exam/', ExamListView.as_view(), name='exam_list'),
    path('exam/<int:pk>/', ExamView.as_view(), name='exam'),
    path('exam/search/', ExamSearchView.as_view(), name='exam_search'),

]