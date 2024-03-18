from rest_framework import serializers

from .models import Chat, Message


class ChatSerializer(serializers.ModelSerializer):


    class Meta:
        model = Chat
        fields = ['id', 'participants', 'created_at',]

 
