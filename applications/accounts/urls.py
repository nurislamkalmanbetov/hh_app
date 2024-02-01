from django.urls import include, path

from .views import *

urlpatterns = [
    # Custom
    path('signup/', RegistrationAPIView.as_view(), name='signup'),
    path('reset-password/', ResetPasswordAPIView.as_view(), name='reset-password'),
    path('verify-email/', VerifyEmailAPIView.as_view(), name='verify-email'),
    path('set-password/', SetPasswordAPIView.as_view(), name='set-password'),
    path('signin/', UserLoginView.as_view(), name='signin'),
    path('token/', AccessTokenView.as_view(), name='token_refresh'),
    # Profile
    path('profile-detail/<int:id>/', ProfileDetailView.as_view(), name='profile-list'),
    path('profiles-list-filter/<int:pk>/', ProfileFilterListView.as_view(), name='profile-list-all'),
    path('profile-list/', ProfileListView.as_view(), name='profile-list'),

    
]