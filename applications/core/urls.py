from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter


# router = DefaultRouter()
# router.register(r'events', EventViewSet)

urlpatterns = [ 
    path('employerprofile/<int:pk>/', EmployerProfileListAPIView.as_view(), name='employerprofile'),
    path('employercompany/', EmployerCompanyAPIView.as_view(), name='employercompany'),
    path('employercompany-update/<int:pk>/', EmployerCompanyUpdateView.as_view(), name='employercompany'),

    path('branch/', BranchAPIView.as_view(), name='branch'),
    # path('branch-update/<int:pk>/', BranchUpdateView.as_view(), name='branch'),
    path('branch-list/', BranchListAPIView.as_view(), name='branchlist'),
    path('branch-detail/<int:pk>/', BranchDetailListAPIView.as_view(), name='branchlistdetail'),

    path('city/', CityListAPIView.as_view(), name='city'),


]
