import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import ChatMessage

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_name = "clinic_chat"
        self.room_group_name = f"chat_{self.room_name}"

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

    async def receive(self, text_data):
        print("Raw : ",text_data)
        data = json.loads(text_data)
        message = data.get("message")
        print("MESSAGE:", message)
        if not message:
            return

        user = self.scope["user"]
        print("USER:", user, "AUTH:", user.is_authenticated)
        # FK value saved in DB
        chat_user = user if user.is_authenticated else None

        # String sent to frontend
        username = user.username if user.is_authenticated else "Guest"

        # Save message to DB
        await sync_to_async(ChatMessage.objects.create)(
            username=chat_user,
            message=message
        )

        # Send plain JSON to all clients
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "username": username,   # MUST be a string
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "message": event["message"],
            "username": event["username"],  # string only
        }))
