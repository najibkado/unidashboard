from main.models import Module
from django.db import IntegrityError
from rest_framework.response import Response
from rest_framework import status 
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from main.serializers import ModuleSerializerClass

class ModulesApiView(APIView):

    def get(self, request):
        modules = Module.objects.all()
        serializer = ModuleSerializerClass(modules, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ModuleSerializerClass(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ModuleApiView(APIView):

    def get_object(self, id):
        try:
            return Module.objects.get(pk=id)
        except Module.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id):
        module = self.get_object(id)
        serializer = ModuleSerializerClass(module)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id):
        module = self.get_object(id)
        serializer = ModuleSerializerClass(module, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        module = self.get_object(id)
        module.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
