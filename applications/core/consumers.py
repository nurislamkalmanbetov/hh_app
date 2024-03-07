import json
import redis
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

class InterviewsConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        from applications.staff.models import Notification
        await self.channel_layer.group_add("notification", self.channel_name)
        await self.accept()
        unread_count = await sync_to_async(Notification.objects.filter(read=False).count)()
        self.unread_count = unread_count
    
        async for n in Notification.objects.all():
            await self.send(text_data=json.dumps(
                {
                    'message': n.data, 
                    'id': n.id, 
                    'read': n.read,
                    'notification_date': n.created_at.strftime('%Y-%m-%d %H:%M'),
                    'unread_count': unread_count
                    }

                    ))
        


    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        from applications.staff.models import Notification
        data = json.loads(text_data)
        notification_id = data['id']
        print(notification_id)
        notification = await sync_to_async(Notification.objects.get)(id=notification_id)
        notification.read = True
        await sync_to_async(notification.save)()
        self.unread_count -= 1
        await self.send(text_data=json.dumps({
            'id': notification_id,
            'message': notification.data, 
            'read': notification.read,
            'notification_date': notification.created_at.strftime('%Y-%m-%d %H:%M'),
            'unread_count': self.unread_count
            }))

            
    async def interviews_message(self, event):
        
        self.unread_count += 1

        await self.send(text_data=json.dumps({
            'id': event['id'],
            'message': event['message'], 
            'read': event['read'],
            'notification_date': event['notification_date'],
            'unread_count': self.unread_count
            }))


    
        