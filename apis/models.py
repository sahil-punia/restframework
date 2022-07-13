from email.policy import default
from django.db import models
# from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
# Create your models here.
import uuid

from django.forms import UUIDField

from .managers import CustomUserManager

class User(AbstractBaseUser,PermissionsMixin):
    # id           =  UUIDField(primary_key=True, default =uuid.uuid4 ,editable=False)
    username     =  models.CharField(max_length=56)
    first_name   =  models.CharField(max_length=56, blank=True, null=True)
    last_name    =  models.CharField(max_length=56, blank=True, null=True)
    email        =  models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    is_active    =  models.BooleanField(default=True)
    is_created   =  models.DateTimeField(auto_now_add=True)
    is_udated    =  models.DateTimeField(auto_now_add=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()
    def __str__(self):
        return self.email