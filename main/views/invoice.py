from main.models import StudentInvoice
from django.db import IntegrityError
from rest_framework.response import Response
from rest_framework import status 
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from main.serializers import StudentInvoiceSerializerClass

class InvoicesApiView(APIView):
    
    def get(self, request):
        invoices = StudentInvoice.objects.all()
        serializer = StudentInvoiceSerializerClass(invoices, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = StudentInvoiceSerializerClass(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class InvoiceApiView(APIView):
    
    def get_object(self, id):
        try:
            return StudentInvoice.objects.get(pk=id)
        except StudentInvoice.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id):
        invoice = self.get_object(id)
        serializer = StudentInvoiceSerializerClass(invoice)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id):
        invoice = self.get_object(id)
        serializer = StudentInvoiceSerializerClass(invoice, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        invoice = self.get_object(id)
        invoice.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)