from datetime import date, datetime, timedelta

from applications.accounts.models import User
from django_filters import rest_framework as django_filters
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import filters, generics, status
from rest_framework.generics import (GenericAPIView, ListAPIView,
                                     UpdateAPIView, mixins)
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
# from schedule.models import Event
from .models import *
from .serializers import *
from .permissions import IsEmployerPermisson
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from applications.staff.models import Notification
from drf_spectacular.utils import extend_schema


class EmployerProfileListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated, IsEmployerPermisson]
    serializer_class = EmployerProfileSerializers
    def get_queryset(self, *args, **kwargs):
        user_id = self.request.user.id
        queryset = EmployerCompany.objects.filter(user__id=user_id)
        return queryset


class EmployerCompanyAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated, IsEmployerPermisson]

    def get(self, request, *args, **kwargs):
        user_id = request.user.id

        employer_company = EmployerCompany.objects.filter(user__id=user_id)
        serializer = EmployerCompanySerialzers(employer_company, many=True, context={'request': request})
        return Response(serializer.data)


    def post(self, request, *args, **kwargs):
        serializer = EmployerCompanySerialzers(data=request.data)
   
        if serializer.is_valid():
            user = request.user
            serializer.save(user=user)
       
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmployerCompanyUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = EmployerUpdateSerialzers
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated, IsEmployerPermisson]


    def patch(self, request, *args, **kwargs):
        user_id = request.user.id
        user = User.objects.get(id=user_id)

        employer_company = EmployerCompany.objects.get(user=user)
        serializer = EmployerUpdateSerialzers(employer_company, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    



class BranchAPIView(APIView):
    permission_classes = [IsAuthenticated, IsEmployerPermisson]
 
    def post(self, request, *args, **kwargs):
        serializer = BranchSerializers(data=request.data)
        if serializer.is_valid():
            user_id = request.user.id
            employer_company = get_object_or_404(EmployerCompany, user__id=user_id)

         
            serializer.save(company=employer_company)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BranchUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated, IsEmployerPermisson]

    def patch(self, request, *args, **kwargs):
        branch_id = self.kwargs['pk']
        branch = Branch.objects.get(id=branch_id)
        user = request.user
        serializer = BranchSerializers(branch, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BranchListAPIView(ListAPIView):
    serializer_class = BranchListSerializers
    permission_classes = [IsAuthenticated, IsEmployerPermisson]
    def get_queryset(self):
        user_id = self.request.user.id
        queryset = Branch.objects.filter(company__user__id=user_id).select_related( 'company')
        return queryset
        
class BranchDetailListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated, IsEmployerPermisson]
    serializer_class = BranchSerializers

    def get_queryset(self):
        branch_id = self.request.query_params.get('branch_id', None)
        if not branch_id:
            return Branch.objects.none()
        
        # Используйте filter(id=branch_id) вместо filter(branch=branch)
        branch = get_object_or_404(Branch, id=branch_id)
        queryset = Branch.objects.filter(id=branch.id).select_related('company')
        return queryset


class HousingAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated, IsEmployerPermisson]
    @extend_schema(request=HousingSerializers)
    def post(self, request, *args, **kwargs):
        serializer = HousingSerializers(data=request.data)
        if serializer.is_valid():
            user_id = request.user.id
            try:

                employer_company = EmployerCompany.objects.get(id=user_id)
            except EmployerCompany.DoesNotExist:
                return Response({'error': 'Add a company to add applications'}, status=status.HTTP_400_BAD_REQUEST)
            housing = serializer.save(employer=employer_company)
        

            files_data = request.FILES.getlist('files')  # Получаем список видео
            for file_data in files_data:
                FilesHousing.objects.create(housing=housing, files=file_data)
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class HousingListAPIView(ListAPIView):
    serializer_class = HousingListSerializers
    permission_classes = [IsAuthenticated, IsEmployerPermisson]
    def get_queryset(self):
        user_id = self.request.user.id
        queryset = Housing.objects.filter(employer__user__id=user_id).select_related('employer',)
        return queryset

