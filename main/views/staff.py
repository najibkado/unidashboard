from main.models import Staff
from django.db import IntegrityError
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status 
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from main.serializers import StaffSerializerClass

class StaffsApiView(APIView):

    def get(self,  request):
        staffs = Staff.objects.all()
        serializer = StaffSerializerClass(staffs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = StaffSerializerClass(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StaffApiView(APIView):

    def get_object(self, id):
        try:
            return Staff.objects.get(pk=id)
        except Staff.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    def get(self, request, id):
        staff = self.get_object(id)
        serializer = StaffSerializerClass(staff)
        return Response(serializer.data)

    def put(self, request, id):
        staff = self.get_object(id)
        serializer = StaffSerializerClass(staff, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        staff = self.get_object(id)
        staff.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

        
