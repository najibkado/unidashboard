from main.models import StudentAcademics
from django.db import IntegrityError
from rest_framework.response import Response
from rest_framework import status 
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from main.serializers import StudentAcademicsSerializerClass

class StudentsAcademicsApiView(APIView):
    
    def get(self, request):
        academics = StudentAcademics.objects.all()
        serializer = StudentAcademicsSerializerClass(academics, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = StudentAcademicsSerializerClass(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StudentAcademicsApiView(APIView):
    
    def get_object(self, id):
        try:
            return StudentAcademics.objects.get(pk=id)
        except StudentAcademics.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id):
        academics = self.get_object(id)
        serializer = StudentAcademicsSerializerClass(academics)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id):
        academics = self.get_object(id)
        serializer = StudentAcademicsSerializerClass(academics, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        academics = self.get_object(id)
        academics.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)