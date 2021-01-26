# from django.shortcuts import render
# from django.contrib.auth import authenticate, login, logout
# from django.views.decorators.csrf import csrf_exempt
# from django.urls import reverse
# from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
# from .models import Entry
# from rest_framework.parsers import JSONParser
# from .serializers import EntrySerializer
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from rest_framework import status 
# from rest_framework.views import APIView
# from rest_framework.authentication import SessionAuthentication, TokenAuthentication
# from rest_framework.permissions import IsAuthenticated

# # Create your views here.

# def index(request):
#     return render(request, "main/index.html")

# def login_view(request):

#     if request.method == "POST":

#         username = request.POST['username']
#         password = request.POST['password']
#         print(username, password)

#         user = authenticate(request, username=username, password=password)

#         # Check if authentication successful
#         if user is not None:
#             login(request, user)
#             return HttpResponseRedirect(reverse("index"))
#         else:
#             return HttpResponseRedirect(reverse("index"))

# def logout_view(request):
#     logout(request)
#     return render(request, "main/index.html")

# class EntriesApiView(APIView):
    
#     authentication_classes = [SessionAuthentication, TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         entries = Entry.objects.all()
#         serializer = EntrySerializer(entries, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = EntrySerializer(data=request.data)

#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class EntryApiView(APIView):

#     authentication_classes = [SessionAuthentication, TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     def get_object(self, id):
        
#         try:
#             return Entry.objects.get(pk=id)
#         except Entry.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
    
#     def get(self, request, id):
#         entryObj = self.get_object(id)
#         serializer = EntrySerializer(entryObj)
#         return Response(serializer.data)

#     def put(self, request, id):
#         entryObj = self.get_object(id)
#         serializer = EntrySerializer(entryObj ,data=request.data)

#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, id):
#         entryObj = self.get_object(id)
#         entryObj.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)