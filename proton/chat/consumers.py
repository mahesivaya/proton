# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from django.contrib.auth import get_user_model
from .models import Room, Message, DirectMessage
from django.contrib.auth import get_user_model
from .models import Room, Message, DirectMessage

User = get_user_model()
from .models import ChatMessage

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_name = "clinic_chat"
        self.room_group_name = f"chat_{self.room_name}"

    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"
        self.user = self.scope["user"]

        if self.user.is_anonymous:
            await self.close()
            return

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

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
                "username": self.user.username,
                "message": message,
            },
        )

    async def chat_message(self, event):
        await self.send(
            text_data=json.dumps(
                {
                    "username": event["username"],
                    "message": event["message"],
                }
            )
        )

    @sync_to_async
    def save_message(self, room_name, user, message):
        room, _ = Room.objects.get_or_create(name=room_name)
        Message.objects.create(room=room, user=user, content=message)


class DMConsumer(AsyncWebsocketConsumer):
    """
    Direct messages: ws://.../ws/dm/<username>/
    """

    async def connect(self):
        self.user = self.scope["user"]
        self.other_username = self.scope["url_route"]["kwargs"]["username"]

        if self.user.is_anonymous:
            await self.close()
            return

        # derive deterministic DM room key for both directions
        self.room_group_name = await self.get_dm_group_name(self.user.username, self.other_username)

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        message = data.get("message", "").strip()
        if not message:
            return

        other_user = await self.get_user_by_username(self.other_username)
        if other_user is None:
            return

        # save DM
        await self.save_dm(self.user, other_user, message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "dm_message",
                "username": self.user.username,
                "message": message,
            },
        )

    async def dm_message(self, event):
        await self.send(
            text_data=json.dumps(
                {
                    "username": event["username"],
                    "message": event["message"],
                }
            )
        )

    # ---------- helpers ----------
    @sync_to_async
    def get_dm_group_name(self, u1, u2):
        # stable key: dm_userA_userB (sorted)
        user_names = sorted([u1, u2])
        return f"dm_{user_names[0]}_{user_names[1]}"

    @sync_to_async
    def get_user_by_username(self, username):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            return None

    @sync_to_async
    def save_dm(self, sender, receiver, content):
        DirectMessage.objects.create(sender=sender, receiver=receiver, content=content)
