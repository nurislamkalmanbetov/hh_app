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


class EmployerProfileListAPIView(ListAPIView):
    #сделаем по int pk user id
    permission_classes = [IsAuthenticated]
    serializer_class = EmployerProfileSerializers
    def get_queryset(self, *args, **kwargs):
        user_id = self.kwargs['pk']
        queryset = EmployerCompany.objects.filter(user__id=user_id).select_related('user')
        return queryset


class EmployerCompanyAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        user_id = request.query_params.get('user_id', None)
        if user_id is not None:
            employer_company = EmployerCompany.objects.select_related('user').filter(user__id=user_id)

            serializer = EmployerCompanySerialzers(employer_company, many=True)
            return Response(serializer.data)
        else:
            
            return Response({'error': 'User ID parameter is required.'}, status=status.HTTP_400_BAD_REQUEST)
        
    @swagger_auto_schema(request_body=EmployerCompanySerialzers)
    def post(self, request, *args, **kwargs):
        serializer = EmployerCompanySerialzers(data=request.data)
        if serializer.is_valid():
         
            user = User.objects.get(id=request.data['user'])
            if user.role != 'is_employer':
                return Response({'error': 'User is not employer'}, status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class EmployerCompanyUpdateView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(request_body=EmployerUpdateSerialzers)
    def patch(self, request, *args, **kwargs):
        
        user_id = kwargs['pk']
        user = User.objects.get(id=user_id)
        if user.role != 'is_employer':
            return Response({'error': 'User is not employer'}, status=status.HTTP_400_BAD_REQUEST)
        employer_company = EmployerCompany.objects.get(user=user)
        serializer = EmployerUpdateSerialzers(employer_company, data=request.data, partial=True)
        
        if serializer.is_valid():
            
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    

class CityListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = City.objects.all()
    serializer_class = CitySerializers
    filter_backends = [filters.SearchFilter]
    search_fields = ['name'] 


class BranchAPIView(APIView):
    # parser_classes = (MultiPartParser, FormParser)
    permission_classes = (IsAuthenticated,)
    @swagger_auto_schema(request_body=BranchSerializers)
    def post(self, request, *args, **kwargs):
        serializer = BranchSerializers(data=request.data)
        if serializer.is_valid():
            employer_company_id = request.data.get('company')
            if employer_company_id is None:
                return Response({'error': 'Employer company ID is missing.'}, status=status.HTTP_400_BAD_REQUEST)

         
            employer_company = EmployerCompany.objects.get(id=employer_company_id)

            if employer_company.user.role != 'is_employer':
                return Response({'error': 'User is not employer'}, status=status.HTTP_400_BAD_REQUEST)
            
            branch = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BranchUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(request_body=BranchSerializers)
    def patch(self, request, *args, **kwargs):
        branch_id = self.kwargs['pk']
        branch = Branch.objects.get(id=branch_id)
        
        serializer = BranchSerializers(branch, data=request.data, partial=True)
        
        if serializer.is_valid():
            print(serializer)
            serializer.save()
            print(serializer)

            # Возвращаем обновленные данные после успешного сохранения
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BranchListAPIView(ListAPIView):
    serializer_class = BranchListSerializers
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        company_id = self.request.query_params.get('company_id', None)
        if not company_id:
            return Branch.objects.none()
        
        company = get_object_or_404(EmployerCompany, id=company_id)
        queryset = Branch.objects.filter(company=company).select_related('city', 'company')
        return queryset
        
class BranchDetailListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BranchSerializers

    def get_queryset(self):
        branch_id = self.request.query_params.get('branch_id', None)
        if not branch_id:
            return Branch.objects.none()
        
        # Используйте filter(id=branch_id) вместо filter(branch=branch)
        branch = get_object_or_404(Branch, id=branch_id)
        queryset = Branch.objects.filter(id=branch.id).select_related('city', 'company')
        return queryset

    

class PositionEmployeeAPIView(APIView):
    # permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        user_id = request.query_params.get('user_id', None)
        if user_id is not None:
            position_employee = PositionEmployee.objects.select_related('employer').filter(employer__id=user_id)

            serializer = PositionEmployeeSerializers(position_employee, many=True)
            return Response(serializer.data)
        else:
            
            return Response({'error': 'User ID parameter is required.'}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=PositionEmployeeSerializers)
    def post(self, request, *args, **kwargs):
        serializer = PositionEmployeeSerializers(data=request.data)
        if serializer.is_valid():
            user_id = request.data.get('employer')
            user = User.objects.get(id=user_id)
            if user.role != 'is_employer':
                return Response({'error': 'User is not employer'}, status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PositionEmployeeDeleteAPIView(APIView):
    # permission_classes = [IsAuthenticated]
    def delete(self, request, *args, **kwargs):
        position_employee_id = kwargs['pk']
        position_employee = PositionEmployee.objects.get(id=position_employee_id)
        position_employee.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class VacancyCreateAPIView(APIView):
    @swagger_auto_schema(request_body=VacancySerializers)
    def post(self, request, *args, **kwargs):
        serializer = VacancySerializers(data=request.data)
        if serializer.is_valid():
            user_id  = request.data.get('user_id')
            branch = request.data.get('branch')
            position = request.data.get('position')
  
            user = EmployerCompany.objects.get(user__id=user_id)
            #выводим только его филлиалы и проверяем есть ли у него такой филлиал
            branch = Branch.objects.filter(company=user).filter(id=branch).first()
            position = PositionEmployee.objects.filter(employer=user_id).filter(id=position).first()
         
    
            if user_id is None:
                return Response({'error': 'User ID is missing.'}, status=status.HTTP_400_BAD_REQUEST)
            
            if user is None:
                return Response({'error': 'Вы еще не добавили компанию'}, status=status.HTTP_400_BAD_REQUEST)
            
            if user.user.role != 'is_employer':
                return Response({'error': 'Вы не работодатель'}, status=status.HTTP_400_BAD_REQUEST)
            
            if branch is None:
                return Response({'error': 'Branch is missing.'}, status=status.HTTP_400_BAD_REQUEST)
            
            if position is None:
                return Response({'error': 'Position is missing.'}, status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class VacancyListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = VacancyListSerializers
    filter_backends = [filters.SearchFilter]
    search_fields = ['position__name', 'branch__name',]

    def get_queryset(self):
        queryset = Vacancy.objects.all().select_related('employer_company', 'branch', 'position')
        return queryset

class VacancyDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        vacancy_id = kwargs['pk']
        vacancy = Vacancy.objects.filter(id=vacancy_id).select_related('employer_company', 'branch', 'position').first()
        if vacancy is None:
            return Response({'error': 'Vacancy is missing.'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = VacancyDetailSerializers(vacancy)
        return Response(serializer.data)


class EmployerVacancyListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = VacancyListSerializers

    def get_queryset(self):
        user_id = self.request.query_params.get('user_id', None)
        if not user_id:
            return Vacancy.objects.none()
        
        user = get_object_or_404(EmployerCompany, user__id=user_id)
        queryset = Vacancy.objects.filter(employer_company=user).select_related('employer_company', 'branch', 'position')
        return queryset