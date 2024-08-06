from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from asgiref.sync import sync_to_async
import json
from .models import *

class ChatroomConsumer(AsyncWebsocketConsumer):
    print('Inside ChatConsumer')
    
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['chatroom_name']
        self.room_group_name = f'chat_{self.room_name}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    # recieves {"message":"Nice post","username":"cypher","room":"public-chat"} from chatSocket in main.js
    async def receive(self, text_data):
        data_json = json.loads(text_data)
        message = data_json['message']
        username = data_json['username']
        room = data_json['room']

        # sends message to channel_layer
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