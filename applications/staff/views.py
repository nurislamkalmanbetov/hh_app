from django.shortcuts import render

from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.db.models import Q, Exists, OuterRef

from rest_framework.parsers import  MultiPartParser

from rest_framework import generics, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, status
from rest_framework.generics import ListAPIView
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from applications.staff.permissions import IsEmployeePermission
from applications.accounts.serializers import ProfileSerializer, ProfileAllSerializer
from applications.core.serializers import InterviewsListSerializers

from .serializers import *
from ..accounts.models import *
from .permissions import IsEmployeePermission



class EmployeeListCreateAPIView(generics.ListCreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

class EmployeeDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class EmployerCompanyStaffView(ModelViewSet):
    serializer_class = StaffEmployerUpdateSerialzers
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated, IsEmployeePermission]
    queryset = EmployerCompany.objects.all()  # Здесь устанавливаем нужный набор данных



    

class EmployerCompanyUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = StaffEmployerUpdateSerialzers
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated, IsEmployeePermission]
    queryset = EmployerCompany.objects.all()  # Здесь устанавливаем нужный набор данных

    def patch(self, request, *args, **kwargs):
        user_id = request.user.id
        user = User.objects.get(id=user_id)

        employer_company = EmployerCompany.objects.get(user=user)
        serializer = StaffEmployerUpdateSerialzers(
            employer_company, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    



class InterviewsListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, IsEmployeePermission]
    serializer_class = InterviewsListSerializers
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['vacancy', 'is_accepted', 'is_work', 'is_rejected', 'is_passed']

    def get_queryset(self):
        """
        Возвращает все объекты интервью.
        """
        return Interviews.objects.all()
    


