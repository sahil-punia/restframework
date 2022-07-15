
from dataclasses import fields
import email
from email.mime import image
from rest_framework import serializers
from .models import User,Profile
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator
from django.core.exceptions import ValidationError

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required = True, validators = [UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(write_only = True,required =True, validators = [validate_password])
    confirm_password = serializers.CharField(required = True , write_only = True)

    class Meta:
        model = User
        fields = ('username', 'email' , 'password' ,'confirm_password', 'first_name' , "last_name")
        
    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            return serializers.ValidationError({"password":"Password field didn't match"})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username   = validated_data['username'],
            email      = validated_data['email'],
            first_name = validated_data['first_name'],
            last_name  = validated_data['last_name']
        )

        user.set_password(validated_data['password'])
        user.save()
        return user





class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # Add custom claims
        token['username'] = user.username
        return token


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model  =Profile
        fields = ['id', 'first_name', 'last_name', 'email' ,'city' , 'address', 'zipcode', 'gender']

        # first_name = serializers.CharField(max_length = 100)
    # last_name  = serializers.CharField(max_length = 100)
    # email      = serializers.EmailField(max_length = 100)
    # city       = serializers.CharField(max_length = 100)
    # address    = serializers.CharField(max_length = 100)
    # zipcode    = serializers.IntegerField(max_length = 100)
    # gender     = serializers.CharField(max_length = 100)
    # date       = serializers.DateTimeField()

    # # image      = serializers.ImageField()
    # # file       = serializers.FileField()

    # def create(self, validated_data):
    #     return Profile.objects.create(validated_data)

    # def update(self, instance, validated_data):
    #     instance.first_name = validated_data.get('first_name',instance.first_name)
    #     instance.last_name  = validated_data.get('last_name',instance.last_name)
    #     instance.email      = validated_data.get('email',instance.email)
    #     instance.city       = validated_data.get('city',instance.city)
    #     instance.address    = validated_data.get('address',instance.address)
    #     instance.zipcode    = validated_data.get('zipcode',instance.zipcode)
    #     instance.gender     = validated_data.get('gender',instance.gender)
    #     instance.date       = validated_data.get('date',instance.date)
    #     instance.save()
    #     return instance
    