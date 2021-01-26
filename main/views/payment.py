from main.models import StudentPayments
from django.db import IntegrityError
from rest_framework.response import Response
from rest_framework import status 
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from main.serializers import StudentPaymentsSerializerClass

class PaymentsApiView(APIView):
    
    def get(self, request):
        payments = StudentPayments.objects.all()
        serializer = StudentPaymentsSerializerClass(payments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = StudentPaymentsSerializerClass(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PaymentApiView(APIView):
    
    def get_object(self, id):
        try:
            return StudentPayments.objects.get(pk=id)
        except StudentPayments.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id):
        payment = self.get_object(id)
        serializer = StudentPaymentsSerializerClass(payment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id):
        payment = self.get_object(id)
        serializer = StudentPaymentsSerializerClass(payment, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        payment = self.get_object(id)
        payment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)