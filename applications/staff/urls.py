from django.urls import include, path
from .views import *



urlpatterns = [
  # сотрудники
  path('employees/', EmployeeListCreateAPIView.as_view(), name='employee-list-create'),
  path('employees/<int:pk>/', EmployeeDetailAPIView.as_view(), name='employee-detail'),
  # компании
  path('employer/company/', EmployerCompanyStaffView.as_view({'get': 'list', 'post': 'create'}), name='employer-company-list'),
  path('employer/company/<int:pk>/', EmployerCompanyStaffView.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='employer-company-detail'),
  # interiew
  path('interview-vacancies/interviews/', InterviewsListAPIView.as_view(), name='interviews-list'),
]
