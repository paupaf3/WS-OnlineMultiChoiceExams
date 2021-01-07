from django.urls import path
from .views import (
    exam_view, 
    exam_list_view, 
    exam_search_view, 
    exam_create_view, 
    exam_delete_view, 
    exam_update_view, 
    exam_download_view, 
    grade_view,
    grade_list_view, 
    grade_create_view, 
    grade_user_view, 
    grade_delete_view, 
    grade_download_view, 
    )

urlpatterns = [
    #EXAM
    path('exam/', exam_list_view, name='exam_list'),
    path('exam/search/', exam_search_view, name='exam_search'),
    path('exam/upload/', exam_create_view, name='exam_create'),
    path('exam/<int:pk>/', exam_view, name='exam'),
    path('exam/<int:pk>/delete/', exam_delete_view, name='exam_delete'),
    path('exam/<int:pk>/update/', exam_update_view, name='exam_update'),
    path('exam/<int:pk>/download/', exam_download_view, name='exam_download'),

    
    #GRADE
    path('grade/', grade_list_view, name='grade_list'),
    path('grade/upload/', grade_create_view, name='grade_create'),
    path('grade/<int:user>/', grade_user_view, name='grade_user_list'),
    path('grade/<int:user>/<int:exam>/', grade_view, name='grade'),
    path('grade/<int:user>/<int:exam>/delete/', grade_delete_view, name='grade_delete'),
    path('grade/<int:user>/<int:exam>/download/', grade_download_view, name='grade_download'),

]