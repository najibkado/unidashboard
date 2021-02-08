from main.models import Programme, Staff, Module
from django.db import IntegrityError
from rest_framework.response import Response
from rest_framework import status 
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from main.serializers import ProgrammeSerializerClass
from main import event
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse


class ProgrammesApiView(APIView):
    
    def get(self, request):
        programmes = Programme.objects.all()
        serializer = ProgrammeSerializerClass(programmes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ProgrammeSerializerClass(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProgrammeApiView(APIView):
    
    def get_object(self, id):
        try:
            return Programme.objects.get(pk=id)
        except Programme.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id):
        programme = self.get_object(id)
        serializer = ProgrammeSerializerClass(programme)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id):
        programme = self.get_object(id)
        serializer = ProgrammeSerializerClass(programme, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        programme = self.get_object(id)
        programme.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

def programmes_view(request):

    loggedin_user = request.user
    loggedin_staff = Staff.objects.get(user=loggedin_user)

    if request.user.is_staff or loggedin_staff.department.lower() == "it" or loggedin_staff.it_department_access:

        event.create_event(request, request.user, f"Accessed Programmes Page")

        programmes = Programme.objects.all()

        return render(request, "main/programmes.html", {
            "programmes": programmes,
        })

    else:
        event.create_event(request, request.user, f"Tried to access programmes page")
        return HttpResponseRedirect(reverse("noaccess"))

def programme_reg_view(request):
    
    loggedin_user = request.user
    loggedin_staff = Staff.objects.get(user=loggedin_user)

    if request.user.is_staff or loggedin_staff.department.lower() == "it" or loggedin_staff.it_department_access:

        event.create_event(request, request.user, "Accessed Programme Registration Page")

        modules = Module.objects.all()
        
        if request.method == "GET":
            return render(request, "main/programme_register.html", {
                "modules": modules
            })

        if request.method == "POST":
            
            code = request.POST["programme-code"]
            title = request.POST["programme-title"]
            desc = request.POST["programme-desc"]
            modules = request.POST.getlist("modules")
            fee = request.POST["programme-fee"]

            try:
                programme = Programme(
                    code = code,
                    title = title,
                    description = desc,
                    fee = int(fee)
                )
                programme.save()

                for module in modules:
                    modul = Module.objects.get(pk=int(module))
                    programme.modules.add(modul)
                    programme.save()

                event.create_event(request, request.user, "Created a new programme")

            except IntegrityError:

                event.create_event(request, request.user, "Tried to create a new Programme")
                return HttpResponse("Failed to create a new programme")
                

            return HttpResponseRedirect(reverse("programme", args=(programme.id, )))

    else:

        event.create_event(request, request.user, "Tried to access programme registration page")
        return HttpResponseRedirect(reverse("noaccess"))

def programme_view(request, id):

    loggedin_user = request.user
    loggedin_staff = Staff.objects.get(user=loggedin_user)

    if request.user.is_staff or loggedin_staff.department.lower() == "it" or loggedin_staff.it_department_access:

        event.create_event(request, request.user, f"Accessed Programme {id}")

        programme = Programme.objects.get(pk=id)

        return render(request, "main/programme.html", {
            "programme": programme,
            "programme_module_num": programme.modules.count()
        })

    else:
        event.create_event(request, request.user, f"Tried to access programme {id}")
        return HttpResponseRedirect(reverse("noaccess"))