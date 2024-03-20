from django.shortcuts import render

from rest_framework import generics
from rest_framework.response import Response
from .serializers import *
from ..accounts.models import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import (ListAPIView)
from rest_framework import generics, status
# from drf_yasg2.utils import swagger_auto_schema
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.parsers import  MultiPartParser
from .permissions import IsEmployeePermission
from rest_framework.exceptions import PermissionDenied
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.views import APIView





class EmployeeListCreateAPIView(generics.ListCreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

class EmployeeDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer



class EmployerCompanyUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = StaffEmployerUpdateSerialzers
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated, IsEmployeePermission]

    # @swagger_auto_schema(
    #     operation_summary="Обновить информацию  работодателя",
    #     request_body=StaffEmployerUpdateSerialzers,
    # )
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

    # @swagger_auto_schema(operation_summary="Получить информацию работодателя")
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    # @swagger_auto_schema(
    #     operation_summary="Изменить информацию работодателя",
    #     request_body=StaffEmployerUpdateSerialzers,
    # )
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    

from applications.core.permissions import IsEmployerPermisson
from applications.staff.permissions import IsEmployeePermission

from applications.core.serializers import InterviewsListSerializers


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



# from rest_framework.response import Response

# class InterviewsListAPIView(generics.ListAPIView):
#     permission_classes = [IsAuthenticated, IsEmployeePermission]
#     serializer_class = InterviewsListSerializers

#     def get(self, request, *args, **kwargs):
#         vacancy_id = self.kwargs.get('vacancy_id')
#         interviews = Interviews.objects.filter(vacancy__id=vacancy_id)
#         serializer = self.serializer_class(interviews, many=True)
#         return Response(serializer.data)