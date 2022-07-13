
from rest_framework import serializers
from .models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator
from django.core.exceptions import ValidationError



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