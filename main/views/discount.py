from main.models import DiscountsAndScholarship
from django.db import IntegrityError
from rest_framework.response import Response
from rest_framework import status 
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from main.serializers import DiscountsAndScholarshipSerializerClass

class DiscountsAndScholarshipsApiView(APIView):
    
    def get(self, request):
        discounts = DiscountsAndScholarship.objects.all()
        serializer = DiscountsAndScholarshipSerializerClass(discounts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = DiscountsAndScholarshipSerializerClass(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DiscountsAndScholarshipApiView(APIView):
    
    def get_object(self, id):
        try:
            return DiscountsAndScholarship.objects.get(pk=id)
        except DiscountsAndScholarship.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id):
        discount = self.get_object(id)
        serializer = DiscountsAndScholarshipSerializerClass(discount)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id):
        discount = self.get_object(id)
        serializer = DiscountsAndScholarshipSerializerClass(discount, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        discount = self.get_object(id)
        discount.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)