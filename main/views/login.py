from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

def login_view(request):

    if request.method == "GET":
        return render(request, "main/login.html")

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        print(username, password)

        user = authenticate(request, username=username, password=password)

        if user is not None:

            login(request, user)

            return HttpResponseRedirect(reverse("index"))

        return HttpResponse("User not registered")