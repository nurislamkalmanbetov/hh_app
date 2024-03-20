from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.template.loader import render_to_string

from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import (exceptions, filters, generics, mixins, status, viewsets)
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated


from random import randint
from django.shortcuts import get_object_or_404
from django.db.models import F
from .permissions import IsEmployeePermisson
from applications.core.permissions import IsEmployerPermisson
from .serializers import *
from applications.core.models import Vacancy, Invitation
from .tasks import send_custom_email_task

User = get_user_model()





class RegistrationAPIView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer  # Используйте свой сериализатор

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        user = User.objects.filter(email=email).first()

        if user is not None and not user.is_verified_email:
            verification_code = randint(10000, 99999)
            user.verification_code = verification_code
            user.verification_code_created_at = timezone.now()
            user.save()

            context = {
                'verification_code': verification_code,
            }

            send_custom_email_task.delay(
                user.email,
                'Подтверждение регистрации',
                'email_template.html',
                context
            )

            return Response({
                "user": user.email,
                "role": user.role,
                "status": status.HTTP_200_OK
            })

        serializer = self.get_serializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            user = User.objects.filter(email=serializer.validated_data['email']).first()

            user = User.objects.create(
                email=serializer.validated_data['email'],
                role=serializer.validated_data['role'],
            )

            verification_code = randint(10000, 99999)
            user.verification_code = verification_code
            user.verification_code_created_at = timezone.now()
            user.save()

            context = {
                'verification_code': verification_code,
            }

            send_custom_email_task.delay(
                user.email,
                'Подтверждение регистрации',
                'email_template.html',
                context
            )

            return Response({
                "user": user.email,
                "role": user.role,
                "status": status.HTTP_201_CREATED
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordAPIView(APIView):
    
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        user = User.objects.filter(email=email).first()

        if user is None:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        verification_code = randint(10000, 99999)
        user.verification_code = verification_code
        user.verification_code_created_at = timezone.now()
        user.save()
        context = {
            'verification_code': verification_code,
        }

        send_custom_email_task.delay(
            user.email,
            'Сброс пароля',
            'password_reset_email.html',
            context
        )

        return Response({
            "user": user.email,
            "role": user.role,
            "status": status.HTTP_200_OK
        })

        
class VerifyEmailAPIView(APIView):
    serializer_class = VerifyEmailSerializer
    

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.data['email']
            verification_code = serializer.data['verification_code']
            user = User.objects.filter(email=email).first()
            if user is None:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
            if user.verification_code != verification_code:
                return Response({"error": "Incorrect code"}, status=status.HTTP_400_BAD_REQUEST)
            if user.verification_code_created_at + timezone.timedelta(minutes=5) < timezone.now():
                return Response({"error": "Registration code expired. Please request a new code and try again"}, status=status.HTTP_400_BAD_REQUEST)
            
            user.is_active = True
            
            user.verification_code = None
            user.save()
            return Response({
                "status": status.HTTP_200_OK,
                "user": user.email,
                "role": user.role

            })
        return Response(serializer.error, status=status.HTTP_404_NOT_FOUND)
    
        
class SetPasswordAPIView(APIView):
    serializer_class = SetPasswordSerializer


    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            email = serializer.data['email']
            password = serializer.data['password']
            password_confirm = serializer.data['password_confirm']
            user = User.objects.filter(email=email).first()
            if password != password_confirm:
                return Response({"error": "The entered passwords do not match"}, status=status.HTTP_400_BAD_REQUEST)
            user = User.objects.filter(email=serializer.data['email']).first()
            if user is None:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

            
            user.set_password(password)
            user.is_verified_email = True
            user.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                "status": status.HTTP_200_OK,
                "id": user.id,
                "user": user.email,
                "role": user.role,
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            })
        
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)


class UserLoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        
        user = authenticate(request, username=email, password=password)
        if user:  
            if not user.is_verified_email:
                return Response({"error": "Please verify your email address by clicking on the confirmation link sent to your inbox"}, status=status.HTTP_400_BAD_REQUEST)
            
            refresh = RefreshToken.for_user(user)
            return Response({
                
                'id': user.id,
                'email': user.email,
                'role': user.role,
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)





class AccessTokenView(ObtainAuthToken):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user  
        return Response({
            "status": status.HTTP_200_OK,
            "id": user.id,
            "email": user.email, 
            "role": user.role,
        })
    



class ProfileDetailView(ListAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated, IsEmployerPermisson]

    def get_queryset(self):
        profile_id = self.kwargs['id']
        return Profile.objects.filter(id=profile_id)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context

    

class ProfileFilterListView(ListAPIView):
    serializer_class = ProfileAllSerializer
    permission_classes = [IsAuthenticated, IsEmployerPermisson]

    def get_queryset(self):
        vacancy_id = self.kwargs.get('pk')
        employer = self.request.user.id

        vacancy = get_object_or_404(Vacancy, id=vacancy_id)

        profiles_for_vacancy = Profile.objects.annotate(
            vacancy_language_de=F('german'),
            vacancy_language_en=F('english')
        ).filter(
            vacancy_language_de__gte=vacancy.language_german,
            vacancy_language_en__gte=vacancy.language_english
        )

        invited_users = Invitation.objects.filter(employer__id=employer, vacancy__id=vacancy_id).values_list('user', flat=True)

        if vacancy.gender != 'Any':
            # Если пол важен, фильтруем по указанному полу в вакансии
            profiles_for_vacancy = profiles_for_vacancy.filter(gender_en=vacancy.gender)

        queryset = profiles_for_vacancy.exclude(id__in=invited_users)

        return queryset


class ProfileListView(ListAPIView):
    serializer_class = ProfileAllSerializer
    permission_classes = [IsAuthenticated, IsEmployerPermisson]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filter_fields = ['gender_en', 'nationality_en', 'german', 'english',]

    def get_queryset(self):
        return Profile.objects.all()