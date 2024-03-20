from django.urls import path, include
from .views import *
from rest_framework import routers
app_name = 'core'
router = routers.SimpleRouter()
router.register(r'favorite', FavoriteModelViewsets, basename='favorite')


urlpatterns = router.urls
urlpatterns = [ 
    path('',include(router.urls)),
    path('employer-profile/', EmployerProfileListAPIView.as_view(), name='employerprofile'),
    path('employercompany/', EmployerCompanyAPIView.as_view(), name='employercompany'),
    path('employercompany-update/', EmployerCompanyUpdateView.as_view(), name='employercompany-update'),
    path('branch/', BranchAPIView.as_view(), name='branch'),
    path('branch-update/<int:pk>/', BranchUpdateAPIView.as_view(), name='branch'),
    path('branch-list/', BranchListAPIView.as_view(), name='branchlist'),
    path('branch-detail/', BranchDetailListAPIView.as_view(), name='branchlistdetail'),
    

    path('housing/', HousingAPIView.as_view(), name='housing'),
    path('housing-list/', HousingListAPIView.as_view(), name='housinglist'),

    path('vacancy-create/', VacancyCreateAPIView.as_view(), name='vacancycreate'),
    path('vacancy-update/<int:pk>/', VacancyUpdateAPIView.as_view(), name='vacancyupdate'),
    path('vacancy-list/', VacancyListAPIView.as_view(), name='vacancylist'),
    path('vacancy-detail/<int:pk>/', VacancyDetailAPIView.as_view(), name='vacancydetail'),
    path('vacancy-employer/', EmployerVacancyListAPIView.as_view(), name='vacancy-employer'),

    path('invitation/', InvitationAPIView.as_view(), name='invitation'),

    path('interviews-list/', InterviewsModelViewsets.as_view(
        {'get': 'list', }), name='interviews-list'),
    path('interviews-create/', InterviewsAPIView.as_view(), name='interviews-create'),
]
    