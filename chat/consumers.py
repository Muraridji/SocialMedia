import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_id = self.scope["url_route"]["kwargs"]["chat_id"]
        self.room_group_name = f"chat_{self.chat_id}"

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
        import json
        from django.contrib.auth import get_user_model

        data = json.loads(text_data)
        message = data["message"]
        user = self.scope["user"]

        chat = await self.get_chat(self.chat_id)
        msg = await self.create_message(chat, user, message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": msg.content,
                "username": user.username,
                "created_at": msg.created_at.strftime("%d.%m.%Y %H:%M"),
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "message": event["message"],
            "username": event["username"],
            "created_at": event["created_at"],
        }))

    @database_sync_to_async
    def get_chat(self, chat_id):
        from chat.models import Chat
        return Chat.objects.get(id=chat_id)

    @database_sync_to_async
    def create_message(self, chat, user, message):
        from chat.models import Message
        return Message.objects.create(chat=chat, author=user, content=message)
