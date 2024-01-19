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





class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = (
            'id',
            'user',

            'first_name', 'last_name',
            'user','profile_photo','gender','nationality',
            'date_of_birth','inn','phone',
            
            'language_1', 'language_level_1',
            'language_2', 'language_level_2',
            'language_3', 'language_level_3',
            'language_4', 'language_level_4',

            'whatsapp_phone_number',
        )






        
class ProfileListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = (
            'id',
            'user',

            'first_name', 'last_name',
            'user','profile_photo','gender','nationality',
            'date_of_birth','inn','phone',
            
            'language_1', 'language_level_1',
            'language_2', 'language_level_2',
            'language_3', 'language_level_3',
            'language_4', 'language_level_4',

            'whatsapp_phone_number',
        )



class UserListSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=User.ROLE_CHOICES)


    class Meta:
        model = User
        fields = (
            'id', 'email',
            'role', 'is_staff', 'is_superuser',
            'is_active', 'is_verified_email',
            'verification_code_created_at', 'registered_at',
        )




class RatingSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(write_only=True)
    employer_email = serializers.EmailField(write_only=True)
    user_email_read = serializers.EmailField(source='user.email', read_only=True)
    employer_email_read = serializers.EmailField(source='employer.email', read_only=True)
    # new 
    value_rating = serializers.CharField(source='get_star_display', read_only=True)
    value_rating_write = serializers.ChoiceField(source='value_rating', choices=Rating.STAR_CHOICES, write_only=True, help_text="Рейтинг от 1-5")

    class Meta:
        model = Rating
        # fields = (
            # 'id', 'user_email_read', 'employer_email_read', 'value_rating', 
            # 'rating_date', 'user_email', 'employer_email'
            # )
        
        # new 
        fields = (
            'id', 'user_email_read', 'employer_email_read', 'value_rating', 
            'rating_date', 'user_email', 'employer_email', 'value_rating_write'
            )
    
    
    def create(self, validated_data):
        user_email = validated_data.pop('user_email', None)
        employer_email = validated_data.pop('employer_email', None)

        if not employer_email or not user_email:
            raise ValidationError({'detail': 'Необходимо предоставить адреса электронной почты пользователя и работодателя.'})

        employer = User.objects.filter(email=employer_email).first()
        if not employer or employer.role != 'Работодатель':
            raise ValidationError({'employer_email': 'Только работодатели могут создавать рейтинги или работодатель не найден.'})

        user = User.objects.filter(email=user_email).first()
        if not user:
            raise ValidationError({'user_email': f"Пользователь с адресом электронной почты {user_email} не найден."})

        if Rating.objects.filter(user=user, employer=employer).exists():
            raise ValidationError('Рейтинг от этого работодателя для данного пользователя уже существует.')

        rating = Rating.objects.create(user=user, employer=employer, **validated_data)
        return rating



class ReviewSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(write_only=True)
    employer_email = serializers.EmailField(write_only=True)
    user_email_read = serializers.EmailField(source='user.email', read_only=True)
    employer_email_read = serializers.EmailField(source='employer.email', read_only=True)
    rating__rating = serializers.IntegerField(source='rating.value_rating', read_only=True)

    class Meta:
        model = Review
        fields = ('id', 'user_email_read', 'employer_email_read','rating__rating', 'text', 'creation_date', 'user_email', 'employer_email')

    def create(self, validated_data):
        user_email = validated_data.pop('user_email', None)
        employer_email = validated_data.pop('employer_email', None)

        if not employer_email or not user_email:
            raise ValidationError({'detail': 'Необходимо предоставить адреса электронной почты пользователя и работодателя.'})

        employer = User.objects.filter(email=employer_email).first()
        if not employer or employer.role != 'Работодатель':
            raise ValidationError({'employer_email': 'Только работодатели могут создавать отзывы или работодатель не найден.'})

        user = User.objects.filter(email=user_email).first()
        if not user:
            raise ValidationError({'user_email': f"Пользователь с адресом электронной почты {user_email} не найден."})

        review = Review.objects.create(user=user, employer=employer, **validated_data)
        return review
    



class WorkExperienceSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(write_only=True)
    user_email_read = serializers.EmailField(source='user.email', read_only=True)
    type_company = serializers.ChoiceField(choices=WorkExperience.TYPE_OF_COMPANY_CHOICES, help_text="Тип компании")
    start_date = serializers.DateField(help_text="Дата начала работы")
    end_date = serializers.DateField(help_text="Дата окончания работы")

    class Meta:
        model = WorkExperience
        fields = (
            'id', 
            'user_email_read', 
            'type_company', 'company', 'position', 'start_date', 'end_date', 'responsibilities', 'country', 
            'user_email'
        )

    def create(self, validated_data):
        user_email = validated_data.pop('user_email', None)

        if not user_email:
            raise ValidationError({'detail': 'Необходимо предоставить адрес электронной почты пользователя.'})

        user = User.objects.filter(email=user_email).first()
        if not user:
            raise ValidationError({'user_email': f"Пользователь с адресом электронной почты {user_email} не найден."})

        work_experience = WorkExperience.objects.create(user=user, **validated_data)
        return work_experience
    


class WorkScheduleSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(write_only=True)
    user_email_read = serializers.EmailField(source='user.email', read_only=True)
    
    monday = serializers.ChoiceField(choices=WorkSchedule.TIME_CHOICES)
    tuesday = serializers.ChoiceField(choices=WorkSchedule.TIME_CHOICES)
    wednesday = serializers.ChoiceField(choices=WorkSchedule.TIME_CHOICES)
    thursday = serializers.ChoiceField(choices=WorkSchedule.TIME_CHOICES)
    friday = serializers.ChoiceField(choices=WorkSchedule.TIME_CHOICES)
    saturday = serializers.ChoiceField(choices=WorkSchedule.TIME_CHOICES)
    sunday = serializers.ChoiceField(choices=WorkSchedule.TIME_CHOICES)
    custom = serializers.ChoiceField(choices=WorkSchedule.TIME_CHOICES)

    class Meta:
        model = WorkSchedule
        fields = (
            'id',
            'user_email', 'user_email_read',
            'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday',
            'custom', 'custom_start_time', 'custom_end_time',
        )

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['monday'] = self._get_readable_choice(instance.monday)
        rep['tuesday'] = self._get_readable_choice(instance.tuesday)
        rep['wednesday'] = self._get_readable_choice(instance.wednesday)
        rep['thursday'] = self._get_readable_choice(instance.thursday)
        rep['friday'] = self._get_readable_choice(instance.friday)
        rep['saturday'] = self._get_readable_choice(instance.saturday)
        rep['sunday'] = self._get_readable_choice(instance.sunday)
        rep['custom'] = self._get_readable_choice(instance.custom)
        return rep

    def _get_readable_choice(self, field_value):
        return dict(WorkSchedule.TIME_CHOICES).get(field_value)
