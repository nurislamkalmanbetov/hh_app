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
            #проверка является ли юзер работадателем
            user = User.objects.get(id=request.data['user'])
            if user.role != 'is_employer':
                return Response({'error': 'User is not employer'}, status=status.HTTP_400_BAD_REQUEST)
            employer_company = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(request_body=EmployerCompanySerialzers)
    def patch(self, request, *args, **kwargs):
        user_id = request.query_params.get('user_id', None)
        if user_id is not None:
            employer_company = EmployerCompany.objects.get(user__id=user_id)
            serializer = EmployerCompanySerialzers(employer_company, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)
        else:
            return Response({'error': 'User ID parameter is required.'}, status=status.HTTP_400_BAD_REQUEST)