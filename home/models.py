from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class ChatGroup(models.Model):
    group_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.group_name


class GroupMessage(models.Model):
    group = models.ForeignKey(ChatGroup, related_name='chat_messages', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author.username}: {self.body}'
    
    class Meta:
        ordering = ['-created']


class PrivateChat(models.Model):
    user1 = models.ForeignKey(User, related_name='chat_user1', on_delete=models.CASCADE)
    user2 = models.ForeignKey(User, related_name='chat_user2', on_delete=models.CASCADE)

    def __str__(self):
        return f'Chat between {self.user1.username} and {self.user2.username}'
    
    def get_chat_name(self):
        return f'Private_{min(self.user1.id, self.user2.id)}_{max(self.user1.id, self.user2.id)}'
    
    def name(self):
        return f'{self.user1} and {self.user2}'


class PrivateMessage(models.Model):
    chat = models.ForeignKey(PrivateChat, related_name='messages', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author.username}: {self.body}'

    class Meta:
        ordering = ['-created']