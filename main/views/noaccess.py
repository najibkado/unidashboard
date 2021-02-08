from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def noaccess_view(request):
    return render(request, "main/noaccess.html")