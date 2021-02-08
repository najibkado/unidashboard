from main.models import Module
from django.db import IntegrityError
from rest_framework.response import Response
from rest_framework import status 
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from main.serializers import ModuleSerializerClass
from django.shortcuts import render
from main import event
from main.models import Staff
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

class ModulesApiView(APIView):

    def get(self, request):
        modules = Module.objects.all()
        serializer = ModuleSerializerClass(modules, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ModuleSerializerClass(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ModuleApiView(APIView):

    def get_object(self, id):
        try:
            return Module.objects.get(pk=id)
        except Module.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id):
        module = self.get_object(id)
        serializer = ModuleSerializerClass(module)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id):
        module = self.get_object(id)
        serializer = ModuleSerializerClass(module, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        module = self.get_object(id)
        module.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

def module_reg_view(request):

    loggedin_user = request.user
    loggedin_staff = Staff.objects.get(user=loggedin_user)

    if request.method == "GET":

        if loggedin_user.is_staff or loggedin_staff.department.lower() == "it" or loggedin_staff.it_department_access:       
            event.create_event(request, request.user, "Viewed Module Creation Page")

            return render(request, "main/module_register.html", {
                "tutors": Staff.objects.all()
            })

        event.create_event(request, request.user, "Tried to View Module Creation Page")
        return HttpResponseRedirect(reverse("noaccess"))

    if request.method == "POST":

        if loggedin_user.is_staff or loggedin_staff.department.lower() == "it" or loggedin_staff.it_department_access:       
            event.create_event(request, request.user, "Tried to create a new module")

            code = request.POST["module-code"]
            title = request.POST["module-title"]
            desc = request.POST["module-desc"]
            tutors = request.POST.getlist("tutors")


            try:
                module = Module(
                    code = code,
                    title = title,
                    description = desc
                )
                module.save()
                for tutor in tutors:
                    staff = Staff.objects.get(pk=int(tutor))
                    module.tutors.add(staff)
                    module.save()
                
                event.create_event(request, request.user, "Created a new module")
            except IntegrityError:
                event.create_event(request, request.user, "Failed to create a new module")
                return HttpResponse("Failed to create a new module")

            return HttpResponseRedirect(reverse("module", args=(module.id, )))
        else:

            event.create_event(request, request.user, "Tried to create a new module")
            return HttpResponseRedirect(reverse("noaccess"))


def module_view(request, id):

    loggedin_user = request.user
    loggedin_staff = Staff.objects.get(user=loggedin_user)

    if loggedin_user.is_staff or loggedin_staff.department.lower() == "it" or loggedin_staff.it_department_access:       
        event.create_event(request, request.user, f"Viewed module {id}")

        try:
            module = Module.objects.get(pk=id)
        except Module.DoesNotExist:
            pass
    
        return render(request, "main/module.html", {
            "module": module,
            "module_tutor_num": module.tutors.count()
        })

    else:

        event.create_event(request, request.user, f"Tried to view module {id}")
        return HttpResponseRedirect(reverse("noaccess"))


def modules_view(request):
    
    loggedin_user = request.user
    loggedin_staff = Staff.objects.get(user=loggedin_user)

    if loggedin_user.is_staff or loggedin_staff.department.lower() == "it" or loggedin_staff.it_department_access:       
        event.create_event(request, request.user, f"Viewed modules page")

        modules = Module.objects.all()
    
        return render(request, "main/modules.html", {
            "modules": modules,
        })

    else:

        event.create_event(request, request.user, f"Tried to view modules page")
        return HttpResponseRedirect(reverse("noaccess"))


