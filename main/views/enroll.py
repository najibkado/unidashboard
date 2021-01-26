from main.models import EnrolledStudent
from django.db import IntegrityError
from rest_framework.response import Response
from rest_framework import status 
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from main.serializers import EnrolledStudentSerializerClass

class EnrolledStudentsApiView(APIView):
    
    def get(self, request):
        students = EnrolledStudent.objects.all()
        serializer = EnrolledStudentSerializerClass(students, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = EnrolledStudentSerializerClass(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EnrolledStudentApiView(APIView):
    
    def get_object(self, id):
        try:
            return EnrolledStudent.objects.get(pk=id)
        except EnrolledStudent.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id):
        student = self.get_object(id)
        serializer = EnrolledStudentSerializerClass(student)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id):
        student = self.get_object(id)
        serializer = EnrolledStudentSerializerClass(student, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        student = self.get_object(id)
        student.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)