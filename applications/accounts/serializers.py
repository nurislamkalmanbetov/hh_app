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
    password2 = serializers.CharField(max_length=100,required=True)

    class Meta:
        model = User
        fields = ('email',  'password', 'password2', )
        extra_kwargs = {
            'password': {'write_only': True},
        }
    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Пароли не совпадают.")
        return data
    
    def generate_verification_code(self):
        return randint(1000, 9999)
    
    def send_verication_email(self, user):
        verification_code = self.generate_verification_code(self)
        user.verification_codes = verification_code
        user.save()

        send_mail(
            f'Подтверждение регистрации\n,Ваш код подтверждения: {verification_code}',
            None,
            'kalmanbetovnurislam19@gmail.com',
            [user.email],
            fail_silently=False,
        )

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password']
        )
        self.send_verication_email(self, user)
        return user

class VerifyEmailSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    verification_code = serializers.CharField(max_length=100,required=True)


@swagger_auto_schema(request_body=VerifyEmailSerializer)
class VerifyEmailAPIView(APIView):
    serializer_class = VerifyEmailSerializer
    queryset = User.objects.all()  

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.data['email']
            verification_code = serializer.data['verification_code']
            user = User.objects.filter(email=email).first()
            if user is None:
                return Response({"error": "Пользователь не найден"}, status=status.HTTP_404_NOT_FOUND)
            if user.verification_code != verification_code:
                return Response({"error": "Неверный код"}, status=status.HTTP_400_BAD_REQUEST)
            user.is_active = True
            user.save()
            return Response({"message": "Успешная активация"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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


class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.EmailField(source='user.email')
    university = serializers.CharField(source='university.name_ru')
    faculty = serializers.CharField(source='faculty.name_ru')

    class Meta:
        model = Profile
        fields = ('id', 'user', 'photo', 'first_name', 'last_name', 'telephone',
        'bday', 'gender','been_to_germany', 'nationality', 'birth_country','reg_apartment',
        'university','faculty','study_start','study_end',
        'german', 'english', 'turkish', 'russian', 'chinese', 
        'driver_license', 'driving_experience', 'cat_a', 'cat_b', 'cat_c', 'cat_d', 'cat_e', 'tractor', 'transmission', 
        'reading', 'singing', 'travelling', 'yoga', 'dancing', 'sport', 'drawing', 'computer_games', 'guitar', 'films', 'music', 'knitting', 'cooking', 'fishing', 'photographing', 
        )

    def create(self, validated_data):
        user_email = validated_data.pop('user')
        user = User.objects.get(email=user_email)

        university_name = validated_data.pop('university').get('name_ru')
        university = University.objects.get(name_ru=university_name)

        faculty_name = validated_data.pop('faculty').get('name_ru')
        faculty = Faculty.objects.get(name_ru=faculty_name)
        
        profile = Profile.objects.create(
            user=user,
            university=university,
            faculty=faculty,
            **validated_data
        )
        return profile

class ProfileListSerializer(serializers.ModelSerializer):
    user = serializers.EmailField(source='user.email', read_only=True)
    university = serializers.CharField(source='university.name_ru', read_only=True)
    faculty = serializers.CharField(source='faculty.name_ru', read_only=True)
    

    class Meta:
        model = Profile
        fields = ('id', 'user', 'photo', 'first_name', 'last_name', 'telephone',
        'bday', 'gender','been_to_germany', 'nationality', 'birth_country','reg_apartment',
        'university','faculty','study_start','study_end',
        'german', 'english', 'turkish', 'russian', 'chinese', 
        'driver_license', 'driving_experience', 'cat_a', 'cat_b', 'cat_c', 'cat_d', 'cat_e', 'tractor', 'transmission', 
        'reading', 'singing', 'travelling', 'yoga', 'dancing', 'sport', 'drawing', 'computer_games', 'guitar', 'films', 'music', 'knitting', 'cooking', 'fishing', 'photographing', 
        )

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'avatar', 'email', 'phone', 'whatsapp_phone', 'is_employer', 'is_staff','is_active', 'is_superuser',)


class UserListPutchSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'avatar')

class SupportRequestSerializer(serializers.ModelSerializer):
    user = serializers.EmailField(source='user.email')

    class Meta:
        model = SupportRequest
        fields = [
            'id', 
            'user', 
            'message', 
            'created_at',
        ]

    def create(self, validated_data):
        user_email = validated_data.pop('user').get('email')
        try:
            user = User.objects.get(email=user_email)
        except User.DoesNotExist:
            raise serializers.ValidationError({"user": "User with this email does not exist."})
        supportrequest = SupportRequest.objects.create(user=user, **validated_data)
        return supportrequest


class SupportResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupportResponse
        fields = ['id', 'support_request', 'message', 'created_at', 'sent']

class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

class PasswordResetConfirmSerializer(serializers.Serializer):
    token = serializers.CharField()
    password = serializers.CharField(write_only=True)

class ConnectionRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConnectionRequest
        fields = (
            "id",
            "full_name",
            "email",
            "phone",
            "request_date",
            "manager_notes",
            "call_date",
            "called",
            "consulted",
            "call_later",
        )