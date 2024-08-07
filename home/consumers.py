from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .models import ChatGroup
from asgiref.sync import sync_to_async
import json
from .models import *


# To track of the number of users in each room
room_users_count = {}

class ChatroomConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['chatroom_name']
        self.room_group_name = f'chat_{self.room_name}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # increases users count for the room.
        await self.increase_user_count(self.room_group_name)

        # accepts webSocket connection
        await self.accept()

        # Notify users about updates user count.
        await self.send_user_count()
    
    async def disconnect(self, close_code):

        # decreases users count for the room.
        await self.decrease_user_count(self.room_group_name)

        # leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

        # Notify users about updates user count.
        await self.send_user_count()
    
    # recieves {"message":"Nice post","username":"cypher","room":"public-chat"} from chatSocket in main.js
    async def receive(self, text_data):
        data_json = json.loads(text_data)
        message = data_json['message']
        username = data_json['username']
        room = data_json['room']

        # sends message to channel_layer (room group)
        await self.channel_layer.group_send(
            self.room_group_name, {
                'type': 'chat.message',
                'message': message,
                'username': username,
                'room': room,
            }
        )

        await self.save_message(username, room, message)
    
    # Receive message from above room_group_name and sends to save
    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        room = event['room']

        # send message to Websocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'room': room,
        }))
    
    # saves the message to the database
    @sync_to_async
    def save_message(self, username, room, message):
        user = User.objects.get(username=username)
        group = ChatGroup.objects.get(group_name=room)
        
        # creates the new message.
        GroupMessage.objects.create(group=group, author=user, body=message)
    
    async def send_user_count(self):
        # Sends the current user count to the room group.
        user_count = room_users_count.get(self.room_group_name, 0)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'user_count',
                'user_count': user_count
            }
        )
    
    async def user_count(self, event):
        # Sends user count to WebSocket.
        user_count = event['user_count']
        await self.send(text_data=json.dumps({
            'user_count': user_count
        }))
    
    @sync_to_async
    def increase_user_count(self, room_group_name):
        if room_group_name not in room_users_count:
            room_users_count[room_group_name] = 0
        room_users_count[room_group_name] += 1
    
    @sync_to_async
    def decrease_user_count(self, room_group_name):
        if room_users_count.get(room_group_name, 0) > 0:
            room_users_count[room_group_name] -= 1
        if room_users_count[room_group_name] == 0:
            del room_users_count[room_group_name]