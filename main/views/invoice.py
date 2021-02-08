from main.models import StudentInvoice
from django.db import IntegrityError
from rest_framework.response import Response
from rest_framework import status 
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from main.serializers import StudentInvoiceSerializerClass
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from main import event
from main.models import Staff, StudentInvoice, Student, StudentPayments
from django.urls import reverse

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

def invoice_reg_view(request):
    
    loggedin_user = request.user
    loggedin_staff = Staff.objects.get(user=loggedin_user)

    if loggedin_user.is_staff or loggedin_staff.director_access or loggedin_staff.student_finance_access or loggedin_staff.department.lower() == "finance":

        if request.method == "GET":        
            event.create_event(request, request.user, "Accessed Invoice Generation Portal")
            students = Student.objects.all()
            return render(request, "main/invoice_register.html", {
                "students": students
            })

        if request.method == "POST":
            event.create_event(request, request.user, "Tried to create a new invoice")

            student = request.POST["student"]
            year = request.POST["year"]
            amount = request.POST["amount"]

            def calculate_balance(student_id, amount):
                
                try:
                    student = Student.objects.get(pk=student_id)
                except:
                    return None

                if StudentPayments.objects.filter(student=student).exists():

                    total_in_invoices = 0

                    for invoice in StudentPayments.objects.get(student=student).invoices.all():
                        total_in_invoices += invoice.amount

                    student_programme = student.programme_application
                    balance = student_programme.fee - total_in_invoices

                else:

                    student_programme = student.programme_application
                    balance = student_programme.fee - amount

                return balance

            def calculate_hold(student_id, amount):

                try:
                    student = Student.objects.get(pk=student_id)
                except:
                    return None

                if StudentPayments.objects.filter(student=student).exists():
                    total_in_invoices = 0

                    for invoice in StudentPayments.objects.get(student=student).invoices.all():
                        total_in_invoices+=invoice.amount
                    student_programme = student.programme_application

                    if total_in_invoices > student_programme.fee:
                        balance =  total_in_invoices - student_programme.fee
                    else:
                        balance = 0

                else:
                    student_programme = student.programme_application

                    if amount > student_programme.fee:
                        balance =  amount - student_programme.fee
                    else:
                        balance = 0

                return balance

            try:
                new_invoice = StudentInvoice(
                    student = Student.objects.get(pk=int(student)),
                    academic_year = year,
                    amount = int(amount),
                    balance = calculate_balance(int(student), int(amount)) if calculate_balance(int(student), int(amount)) != None else -10000000000.0,
                    finance_hold = calculate_hold(int(student), int(amount)) if calculate_hold(int(student), int(amount)) != None else -10000000000.0
                )

                new_invoice.save()
                event.create_event(request, request.user, f"Created a new invoice {new_invoice.id}")
            except IntegrityError:
                event.create_event(request, request.user, "Tried to generate new invoice")
                return HttpResponse("Unable to generate invoice") 

            student = Student.objects.get(pk=int(student))

            try:
                payment_record = StudentPayments.objects.get(student=student)
                payment_record.invoices.add(new_invoice)
                payment_record.save()
                total_amount = 0
                for invoice in payment_record.invoices.all():
                    total_amount += invoice.amount

                programme_fee = payment_record.student.programme_application.fee
                total_discounts_percent = 0

                for discount in payment_record.student.DiscountOrScholarship.all():
                    total_discounts_percent += discount.percent

                #Check this steps
                programme_fee_after_discount = programme_fee - (programme_fee / 100 * total_discounts_percent)
                percent_paid = total_amount / programme_fee_after_discount * 100
                payment_record.percent = percent_paid
                payment_record.save()

            except StudentPayments.DoesNotExist:
                new_payment_record = StudentPayments(
                    student = student,
                    percent = 0,
                    academic_year = year,
                )
                new_payment_record.save()
                new_payment_record.invoices.add(new_invoice)
                new_payment_record.save()
                total_amount = 0
                for invoice in new_payment_record.invoices.all():
                    total_amount += invoice.amount

                programme_fee = new_payment_record.student.programme_application.fee
                total_discounts_percent = 0

                for discount in new_payment_record.student.DiscountOrScholarship.all():
                    total_discounts_percent += discount.percent


                programme_fee_after_discount = programme_fee - ( programme_fee / 100 * total_discounts_percent )
                percent_paid = total_amount / programme_fee_after_discount * 100
                new_payment_record.percent = percent_paid
                new_payment_record.save()


            return HttpResponseRedirect(reverse("invoice", args=(new_invoice.id, )))
    else:
        event.create_event(request, request.user, "Tried to acces Invoice Generation Portal")
        return HttpResponseRedirect(reverse("noaccess"))

def invoice_view(request, id):
    loggedin_user = request.user
    loggedin_staff = Staff.objects.get(user=loggedin_user)

    if loggedin_user.is_staff or loggedin_staff.director_access or loggedin_staff.student_finance_access or loggedin_staff.department.lower() == "finance":

        event.create_event(request, request.user, f"Accessed invoice {id}")
        invoice = StudentInvoice.objects.get(pk=id)

        return render(request, "main/invoice.html", {
            "invoice": invoice
        })

    else:
        event.create_event(request, request.user, f"Tried to acces Invoice {id}")
        return HttpResponseRedirect(reverse("noaccess"))

def invoices_view(request):
    loggedin_user = request.user
    loggedin_staff = Staff.objects.get(user=loggedin_user)

    if loggedin_user.is_staff or loggedin_staff.director_access or loggedin_staff.student_finance_access or loggedin_staff.department.lower() == "finance":

        event.create_event(request, request.user, f"Accessed invoices")
        invoices = StudentInvoice.objects.all()

        return render(request, "main/invoices.html", {
            "invoices": invoices
        })

    else:
        event.create_event(request, request.user, f"Tried to acces Invoices")
        return HttpResponseRedirect(reverse("noaccess"))