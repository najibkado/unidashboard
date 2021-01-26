from main.models import StudentService
from django.db import IntegrityError
from rest_framework.response import Response
from rest_framework import status 
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from main.serializers import StudentServiceSerializerClass

class StudentServicesApiView(APIView):
    
    def get(self, request):
        services = StudentService.objects.all()
        serializer = StudentServiceSerializerClass(services, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = StudentServiceSerializerClass(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StudentServiceApiView(APIView):
    
    def get_object(self, id):
        try:
            return StudentService.objects.get(pk=id)
        except StudentService.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id):
        service = self.get_object(id)
        serializer = StudentServiceSerializerClass(service)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id):
        service = self.get_object(id)
        serializer = StudentServiceSerializerClass(service, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        service = self.get_object(id)
        service.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)