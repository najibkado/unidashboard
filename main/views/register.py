from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from main.models import Staff
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.models import User
from django.db import IntegrityError
from main import event


@login_required
def register_view(request):
    if request.method == "GET":

        event.create_event(request, request.user, "Opened Staff Creation Page")

        user = request.user

        try:
            staff = Staff.objects.get(user=user)
        except Staff.DoesNotExist:
            return HttpResponseRedirect(reverse("noaccess"))

        if user.is_staff or staff.department.lower() == "it" or staff.it_department_access:
            return render(request, "main/register.html")
        return HttpResponseRedirect(reverse("noaccess"))

    if request.method == "POST":
        
        username = request.POST["username"]
        first_name = request.POST["first-name"]
        last_name = request.POST["last-name"]
        password = request.POST["password"]
        email = request.POST["email"]
        degree = request.POST["degree"]
        phone = request.POST["phone"]
        department = request.POST["department"]
        specialization = request.POST["specialization"]
        sex = request.POST["sex"]
        job = request.POST["job"]
        it_department_access = request.POST.get("it-access")
        student_office_department_access = request.POST.get("student-office-access")
        student_visa_access = request.POST.get("visa-access")
        student_finance_access = request.POST.get("finance-access")
        student_admission_access = request.POST.get("admission-access")
        director_access = request.POST.get("director-access")
        
        if User.objects.filter(username = username).exists():
            return HttpResponse("Username taken")

        if first_name == "" or last_name == "" or password == "" or email == "" or phone == "" or department == "" or specialization == "" or sex == "" or job == "":
            return HttpResponse("Fields cant be empty!")

        try:
            user = User.objects.create_user(
                username = username,
                email = email,
                password = password,
                first_name = first_name,
                last_name = last_name
            )

            user.save()

            event.create_event(request, request.user, f"Registered a new user with id {user.id}")

        except IntegrityError:
            event.create_event(request, request.user, "Tried to create a user")
            return HttpResponse("Error creating staff, try again later")

        try:
            staff = Staff(
                user = user,
                sex = sex,
                phone = phone,
                degree = degree,
                specialization = specialization,
                department = department,
                job = job,
                it_department_access = True if it_department_access == "on" else False,
                student_office_department_access = True if student_office_department_access == "on" else False,
                student_visa_access = True if student_visa_access == "on" else False,
                student_finance_access = True if student_finance_access == "on" else False,
                student_admission_access = True if student_admission_access == "on" else False,
                director_access = True if director_access == "on" else False
            )
            staff.save()

            event.create_event(request, request.user, f"Registered a new staff with id {staff.id}")
        except IntegrityError:
            event.create_event(request, request.user, "Tried to create a staff")
            return HttpResponse("User created, unable to create staff, pls use username to create a new staff")



        return HttpResponseRedirect(reverse("staff", args=(staff.id, )))





