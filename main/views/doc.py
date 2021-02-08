from django.shortcuts import render

# Create your views here.

def doc(request):
    return render(request, "main/doc.html")