class VacancyCreateAPIView(APIView):
    permission_classes = [IsAuthenticated, IsEmployerPermisson]

    @extend_schema(request=VacancySerializers)
    def post(self, request, *args, **kwargs):
        serializer = VacancySerializers(data=request.data)
        if serializer.is_valid():
            user_id  = request.user.id
            branch = request.data.get('branch')

            user = EmployerCompany.objects.get(user__id=user_id)
        
            #выводим только его филлиалы и проверяем есть ли у него такой филлиал
            branch = Branch.objects.filter(company=user).filter(id=branch).first()

            if user is None:
                return Response({'error': 'Add a company to add applications'}, status=status.HTTP_400_BAD_REQUEST)
            
            if branch is None:
                return Response({'error': 'Branch is missing.'}, status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save(employer_company=user, branch=branch,)
            channel_layer = get_channel_layer()
            notification_data = {
                 
                'notification': 'Новый заказ',
                'employer': f'{user.first_name}-{user.last_name}',
                'employer_id': user.id,
                'branch': branch.name,
                'employee_count': serializer.data['employee_count'],
                'branch_id': branch.id,
            }

            # Сохраняем уведомление в модель Notification
            notification_save = Notification.objects.create(data=notification_data, type_notification='vacancy_notification')
            notification_save.save()
            result = {
                'type': 'interviews_message',
                'type_notification': 'vacancy_notification',
                'id': notification_save.id,
                'message': notification_save.data,
                'read': notification_save.read,
                'notification_date': notification_save.created_at.strftime('%Y-%m-%d %H:%M'),
            }

            async_to_sync(channel_layer.group_send)('notification', result)


            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class VacancyUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated, IsEmployerPermisson]


    def patch(self, request, *args, **kwargs):
        vacancy_id = kwargs['pk']
        vacancy = Vacancy.objects.get(id=vacancy_id)
        
        serializer = VacancySerializers(vacancy, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VacancyListAPIView(ListAPIView):
    serializer_class = VacancyListSerializers
    filter_backends = [filters.SearchFilter]
    search_fields = ['branch__name',]

    def get_queryset(self):
        queryset = Vacancy.objects.all().select_related('employer_company', 'branch', )
        return queryset
    



class VacancyDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        vacancy_id = kwargs['pk']
        vacancy = Vacancy.objects.filter(id=vacancy_id).select_related(
            'employer_company',
            'branch',
        ).first()

        if vacancy is None:
            return Response({'error': 'Vacancy is missing.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = VacancyDetailSerializers(vacancy, context={'request': request})
        return Response(serializer.data)



class EmployerVacancyListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated, IsEmployerPermisson]

    serializer_class = VacancyListSerializers

    def get_queryset(self):
        user_id = self.request.user.id
        user = get_object_or_404(EmployerCompany, user__id=user_id)
        queryset = Vacancy.objects.filter(employer_company=user).select_related('employer_company', 'branch',)
        return queryset


class InvitationAPIView(APIView):
    permission_classes = [IsAuthenticated, IsEmployerPermisson]


    def get(self, request, *args, **kwargs):
        user_id = request.user.id
        invitation = Invitation.objects.filter(employer__user__id=user_id).select_related('employer', 'vacancy', 'user',)
        serializer = InvitationSerializers(invitation, many=True,  context={'request': request})
        return Response(serializer.data)


    def post(self, request, *args, **kwargs):
        serializer = InvitationSerializers(data=request.data)
        if serializer.is_valid():
            user_id = request.user.id
            vacancy = request.data.get('vacancy')
            user = request.data.get('user')
            invitation = Invitation.objects.filter(employer__user__id=user_id).filter(vacancy=vacancy).filter(user=user).first()
            if invitation is not None:
                return Response({'error': 'You have already invited this applicant'}, status=status.HTTP_400_BAD_REQUEST)
            user = EmployerCompany.objects.get(user__id=user_id)
            vacancy = Vacancy.objects.filter(employer_company=user).filter(id=vacancy).first()
            if vacancy is None:
                return Response({'error': 'Vacancy is missing.'}, status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save(employer=user, vacancy=vacancy)
     
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    




class InterviewsModelViewsets(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated, IsEmployerPermisson]
    serializer_class = InterviewsListSerializers
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['vacancy', ]


    def get_queryset(self):
        user_id = self.request.user.id
        queryset = Interviews.objects.filter(employer__user__id=user_id).select_related('vacancy',).prefetch_related('user',)
        return queryset



class InterviewsAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, IsEmployerPermisson]
    serializer_class = InterviewsSerializers
    


    def post(self, request, *args, **kwargs):
        serializer = InterviewsSerializers(data=request.data)
        print('data', request.data)
        if serializer.is_valid():
            user_id = request.user.id
            vacancy = request.data.get('vacancy')
            user = serializer.validated_data.get('user')
            print('user', user)
            employer = EmployerCompany.objects.get(user__id=user_id)

            vacancy = Vacancy.objects.filter(employer_company=employer, id=vacancy).first()
            if not vacancy:
                return Response({'error': 'Vacancy is missing.'}, status=status.HTTP_400_BAD_REQUEST)
            
            channel_layer = get_channel_layer()

            serializer.save(employer=employer, vacancy=vacancy)
            
            notification_data = {
                'notification': 'Запрос на собеседование',
                'vacancy_id': vacancy.id,
                'employer': f'{employer.first_name}-{employer.last_name}',
                'employer_id': employer.id,
                'user_profile_id': [user.id for user in user],  # Передаем список идентификаторов пользователей
            }
            print(serializer.data)
            
            # Сохраняем уведомление в модель Notification
            notification_save = Notification.objects.create(data=notification_data, type_notification='interviews_notification')
            notification_save.save()
            result = {
                'type': 'interviews_message',
                'type_notification': 'interviews_notification',
                'id': notification_save.id,
                'message': notification_save.data,
                'read': notification_save.read,
                'notification_date': notification_save.created_at.strftime('%Y-%m-%d %H:%M'),
            }
            
            async_to_sync(channel_layer.group_send)('notification', result)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    




class FavoriteModelViewsets(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsEmployerPermisson]
    serializer_class = FavoriteListSerializers
    @extend_schema(
            description='Получение списка избранных студентов',
            responses=FavoriteListSerializers,
            

    )
    def get_queryset(self):
        user_id = self.request.user.id
        queryset = Favorite.objects.filter(employer__user__id=user_id).select_related('user',)
        return queryset
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @extend_schema(
            description='Добавление в избранное',
            request=FavoriteSerializers,
            

    )
    def create(self, request, *args, **kwargs):
        serializer = FavoriteSerializers(data=request.data)
        user_id = request.user.id
        user = request.data.get('user')
        
        # Получаем объект Profile, соответствующий переданному идентификатору пользователя
        try:
            profile = Profile.objects.get(id=user)
        except Profile.DoesNotExist:
            return Response({'error': 'Profile with given ID does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Проверяем, не добавлен ли уже этот пользователь в избранное
        favorite = Favorite.objects.filter(employer__user__id=user_id, user=profile).exists()
        if favorite:
            # Если пользователь уже добавлен в избранное, удаляем его
            favorite = Favorite.objects.filter(employer__user__id=user_id, user=profile).delete()
            return Response({'is_favorite':False}, status=status.HTTP_200_OK)
        
        # Получаем работодателя и сохраняем в избранное
        employer = EmployerCompany.objects.get(user__id=user_id)
        serializer.is_valid(raise_exception=True)
        serializer.save(employer=employer, user=profile)  # передаем profile вместо user
        
        return Response({'is_favorite':True}, status=status.HTTP_201_CREATED)
    
    

