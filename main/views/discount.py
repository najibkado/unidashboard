from main.models import DiscountsAndScholarship
from django.db import IntegrityError
from rest_framework.response import Response
from rest_framework import status 
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from main.serializers import DiscountsAndScholarshipSerializerClass
from django.shortcuts import render
from main import event
from main.models import Staff
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

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

def discount_reg_view(request):

    loggedin_user = request.user
    loggedin_staff = Staff.objects.get(user=loggedin_user)

    if loggedin_user.is_staff or loggedin_staff.student_admission_access or loggedin_staff.department.lower() == "admission":

        if request.method == "GET":

            event.create_event(request, request.user, "Accessed Discount and Scholarship Registration Page")
            return render(request, "main/discount_register.html")

        if request.method == "POST":

            event.create_event(request, request.user, "Tried to register Discount or Scholarship")

            discount_code = request.POST["discount-code"]
            discount_title = request.POST["discount-title"]
            discount_desc = request.POST["discount-desc"]
            discount_percent = request.POST["discount-percent"]

            try:
                new_discount = DiscountsAndScholarship(
                    code = discount_code,
                    title = discount_title,
                    description = discount_desc,
                    percent = discount_percent
                )
                new_discount.save()
                event.create_event(request, request.user, "Created a new discount or scholarship")
                return HttpResponseRedirect(reverse("discount", args=(new_discount.id, )))
            except IntegrityError:
                event.create_event(request, request.user, "Failed to register Discount or Scholarship")
                return HttpResponseRedirect("discount-register")

    else:
        event.create_event(request, request.user, "Tried to Access Discount and Scholarship Registration Page")
        return HttpResponseRedirect(reverse("noaccess"))

def discounts_view(request):
    loggedin_user = request.user
    loggedin_staff = Staff.objects.get(user=loggedin_user)

    if loggedin_user.is_staff or loggedin_staff.student_admission_access or loggedin_staff.department.lower() == "admission":

        event.create_event(request, request.user, f"Accessed Discounts and Scholarships")

        try:
            discounts = DiscountsAndScholarship.objects.all()
        except:
            return HttpResponse("Does not exist")

        return render(request, "main/discounts.html", {
            "discounts": discounts
        })

    else:
        event.create_event(request, request.user, f"Tried to Access Discounts and Scholarships Page")
        return HttpResponseRedirect(reverse("noaccess"))

def discount_view(request, id):
    
    loggedin_user = request.user
    loggedin_staff = Staff.objects.get(user=loggedin_user)

    if loggedin_user.is_staff or loggedin_staff.student_admission_access or loggedin_staff.department.lower() == "admission":

        event.create_event(request, request.user, f"Accessed Discount and Scholarship {id}")

        try:
            discount = DiscountsAndScholarship.objects.get(pk=id)
        except:
            return HttpResponse("Does not exist")

        return render(request, "main/discount.html", {
            "discount": discount
        })

    else:
        event.create_event(request, request.user, f"Tried to Access Discount and Scholarship Page {id}")
        return HttpResponseRedirect(reverse("noaccess"))
