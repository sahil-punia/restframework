from django.shortcuts import render

# Create your views here.
from .models import User
from .serializer import RegisterSerializer,MyTokenObtainPairSerializer
from rest_framework.permissions import AllowAny
from rest_framework import generics
from rest_framework_simplejwt.views import TokenObtainPairView



class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class   = RegisterSerializer

class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class   = MyTokenObtainPairSerializer