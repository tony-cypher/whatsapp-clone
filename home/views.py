from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import ChatGroup, GroupMessage
from .forms import GroupMessageForm

# Create your views here.

def groups(request):
    rooms = ChatGroup.objects.all()
    return render(request, 'home/index.html', {'rooms': rooms})

@login_required
def group_chat(request, name):
    group = get_object_or_404(ChatGroup, group_name=name)
    print(group)
    messages = GroupMessage.objects.filter(group=group)
    return render(request, 'home/group_chat.html', {'group': group, 'messages':messages})