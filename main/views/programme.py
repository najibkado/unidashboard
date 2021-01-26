from main.models import Programme
from django.db import IntegrityError
from rest_framework.response import Response
from rest_framework import status 
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from main.serializers import ProgrammeSerializerClass

class ProgrammesApiView(APIView):
    
    def get(self, request):
        programmes = Programme.objects.all()
        serializer = ProgrammeSerializerClass(programmes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ProgrammeSerializerClass(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProgrammeApiView(APIView):
    
    def get_object(self, id):
        try:
            return Programme.objects.get(pk=id)
        except Programme.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id):
        programme = self.get_object(id)
        serializer = ProgrammeSerializerClass(programme)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id):
        programme = self.get_object(id)
        serializer = ProgrammeSerializerClass(programme, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        programme = self.get_object(id)
        programme.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)