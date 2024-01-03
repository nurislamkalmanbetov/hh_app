from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.views import APIView
from drf_yasg2.utils import swagger_auto_schema
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.core.mail import send_mail
from random import randint
from .models import *
from .serializers import *

User = get_user_model()

class RegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email',)

class VerifyEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    verification_code = serializers.CharField(required=True, style={'input_type': 'verification_code'})


class SetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, style={'input_type': 'password'})
    password_confirm = serializers.CharField(required=True, style={'input_type': 'password'})
    

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'is_employer', 'is_student',)
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create(

            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, allow_blank=False, allow_null=False)
    password = serializers.CharField(required=True, allow_blank=False, allow_null=False)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        return data

