from main.models import Student
from django.db import IntegrityError
from rest_framework.response import Response
from rest_framework import status 
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from main.serializers import StudentSerializerClass

class StudentsApiView(APIView):
    
    def get(self, request):
        students = Student.objects.all()
        serializer = StudentSerializerClass(students, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = StudentSerializerClass(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StudentApiView(APIView):
    
    def get_object(self, id):
        try:
            return Student.objects.get(pk=id)
        except Student.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id):
        student = self.get_object(id)
        serializer = StudentSerializerClass(student)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id):
        student = self.get_object(id)
        serializer = StudentSerializerClass(student, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        student = self.get_object(id)
        student.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)