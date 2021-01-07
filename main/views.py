from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from .models import Student, Staff
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.

def index(request):
    return HttpResponse("Index page")

@csrf_exempt
def student(request):

    #Returns all students
    if request.method == "GET":
        try:
            students = Student.objects.all()
        except Student.DoesNotExist:
            students = None

        if students is not None:
            return JsonResponse({
                "students" : [student.serialize() for student in students]
            })
        else:
            return JsonResponse({
                "students" : "No students record found"
            })

    #Create a new student
    elif request.method == "POST":

        data = json.loads(request.body)

        first_name = data.get("first-name")
        last_name = data.get("last-name")
        sex = data.get("sex")
        phone = data.get("phone")
        email = data.get("email")
        country = data.get("country")
        address = data.get("address")
        isInternational = data.get("is-international")
        programme_applied = data.get("programmed-applied")
        hasOffer = data.get("has-offer")
        discountOrScholarship = data.get("discount-or-scholarship")

        context = {
            "first-name": first_name,
            "last-name": last_name,
            "sex": sex,
            "phone": phone,
            "email": email,
            "country": country,
            "address": address,
            "is-international": isInternational,
            "programmed-applied": programme_applied,
            "has-offer": hasOffer,
            "discount-or-scholarship": discountOrScholarship
        }

        return JsonResponse({
            "students" : [context]
        })

        # if first_name is not "" and last_name is not "" and sex is not "" and phone is not "" and email is not "" and country is not "" and address is not "" and isInternational is not "" and programme_applied is not "":
            
        #     if "@" in email and "." in email :

        #         try:

        #             student = Student(
        #                 first_name = first_name,
        #                 last_name = last_name,
        #                 sex = sex,
        #                 phone = phone,
        #                 email = email,
        #                 country = country,
        #                 address = address,
        #                 isInternationalStudent = isInternational,
        #                 programme_application = programme_applied,
        #                 hasOffer = hasOffer,
        #                 DiscountOrScholarship = discountOrScholarship
        #             )

        #             student.save()

        #             return JsonResponse({
        #                 "message" : "successfully added to record",
        #                 "student" : student.serialize()
        #             })

        #         except IntegrityError:
        #             return JsonResponse({
        #                 "message" : "could not register user at the moment. pls try again later"
        #             })

        #     else:

        #         return JsonResponse({
        #             "message" : "Invalid email, please provide a valid email"
        #         })



    elif request.method == "DELETE":

        try:
            students = Student.objects.all()
        except Student.DoesNotExist:
            students = None

        if students is not None:
            
            for student in students:
                
                student.delete()

            return JsonResponse({
                "message" : "successfully deleted",
                "students" : [student.serialize() for student in students]
            })

def staff(request):
    pass

def enroll(request):
    pass

def service(request):
    pass

def finance(request):
    pass