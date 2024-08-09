from django.contrib import admin
from .models import ChatGroup, GroupMessage, PrivateChat, PrivateMessage

# Register your models here.

admin.site.register(ChatGroup)
admin.site.register(GroupMessage)
admin.site.register(PrivateChat)
admin.site.register(PrivateMessage)