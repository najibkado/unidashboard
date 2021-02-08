from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from main.models import Staff, EnrolledStudent, StudentInvoice, Student
from main import event
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.urls import reverse

@login_required
def dashboard_view(request):

    loggedin_user = request.user
    loggedin_staff = Staff.objects.get(user=loggedin_user)

    if request.user.is_staff or loggedin_staff.department.lower() == "director" or loggedin_staff.director_access:

        event.create_event(request, request.user, "Accessed Director Dashboard")

        invoices = StudentInvoice.objects.all()

        total_payment_recieved = 0
        total_payment_balance = 0
        num_of_intl_students = 0
        num_of_local_students = 0
        num_of_applications= len(Student.objects.filter(hasOffer=False))
        num_of_all_students = len(Student.objects.filter(hasOffer=True))

        for invoice in invoices:
            total_payment_recieved += invoice.amount
            total_payment_balance += invoice.balance

        event_num = len(event.get_events(request))
        enrolled_students = EnrolledStudent.objects.all()
        enrolled_num = len(enrolled_students)

        for student in enrolled_students:
            if student.student.isInternationalStudent:
                num_of_intl_students+=1
            else:
                num_of_local_students+=1

        events = event.get_events(request)
        

        return render(request, "main/dashboard.html", {
            "num_of_events" : event_num,
            "num_of_enrolled": enrolled_num,
            "total_payment_recieved": total_payment_recieved,
            "total_payment_balance": total_payment_balance,
            "num_of_intl_students": num_of_intl_students,
            "num_of_local_students": num_of_local_students,
            "num_of_applications": num_of_applications,
            "num_of_all_students": num_of_all_students,
            "events": reversed(events)
            })

    else:
        event.create_event(request, request.user, "Tried to access director dashboard")
        return HttpResponseRedirect(reverse("noaccess"))