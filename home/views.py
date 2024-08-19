from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import GroupMessageForm

# Create your views here.

def groups(request):
    rooms = ChatGroup.objects.all()
    private_rooms = []
    for chat in PrivateChat.objects.all():
        if request.user.username in chat.name():
            private_rooms.append(chat)
    return render(request, 'home/index.html', {'rooms': rooms, 'private_rooms': private_rooms})

@login_required
def group_chat(request, name):
    rooms = ChatGroup.objects.all()
    private_rooms = []
    for chat in PrivateChat.objects.all():
        if request.user.username in chat.name():
            private_rooms.append(chat)
    print(private_rooms)
    group = get_object_or_404(ChatGroup, group_name=name)
    messages = GroupMessage.objects.filter(group=group)
    data = {'group': group, 'messages':messages, 'rooms': rooms, 'private_rooms': private_rooms, 'room': 'public'}
    return render(request, 'home/group_chat.html', data)

@login_required
def private_chat(request, user1, user2):
    rooms = ChatGroup.objects.all()
    private_rooms = []
    for chat in PrivateChat.objects.all():
        if request.user.username in chat.name():
            private_rooms.append(chat)
    print(private_rooms)
    chat = get_object_or_404(PrivateChat, user1=user1, user2=user2)
    messages = PrivateMessage.objects.filter(chat=chat)
    data = {'chat':chat, 'messages':messages, 'rooms': rooms, 'private_rooms': private_rooms, 'room': 'private'}
    return render(request, 'home/private_chat.html', data)
 