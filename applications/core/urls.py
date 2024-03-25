from django.urls import path, include
from .views import *
from rest_framework import routers
app_name = 'core'
router = routers.SimpleRouter()
router.register(r'favorite', FavoriteModelViewsets, basename='favorite')
router.register(r'housing', HousingViewSet, basename='housing')

urlpatterns = router.urls
urlpatterns = [ 
    path('',include(router.urls)),
    # employer
    path('employer-profile/', EmployerProfileListAPIView.as_view(), name='employerprofile'),
    path('employercompany/', EmployerCompanyAPIView.as_view(), name='employercompany'),
    path('employercompany-update/', EmployerCompanyUpdateView.as_view(), name='employercompany-update'),
    # branch
    path('branch/', BranchAPIView.as_view(), name='branch'),
    path('branch-update/<int:pk>/', BranchUpdateAPIView.as_view(), name='branch'),
    path('branch-list/', BranchListAPIView.as_view(), name='branchlist'),
    path('branch-detail/', BranchDetailListAPIView.as_view(), name='branchlistdetail'),
    # vacancy
    path('vacancy-create/', VacancyCreateAPIView.as_view(), name='vacancycreate'),
    path('vacancy-update/<int:pk>/', VacancyUpdateAPIView.as_view(), name='vacancyupdate'),
    path('vacancy-list/', VacancyListAPIView.as_view(), name='vacancylist'),
    path('vacancy-detail/<int:pk>/', VacancyDetailAPIView.as_view(), name='vacancydetail'),
    path('vacancy-employer/', EmployerVacancyListAPIView.as_view(), name='vacancy-employer'),
    # invitation
    path('invitation/', InvitationAPIView.as_view(), name='invitation'),
    # interview
    path('interviews-list/', InterviewsModelViewsets.as_view(
        {'get': 'list', }), name='interviews-list'),
    path('interviews-create/', InterviewsAPIView.as_view(), name='interviews-create'),
]
    