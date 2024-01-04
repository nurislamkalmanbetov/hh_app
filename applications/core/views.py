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

from rest_framework import viewsets
# from schedule.models import Event
from .models import *
from .serializers import *


class EmployerCompanyAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    # permission_classes = (IsAuthenticated,)
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
            print(serializer.data)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    

class CityListAPIView(ListAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializers
    filter_backends = [filters.SearchFilter]
    search_fields = ['name'] 


class BranchAPIView(APIView):
    # parser_classes = (MultiPartParser, FormParser)
    # permission_classes = (IsAuthenticated,)
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

    @swagger_auto_schema(request_body=BranchSerializers)
    def patch(self, request, *args, **kwargs):
        
        branch_id = kwargs['pk']
        branch = Branch.objects.get(id=branch_id)
        serializer = BranchSerializers(branch, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#пишем гет запрос чтобы вывести филлиал своей компании
class BranchListAPIView(ListAPIView):
    serializer_class = BranchListSerializers
    def get_queryset(self):
        user_id = self.request.query_params.get('user_id', None)
        if user_id is not None:
            employer_company = EmployerCompany.objects.get(user__id=user_id)
            queryset = Branch.objects.filter(company=employer_company)
            return queryset
        else:
            return Response({'error': 'User ID parameter is required.'}, status=status.HTTP_400_BAD_REQUEST)
        

class BranchDetailListAPIView(ListAPIView):
    serializer_class = BranchSerializers
    def get_queryset(self, *args, **kwargs):
        branch_id = self.kwargs['pk']
        queryset = Branch.objects.filter(id=branch_id)
        return queryset
    
