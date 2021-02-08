from main.models import Student, Staff, Programme, DiscountsAndScholarship
from django.db import IntegrityError
from rest_framework.response import Response
from rest_framework import status 
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from main.serializers import StudentSerializerClass
from django.shortcuts import render
from main import event
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse


class StudentsApiView(APIView):
    
    def get(self, request):
        students = Student.objects.all()
        serializer = StudentSerializerClass(students, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = StudentSerializerClass(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StudentApiView(APIView):
    
    def get_object(self, id):
        try:
            return Student.objects.get(pk=id)
        except Student.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id):
        student = self.get_object(id)
        serializer = StudentSerializerClass(student)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id):
        student = self.get_object(id)
        serializer = StudentSerializerClass(student, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        student = self.get_object(id)
        student.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

def student_reg_view(request):
    
    loggedin_user = request.user
    loggedin_staff = Staff.objects.get(user=loggedin_user)

    if loggedin_user.is_staff or loggedin_staff.student_admission_access or loggedin_staff.director_access or loggedin_staff.department.lower() == "admission":
        
        if request.method == "GET":

            discounts_and_scholarships = DiscountsAndScholarship.objects.all()
            programmes = Programme.objects.all()


            event.create_event(request, request.user, "Accessed Student Creation Page")
            return render(request, "main/student_register.html", {
                "discounts": discounts_and_scholarships,
                "programmes": programmes
            })

        if request.method == "POST":

            event.create_event(request, request.user, "Tried to create a new student")

            first_name = request.POST["first-name"]
            lasst_name = request.POST["last-name"]
            sex = request.POST["sex"]
            email = request.POST["email"]
            phone = request.POST["phone"]
            address = request.POST["address"]
            country = request.POST["country"]
            is_international = request.POST.get("is-international")
            programme = request.POST["programme"]
            has_offer = request.POST.get("has-offer")
            discounts = request.POST.getlist("discounts")

            try:
                new_student = Student(
                    first_name = first_name,
                    last_name = lasst_name,
                    sex = sex,
                    phone = phone,
                    email = email,
                    country = country,
                    address = address,
                    isInternationalStudent = True if is_international == "on" else False,
                    programme_application = Programme.objects.get(pk=int(programme)),
                    hasOffer = True if has_offer == "on" else False,
                )

                new_student.save()

                event.create_event(request, request.user, f"Created student {new_student.id}")

                if len(discounts) > 0:
                    for discount in discounts:
                        discount_object = DiscountsAndScholarship.objects.get(pk=int(discount))
                        new_student.DiscountOrScholarship.add(discount_object)
                        new_student.save()

            except IntegrityError:
                event.create_event(request, request.user, "Tried to create a new student")
                return HttpResponse("Failed to create a new user")

            return HttpResponseRedirect(reverse("student", args=(new_student.id, )))


    else:
        event.create_event(request, request.user, "Tried to access student creation page")
        return HttpResponseRedirect(reverse("noaccess"))



def student_view(request, id):
    
    loggedin_user = request.user
    loggedin_staff = Staff.objects.get(user=loggedin_user)

    if loggedin_user.is_staff or loggedin_staff.student_admission_access or loggedin_staff.director_access or loggedin_staff.department.lower() == "admission":
        
        event.create_event(request, request.user, f"Accessed student admission card{id}")

        try:
            student = Student.objects.get(pk=id)
        except:
            return HttpResponse("Student profile does not exist!")

        return render(request, "main/student.html", {
            "student":student
        })

    else:
        event.create_event(request, request.user, f"Tried to access student admision card{id}")
        return HttpResponseRedirect(reverse("noaccess"))



def students_view(request):
    loggedin_user = request.user
    loggedin_staff = Staff.objects.get(user=loggedin_user)

    if loggedin_user.is_staff or loggedin_staff.student_admission_access or loggedin_staff.director_access or loggedin_staff.department.lower() == "admission":
        
        event.create_event(request, request.user, f"Accessed student admission cards page")

        try:
            students = Student.objects.all()
        except:
            return HttpResponse("Student profile does not exist!")

        return render(request, "main/students.html", {
            "students":students
        })

    else:
        event.create_event(request, request.user, f"Tried to access student admission cards")
        return HttpResponseRedirect(reverse("noaccess"))


def students_nooffer_view(request):
    loggedin_user = request.user
    loggedin_staff = Staff.objects.get(user=loggedin_user)

    if loggedin_user.is_staff or loggedin_staff.student_admission_access or loggedin_staff.director_access or loggedin_staff.department.lower() == "admission":
        
        event.create_event(request, request.user, f"Accessed student without offer admission cards page")

        try:
            students = Student.objects.filter(hasOffer=False)
        except:
            return HttpResponse("Student profile does not exist!")

        return render(request, "main/students_nooffer.html", {
            "students":students
        })

    else:
        event.create_event(request, request.user, f"Tried to access student without offer admission cards")
        return HttpResponseRedirect(reverse("noaccess"))
