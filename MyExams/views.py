import os
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import HttpResponse

from .models import Exam, User, Grade
from .serializers import ExamSerializer, GradeSerializer, UserSerializer

'''
#####################################################################################
                                    EXAM
#####################################################################################
'''

#GET d'un exam en concret per ID (pk=primary key)
@api_view(['GET', ])
def exam_view(request, pk):
    try:
        exam = Exam.objects.get(pk=pk)
    except Exam.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = ExamSerializer(exam)
        return Response(serializer.data)

#GET descarga d'un exam en concret per ID (pk=primary key)
@api_view(['GET', ])
def exam_download_view(request, pk):
    try:
        exam = Exam.objects.get(pk=pk)
    except Exam.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        file = os.path.basename(exam.exam_file.name)
        with open("exam_files/"+file, 'r') as file:
            response = HttpResponse(file, content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename=exam_file.csv'
            return response

#GET de la llista amb tots els examens
@api_view(['GET', ])
def exam_list_view(request):
    try:
        examList = Exam.objects.all()
    except Exam.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = ExamSerializer(examList, many=True)
        return Response(serializer.data)

#GET de la busqueda d'un exam per descripcio
#busca que la descripcio contingui la busqueda realitzada (description__contains)
@api_view(['GET', ])
def exam_search_view(request):
    try:
        examList = Exam.objects.filter(description__contains=request.GET['description'])
    except Exam.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = ExamSerializer(examList, many=True)
        return Response(serializer.data)

#PUT modificar la descripcio d'un examen en concret per ID
@api_view(['PATCH', ])
def exam_update_view(request, pk):
    try:
        exam = Exam.objects.get(pk=pk)
    except Exam.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "PATCH":
        #Partial per permetre modificar sol la descripcio de l'exam
        serializer = ExamSerializer(exam, data=request.data, partial=True)
        data = {}
        #Per comprovar que compleix amb la forma
        if serializer.is_valid():
            serializer.save()
            data["success"] = "Update Successful!"
            return Response(data=data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#DELETE eliminar exam per ID
@api_view(['DELETE', ])
def exam_delete_view(request, pk):
    try:
        exam = Exam.objects.get(pk=pk)
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

#POST crear exam
@api_view(['POST', ])
def exam_create_view(request):
    exam = Exam()
    if request.method == "POST":
        serializer = ExamSerializer(exam, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)   

'''
#####################################################################################
                                    GRADE
#####################################################################################
'''

#GET veure nota per id d'examen i id d'usuari 
@api_view(['GET', ])
def grade_view(request, exam, user):
    try:
        grade = Grade.objects.get(exam=exam, user=user)
    except Grade.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = GradeSerializer(grade)
        return Response(serializer.data)

#GET descargar nota per id d'examen i id d'usuari 
@api_view(['GET', ])
def grade_download_view(request, exam, user):
    try:
        grade = Grade.objects.get(exam=exam, user=user)
    except Grade.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        file = os.path.basename(grade.grade_file.name)
        with open("grade_files/"+file, 'r') as file:
            response = HttpResponse(file, content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename=grade_file.csv'
            return response

#GET de la llista amb totes les notes
@api_view(['GET', ])
def grade_list_view(request):
    try:
        gradeList = Grade.objects.all()
    except Grade.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = GradeSerializer(gradeList, many=True)
        return Response(serializer.data)

#GET de la busqueda de notes per id d'usuari
@api_view(['GET', ])
def grade_user_view(request, user):
    try:
        gradeList = Grade.objects.filter(user=user)
    except Grade.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = GradeSerializer(gradeList, many=True)
        return Response(serializer.data)


#DELETE eliminar nota per examID i userID
@api_view(['DELETE', ])
def grade_delete_view(request, exam, user):
    try:
        grade = Grade.objects.get(exam=exam, user=user)
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

#POST crear notes
@api_view(['POST', ])
def grade_create_view(request):
    grade = Grade()
    if request.method == "POST":
        serializer = GradeSerializer(grade, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 