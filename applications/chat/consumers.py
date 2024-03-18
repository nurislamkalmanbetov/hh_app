import jwt
from django.conf import settings
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from asgiref.sync import sync_to_async


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        from applications.accounts.models import User
        self.token = self.scope['url_route']['kwargs'].get('token')
        payload = jwt.decode(self.token, settings.SECRET_KEY, algorithms=['HS256'])
        self.user_id = payload['user_id']
        self.user = await sync_to_async(User.objects.get)(id=self.user_id)
        # print(self.user.id)

        self.chat_group_name = f'chat_{self.user_id}'


        await self.channel_layer.group_add(
            self.chat_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        pass


    async def chat_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))


 
    
    
        
    