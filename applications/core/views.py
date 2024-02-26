from datetime import date, datetime, timedelta

from applications.accounts.models import User
from django_filters import rest_framework as django_filters
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg2.utils import swagger_auto_schema
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

    @swagger_auto_schema(request_body=EmployerCompanySerialzers)
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

    @swagger_auto_schema(request_body=EmployerUpdateSerialzers)
    def patch(self, request, *args, **kwargs):
        user_id = request.user.id
        user = User.objects.get(id=user_id)

        employer_company = EmployerCompany.objects.get(user=user)
        serializer = EmployerUpdateSerialzers(employer_company, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    

class CountryListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Country.objects.all()
    serializer_class = CountrySerializers
    filter_backends = [filters.SearchFilter]
    search_fields = ['name'] 


class BranchAPIView(APIView):
    permission_classes = [IsAuthenticated, IsEmployerPermisson]
    @swagger_auto_schema(request_body=BranchSerializers)
    def post(self, request, *args, **kwargs):
        serializer = BranchSerializers(data=request.data)
        if serializer.is_valid():
            user_id = request.user.id
            employer_company = EmployerCompany.objects.get(user__id=user_id)
            serializer.save(company=employer_company)
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BranchUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated, IsEmployerPermisson]
    @swagger_auto_schema(request_body=BranchSerializers)
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
        queryset = Branch.objects.filter(company__user__id=user_id).select_related('country', 'company')
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
        queryset = Branch.objects.filter(id=branch.id).select_related('country', 'company')
        return queryset


class HousingAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        serializer = HousingSerializers(data=request.data)
        if serializer.is_valid():
            user_id = request.data.get('employer')
            employer_company = EmployerCompany.objects.get(id=user_id)
            print(request.data)
            # Сохраняем объект жилья
            housing = serializer.save(employer=employer_company)
        

            files_data = request.FILES.getlist('files')  # Получаем список видео
            for file_data in files_data:
                FilesHousing.objects.create(housing=housing, files=file_data)
            
            # Возвращаем успешный ответ
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class VacancyCreateAPIView(APIView):
    permission_classes = [IsAuthenticated, IsEmployerPermisson]

    @swagger_auto_schema(request_body=VacancySerializers)
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
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class VacancyUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated, IsEmployerPermisson]

    @swagger_auto_schema(request_body=VacancySerializers)
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

    @swagger_auto_schema(request_body=InvitationSerializers)
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
    permission_classes = [IsAuthenticated, IsEmployerPermisson]
    serializer_class = InterviewsListSerializers
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['vacancy',]


    def get_queryset(self):
        user_id = self.request.user.id
        queryset = Interviews.objects.filter(employer__user__id=user_id).select_related('vacancy', 'user',)
        return queryset

class InterviewsAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, IsEmployerPermisson]
    serializer_class = InterviewsSerializers



    @swagger_auto_schema(request_body=InterviewsSerializers)
    def post(self, request, *args, **kwargs):
        serializer = InterviewsSerializers(data=request.data)
        if serializer.is_valid():
            user_id = request.user.id
            vacancy = request.data.get('vacancy')
            user = request.data.get('user')
            invitation = Interviews.objects.filter(employer__user__id=user_id).filter(vacancy=vacancy).filter(user=user).first()
            if invitation is not None:
                return Response({'error': 'You have already invited this applicant'}, status=status.HTTP_400_BAD_REQUEST)
            user = EmployerCompany.objects.get(user__id=user_id)
            vacancy = Vacancy.objects.filter(employer_company=user).filter(id=vacancy).first()
            if vacancy is None:
                return Response({'error': 'Vacancy is missing.'}, status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save(employer=user, vacancy=vacancy)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FavoriteListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated, IsEmployerPermisson]
    serializer_class = FavoriteListSerializers

    def get_queryset(self):
        user_id = self.request.user.id
        queryset = Favorite.objects.filter(employer__user__id=user_id).select_related('user',)
        return queryset
    


class FavoriteAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, IsEmployerPermisson]
    serializer_class = FavoriteSerializers

    def post(self, request, *args, **kwargs):
        user_id = request.user.id
        serializer = self.get_serializer(data=request.data)
        user = request.data.get('user')
        
        # Проверяем, не добавлен ли уже этот пользователь в избранное
        if Favorite.objects.filter(employer__user__id=user_id, user=user).exists():
            return Response({'error': 'You have already added this user to favorites'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Получаем работодателя и сохраняем в избранное
        employer = EmployerCompany.objects.get(user__id=user_id)
        serializer.is_valid(raise_exception=True)
        serializer.save(employer=employer)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)