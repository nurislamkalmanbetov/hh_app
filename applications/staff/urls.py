


from django.urls import include, path
from .views import *


urlpatterns = [
  # сотрудники
  path('employees/', EmployeeListCreateAPIView.as_view(), name='employee-list-create'),
  path('employees/<int:pk>/', EmployeeDetailAPIView.as_view(), name='employee-detail'),

  path('employer/company/update/', EmployerCompanyUpdateView.as_view(), name='employer-company-update'),

  path('interview-vacancies/interviews/', InterviewsListAPIView.as_view(), name='interviews-list'),
]