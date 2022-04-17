import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from channels.generic.websocket import AsyncWebsocketConsumer

from .models import Room, Message

class ChatConsumer(WebsocketConsumer):
    '''
    Here, we created a ChatConsumer, which inherits from WebsocketConsumer. 
    WebsocketConsumer provides three methods, connect(), disconnect(), and receive():
    '''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.room_name = None
        self.room_group_name = None
        self.room = None
        self.user = None

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        self.room = Room.objects.get(name=self.room_name)
        self.user = self.scope['user']

        # connection has to be accepted
        self.accept()

        self.send(text_data=json.dumps({
            'type': 'connection_established',
            'message': 'You are now connected',
        }))

        # Create or join to group(room) and assign channel_name
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
    
    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name,
        )

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        if not self.user.is_authenticated:  # new
            return  

        # send chat message event to the room
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message', #name of the method that should be invoked on consumers that receive the event.
                'user': self.user.username,
                'message': message,
            } 
            # this is what is being sent to the front end
            # we can use jsonwebtoken to encode the user and send it to the front end
        )
        Message.objects.create(user=self.user, room=self.room, content=message)
        print(self.user, self.room, message)

    def chat_message(self, event):
        self.send(text_data=json.dumps(event))
        print(json.dumps(event))
        print(self.scope['url_route']['kwargs'])
        print(self.room_name)
        print(self.room_group_name)
        print(self.channel_name)


## Same consumer in async form

class AsyncChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )
        
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name,
        )
    
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message', #name of the method that should be invoked on consumers that receive the event.
                'message': message,
            }
        )
    
    async def chat_message(self, event):
        message = event['message']

        await self.send(text_data=json.dumps({'message':message}))
