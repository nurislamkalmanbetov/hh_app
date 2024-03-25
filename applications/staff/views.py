from django.shortcuts import render

from rest_framework import generics
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.parsers import  MultiPartParser
from rest_framework.exceptions import PermissionDenied
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import (ListAPIView)
from rest_framework import generics, status
from rest_framework.viewsets import ModelViewSet

from .serializers import *
from ..accounts.models import *
from ..core.models import *

from django_filters.rest_framework import DjangoFilterBackend

from .permissions import IsEmployeePermission

from applications.staff.permissions import IsEmployeePermission
from applications.core.serializers import *





class EmployeeListCreateAPIView(generics.ListCreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class EmployerCompanyStaffView(ModelViewSet):
    serializer_class = StaffEmployerUpdateSerialzers
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated, IsEmployeePermission]
    queryset = EmployerCompany.objects.all()  



class EmployerCompanyUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = StaffEmployerUpdateSerialzers
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated, IsEmployeePermission]


    def patch(self, request, *args, **kwargs):
        """
        Изменяет объекты интервью по айди. Прям Все!!
        """
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

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    



class InterviewsListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, IsEmployeePermission]
    serializer_class = InterviewsListSerializers
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['vacancy', 'is_accepted', 'is_work', 'is_rejected', 'is_passed']

    def get_queryset(self):
        """
        Возвращает все объекты интервью. Прям Все!!
        """
        return Interviews.objects.all()



# class EmployerCompanyStaffView(generics.RetrieveAPIView):
#     permission_classes = [IsAuthenticated, IsEmployeePermission]
#     serializer_class = EmployerCompanySerialzers
#     queryset = EmployerCompany.objects.all()


# class EmployerCompanyStaffCreta(generics.CreateAPIView):
#     permission_classes = [IsAuthenticated, IsEmployeePermission]
#     serializer_class = EmployerCompanySerialzers
    # queryset = EmployerCompany.objects.all()