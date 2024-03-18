from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.views import APIView

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.core.mail import send_mail
from random import randint
from .models import *
from .serializers import *
from applications.core.models import Favorite
User = get_user_model()

class RegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email','role',)

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
        fields = ('id', 'email', 'password', 'role',)
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data.get('role', 'Пользователь')
            )
        return user
    

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, allow_blank=False, allow_null=False)
    password = serializers.CharField(required=True, allow_blank=False, allow_null=False)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        return data
    



class UniversitySerializer(serializers.ModelSerializer):

    class Meta:
        model = University
        fields = (
            'id',
            'user',
            'name_ru', 'name_en', 'name_de',
            'degree_type_ru', 'degree_type_en', 'degree_type_de',
            'faculty_ru', 'faculty_en', 'faculty_de',
            'address_ru', 'address_en', 'address_de',
            'phone_number_university_ru',
            'email_university','website_university',
            'start_date','end_date','total_years',
            'kurs_year',
            'start_holiday', 'end_holiday',
        )


class ProfileSerializer(serializers.ModelSerializer):
    universities = UniversitySerializer(many=True, read_only=True)
    favorite_employer = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = (
            'id', 
            'profile_photo',
            'first_name', 
            'first_name_ru', 
            'last_name', 
            'last_name_ru',
            'middle_name', 
            'middle_name_ru',
            'gender_ru', 
            'gender_en', 
            'gender_de',
            'nationality_ru', 
            'nationality_en', 
            'nationality_de', 
            'birth_country_ru', 
            'birth_country_en', 
            'birth_country_de',
            'birth_region_ru', 
            'birth_region_en', 
            'birth_region_de',
            'date_of_birth', 
            'phone', 
            'whatsapp_phone_number',
            'german', 
            'english', 
            'russian',
            'universities',
            'favorite_employer'
        )

    def get_favorite_employer(self, obj):
        request = self.context.get('request')
     
        favorite = Favorite.objects.filter(employer__user=request.user, user=obj)
        if favorite.exists():
            return True
        return False

        

class ProfileAllSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Profile
        fields = (
            'id', 'profile_photo',
            'first_name', 
            'last_name',
            'gender_en',
            'nationality_en',
            'date_of_birth',
            'phone',
            'german', 
            'english',
            
        )

