from main.models import EnrolledStudent, Staff, Student, Programme
from django.db import IntegrityError
from rest_framework.response import Response
from rest_framework import status 
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from main.serializers import EnrolledStudentSerializerClass
from main import event
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

class EnrolledStudentsApiView(APIView):
    
    def get(self, request):
        students = EnrolledStudent.objects.all()
        serializer = EnrolledStudentSerializerClass(students, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = EnrolledStudentSerializerClass(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EnrolledStudentApiView(APIView):
    
    def get_object(self, id):
        try:
            return EnrolledStudent.objects.get(pk=id)
        except EnrolledStudent.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id):
        student = self.get_object(id)
        serializer = EnrolledStudentSerializerClass(student)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id):
        student = self.get_object(id)
        serializer = EnrolledStudentSerializerClass(student, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        student = self.get_object(id)
        student.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@login_required
def enroll_register_view(request):
    
    loggedin_user = request.user
    loggedin_staff = Staff.objects.get(user=loggedin_user)

    if loggedin_user.is_staff or loggedin_staff.director_access or loggedin_staff.student_office_department_access or loggedin_staff.department.lower() == "student office":

        if request.method == "GET":
            event.create_event(request, request.user, "Accessed student enrollment portal")
            students = Student.objects.all()
            programmes = Programme.objects.all()
            return render(request, "main/enroll_register.html", {
                "students": students,
                "programmes": programmes
            })

    else:
        event.create_event(request, request.user, "Tried to access student enrollment portal")
        return HttpResponseRedirect(reverse("noaccess"))

@login_required
def enrolled_card_view(request, id):
    pass

@login_required
def enrolled_view(request):
    pass