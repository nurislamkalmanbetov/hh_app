from django.urls import re_path
from .consumers import ChatConsumer

websocket_urlpatterns = [
    # re_path(r'ws/chat/(?P<chat_id>\d+)/$', ChatConsumer.as_asgi()),
    # пишем роут который будет принимать токен
    re_path(r'^ws/chat/(?P<token>[^/]+)/$', ChatConsumer.as_asgi()),


]

