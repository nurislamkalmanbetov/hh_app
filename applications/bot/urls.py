from django.urls import path
from .views import *

urlpatterns = [
    path('create_telegram_user/', TelegramUserListCreateAPIView.as_view(), name='create_telegram_user'),
    path('telegram_user_list/', TelegramUserListView.as_view(), name='telegram_user_list'),
]



