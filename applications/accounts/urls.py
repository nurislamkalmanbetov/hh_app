from django.urls import include, path

from .views import *

urlpatterns = [
    path('signup/', RegistrationAPIView.as_view(), name='signup'),
    path('verify-email/', VerifyEmailAPIView.as_view(), name='verify-email'),
    path('set-password/', SetPasswordAPIView.as_view(), name='set-password'),
    path('signin/', UserLoginView.as_view(), name='signin'),
    path('reset-password/', ResetPasswordAPIView.as_view(), name='reset-password'),
]



