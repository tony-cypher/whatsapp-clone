from django.urls import path
from .consumers import *

websocket_urlpatterns = [
    path('ws/chatroom/<str:chatroom_name>/', ChatroomConsumer.as_asgi()),
    path('ws/private_chat/<str:chatroom_name>/', PrivateChatConsumer.as_asgi()),
]