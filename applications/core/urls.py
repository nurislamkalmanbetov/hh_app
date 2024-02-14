from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter


# router = DefaultRouter()
# router.register(r'events', EventViewSet)

urlpatterns = [ 
    path('employer-profile/', EmployerProfileListAPIView.as_view(), name='employerprofile'),
    path('employercompany/', EmployerCompanyAPIView.as_view(), name='employercompany'),
    path('employercompany-update/', EmployerCompanyUpdateView.as_view(), name='employercompany-update'),

    path('branch/', BranchAPIView.as_view(), name='branch'),
    path('branch-update/<int:pk>/', BranchUpdateAPIView.as_view(), name='branch'),
    path('branch-list/', BranchListAPIView.as_view(), name='branchlist'),
    path('branch-detail/', BranchDetailListAPIView.as_view(), name='branchlistdetail'),
    
    path('city/', CityListAPIView.as_view(), name='city'),
    
    path('positionemployee/', PositionEmployeeAPIView.as_view(), name='positionemployee'),
    path('positionemployee-delete/<int:pk>/', PositionEmployeeDeleteAPIView.as_view(), name='positionemployee'),
    
    path('vacancy-create/', VacancyCreateAPIView.as_view(), name='vacancycreate'),
    path('vacancy-update/<int:pk>/', VacancyUpdateAPIView.as_view(), name='vacancyupdate'),
    path('vacancy-list/', VacancyListAPIView.as_view(), name='vacancylist'),
    path('vacancy-detail/<int:pk>/', VacancyDetailAPIView.as_view(), name='vacancydetail'),
    path('vacancy-employer/', EmployerVacancyListAPIView.as_view(), name='vacancy-employer'),

    path('invitation/', InvitationAPIView.as_view(), name='invitation'),

    
]
    