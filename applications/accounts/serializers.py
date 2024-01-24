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



class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = (
            'id', 'profile_photo',
            'first_name', 'first_name_ru', 
            'last_name', 'last_name_ru',
            'middle_name', 'middle_name_ru',
            'gender_ru', 'gender_en', 'gender_de',
            'nationality_ru', 'nationality_en', 'nationality_de', 
            'birth_country_ru', 'birth_country_en', 'birth_country_de',
            'birth_region_ru', 'birth_region_en', 'birth_region_de',
            'date_of_birth', 'phone', 'whatsapp_phone_number',
            'german', 'english', 'russian',
        )


class ProfileAllSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = (
            'id', 'profile_photo',
            'first_name', 
            'last_name',
            'middle_name',
            'gender_en',
            'nationality_en',
            'phone',
            'german', 'english',
            
        )



class UniversitySerializer(serializers.ModelSerializer):

    class Meta:
        model = University
        fields = (
            'id', 
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


class PassportAndTermSerializer(serializers.ModelSerializer):

    class Meta:
        model = PassportAndTerm
        fields = (
            'id', 
            'number_id_passport', 'inn',
            'passport_number', 'passport_date_of_issue',
            'passport_end_time', 'pnr_code',
            'pdf_file', 'term_date_time',
        )


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = (
            'id', 
            'total_amount','total_amount_in_words',
            'initial_fee','initial_fee_in_words',
            'average_fee','average_fee_in_words',
            'final_fee','final_fee_in_words',
            'debt','debt_in_words',
            'payment_date','payment_accepted_by',
            'payment_accepted_date','payment_accepted',
        )


class DealSerializer(serializers.ModelSerializer):

    class Meta:
        model = Deal 
        fields = (
            'id', 
            'phone_number', 'participant',
            'flight_date','steuer_id',
            'name','stage',
            'program','contract_date',
            'inn','comment','hijab',
        )



class RatingSerializer(serializers.ModelSerializer):
    value_rating = serializers.CharField(source='get_star_display', read_only=True)
    value_rating_write = serializers.ChoiceField(source='value_rating', choices=Rating.STAR_CHOICES, write_only=True, help_text="Рейтинг от 1-5")


    class Meta:
        model = Rating
        
        fields = (
            'id', 
            'value_rating', 
            'rating_date', 
            'user', 
            'employer', 
            'value_rating_write',
            )
        


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = (
            'id', 
            'rating', 
            'text', 
            'creation_date', 
            'user', 
            'employer',
            )




class WorkExperienceSerializer(serializers.ModelSerializer):
    type_company = serializers.ChoiceField(choices=WorkExperience.TYPE_OF_COMPANY_CHOICES, help_text="Тип компании")
    start_date = serializers.DateField(help_text="Дата начала работы")
    end_date = serializers.DateField(help_text="Дата окончания работы")

    class Meta:
        model = WorkExperience
        fields = (
            'id', 
            'user',
            'type_company', 
            'company', 
            'position', 
            'start_date', 
            'end_date', 
            'responsibilities', 
            'country', 
        )


class WorkScheduleSerializer(serializers.ModelSerializer):
    
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
            'user',

            'monday', 
            'tuesday', 
            'wednesday', 
            'thursday', 
            'friday', 
            'saturday', 
            'sunday',
            'custom', 
            'custom_start_time', 
            'custom_end_time',
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