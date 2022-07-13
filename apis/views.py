from django.shortcuts import render

# Create your views here.
from .models import User
from .serializer import RegisterSerializer
from rest_framework.permissions import AllowAny
from rest_framework import generics




class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer