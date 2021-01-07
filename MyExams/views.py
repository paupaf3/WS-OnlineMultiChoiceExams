import os
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import HttpResponse

from .models import Exam, User, Grade
from .serializers import ExamSerializer, GradeSerializer, UserSerializer


#####################################################################################
                                    #EXAM
#####################################################################################

@api_view(['GET', ])
def exam_view(request, exam_id):
    """
    Description: Shows an exam
    Input: Exam ID(exam_id)
    Output: Exam json
    """
    try:
        exam = Exam.objects.get(pk=exam_id)
    except Exam.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = ExamSerializer(exam)
        return Response(serializer.data)

@api_view(['GET', ])
def exam_download_view(request, exam_id):
    """
    Description: Downloads an exam
    Input: Exam ID(exam_id)
    Output: Exam csv file
    """
    try:
        exam = Exam.objects.get(pk=exam_id)
    except Exam.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        file = os.path.basename(exam.exam_file.name)
        with open("exam_files/"+file, 'r') as file:
            response = HttpResponse(file, content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename=exam_file.csv'
            return response

@api_view(['GET', ])
def exam_list_view(request):
    """
    Description: Shows all the exams
    Output: List of exams json
    """
    try:
        examList = Exam.objects.all()
    except Exam.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = ExamSerializer(examList, many=True)
        return Response(serializer.data)

@api_view(['GET', ])
def exam_search_view(request):
    """
    Description: Shows list of exams that the description contains the search
    Input: Keyword of the search
    Output: List of exams json
    """
    try:
        examList = Exam.objects.filter(description__contains=request.GET['description'])
    except Exam.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = ExamSerializer(examList, many=True)
        return Response(serializer.data)

@api_view(['PATCH', ])
def exam_update_view(request, exam_id):
    """
    Description: Modify description of an exam
    Input: Data in the request(the description) and Exam ID(exam_id)
    Output: Exam json
    """
    try:
        exam = Exam.objects.get(pk=exam_id)
    except Exam.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "PATCH":
        serializer = ExamSerializer(exam, data=request.data, partial=True)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data["success"] = "Update Successful!"
            return Response(data=data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE', ])
def exam_delete_view(request, exam_id):
    """
    Description: Deletes an exam
    Input: Exam ID(exam_id)
    """
    try:
        exam = Exam.objects.get(pk=exam_id)
    except Exam.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "DELETE":
        operation = exam.delete()
        data = {}
        if operation:
            data["success"] = "Delete Successful!"
        else:
            data["failure"] = "Delete Failed! Exam has grades!"
        return Response(data=data)

@api_view(['POST', ])
def exam_create_view(request):
    """
    Description: Create an exam
    Input: Data necessary to create the exam
    Output: Exam json
    """
    exam = Exam()
    if request.method == "POST":
        serializer = ExamSerializer(exam, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)   


#####################################################################################
                                    #GRADE
#####################################################################################

@api_view(['GET', ])
def grade_view(request, exam_id, user_id):
    """
    Description: Shows grade using json
    Input: Exam ID(exam_id) and User ID(user_id)
    Output: Grade json
    """
    try:
        grade = Grade.objects.get(exam=exam_id, user=user_id)
    except Grade.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = GradeSerializer(grade)
        return Response(serializer.data)

@api_view(['GET', ])
def grade_download_view(request, exam_id, user_id):
    """
    Description: Download the grade file of a grade
    Input: Exam ID(exam_id) and User ID(user_id)
    Output: Grade csv file
    """
    try:
        grade = Grade.objects.get(exam=exam_id, user=user_id)
    except Grade.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        file = os.path.basename(grade.grade_file.name)
        with open("grade_files/"+file, 'r') as file:
            response = HttpResponse(file, content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename=grade_file.csv'
            return response

@api_view(['GET', ])
def grade_list_view(request):
    """
    Description: Shows a list of all the grades
    Output: List of grades json
    """
    try:
        gradeList = Grade.objects.all()
    except Grade.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = GradeSerializer(gradeList, many=True)
        return Response(serializer.data)

@api_view(['GET', ])
def grade_user_view(request, user_id):
    """
    Description: Shows a list of all the grades a particular User has
    Input: User ID (user)
    Output: List of grades json
    """
    try:
        gradeList = Grade.objects.filter(user=user_id)
    except Grade.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = GradeSerializer(gradeList, many=True)
        return Response(serializer.data)

@api_view(['DELETE', ])
def grade_delete_view(request, exam_id, user_id):
    """
    Description: Deletes a grade
    Input: Exam ID(exam_id) and User ID(user_id)
    """
    try:
        grade = Grade.objects.get(exam=exam_id, user=user_id)
    except Grade.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "DELETE":
        operation = grade.delete()
        data = {}
        if operation:
            data["success"] = "Delete Successful!"
        else:
            data["failure"] = "Delete Failed!"
        return Response(data=data)

@api_view(['POST', ])
def grade_create_view(request):
    """
    Description: Create a grade
    Input: Data necessary to create the grade
    Output: Grade json
    """
    grade = Grade()
    if request.method == "POST":
        serializer = GradeSerializer(grade, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 