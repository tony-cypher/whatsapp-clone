from django.urls import path
from . import views

urlpatterns = [
    path('', views.groups, name='home'),
    path('<str:name>/', views.group_chat, name='group_chat'),
    path('private/<int:user1>/<int:user2>/', views.private_chat, name='private_chat'),
]
