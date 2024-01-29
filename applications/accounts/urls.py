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
    path('profiles-list-all/', ProfileListAllView.as_view(), name='profile-list-all'),
    # University
    # path('university-list/', UniversityListView.as_view(), name='university-list'),
    # # Passport's
    # path('passport-term-list/', PassportAndTermListView.as_view(), name='passport-term-list'),
    # # Payment & Deal
    # path('payment-list/', PaymentListView.as_view(), name='payment-list'),
    # path('deal-list/', DealListView.as_view(), name='deal-list'),
    # # User
    # path('user-lists/', UserView.as_view(), name='user-list'),
    # # Rating 
    # path('rating-list/', RatingListView.as_view(), name='rating-list'),
    # path('rating/create/', RatingCreateView.as_view(), name='rating-create'),
    # path('rating/<int:pk>/', RatingRetrieveUpdateDestroyAPIView.as_view(), name='rating-detail'),
    # # Review
    # path('review-list/', ReviewCreateAPIView.as_view(), name='review-list'),
    # # WorkExperience
    # path('work-experience-list/', WorkExperienceAPIView.as_view(), name='work-experience-list'),
    # # WorkSchedule
    # path('work-schedule-list/', WorkScheduleAPIView.as_view(), name='work-schedule-list'),
    
]