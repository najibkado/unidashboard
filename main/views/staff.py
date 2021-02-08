from main.models import Staff
from django.db import IntegrityError
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status 
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from main.serializers import StaffSerializerClass
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from main import event
from django.contrib.auth.decorators import login_required

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

@login_required
def staffs_view(request):

    loggedin_user = request.user
    loggedin_staff = Staff.objects.get(user=loggedin_user)

    if loggedin_user.is_staff or loggedin_staff.department.lower() == "it" or loggedin_staff.it_department_access:
    
        if request.method == "GET":

            event.create_event(request, request.user, "Accessed Staffs Page")

            try:
                staffs = Staff.objects.all()
            except Staff.DoesNotExist:
                staffs = []

            return render(request, "main/staffs.html", {
                "staffs": staffs
            })

    return HttpResponseRedirect(reverse("noaccess"))

@login_required
def staff_view(request, id):

    loggedin_user = request.user
    loggedin_staff = Staff.objects.get(user=loggedin_user)

    try:
        staff = Staff.objects.get(pk=id)
    except Staff.DoesNotExist:
        pass

    if loggedin_user.is_staff or loggedin_staff.department.lower() == "it" or loggedin_staff.it_department_access:

        event.create_event(request, request.user, f"Viewed staff profile {id}")

        all_events = event.get_my_events(request, staff.user)
        gen_event = len(event.get_events(request))
        all_events_num = len(all_events)

        if all_events_num > 5:
            events = all_events[all_events_num-5:all_events_num]
        else:
            events = all_events

        return render(request, "main/staff.html", {
            "staff": staff,
            "events": reversed(events),
            "event_num": all_events_num,
            "all_events": reversed(all_events),
            "gen_event": gen_event
        })
    return HttpResponseRedirect(reverse("noaccess"))
    
        
