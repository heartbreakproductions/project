import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Message

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = "global_chat"
        self.room_group_name = f'chat_{self.room_name}'
        self.user = self.scope['user']

        if not self.user.is_authenticated:
            await self.close()
            return

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
        data = json.loads(text_data)
        message_content = data.get('message', '').strip()
        delete_message_id = data.get('delete_message_id', None)

        # Handle message deletion request
        if delete_message_id:
            message_owner = await self.get_message_owner(delete_message_id)
            if message_owner == self.user:
                await self.delete_message(delete_message_id)
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'chat_message',
                        'action': 'delete',
                        'message_id': delete_message_id,
                    }
                )
            return

        # Handle new message creation
        if message_content:
            new_message = await self.create_message(user=self.user, content=message_content)
            profile_image_url = await self.get_profile_image_url(self.user)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'action': 'new_message',
                    'message_id': new_message.id,
                    'message': new_message.content,
                    'user': self.user.username,
                    'profile_image_url': profile_image_url,
                    'can_delete': new_message.user == self.user,
                    # 'owner_id': new_message.user.id,
                }
            )

    async def chat_message(self, event):
        """
        Broadcast messages or deletions to WebSocket clients.
        """
        await self.send(text_data=json.dumps(event))

    @database_sync_to_async
    def create_message(self, user, content):
        return Message.objects.create(user=user, content=content)

    @database_sync_to_async
    def delete_message(self, message_id):
        try:
            message = Message.objects.get(id=message_id)
            message.delete()
        except Message.DoesNotExist:
            pass

    @database_sync_to_async
    def get_message_owner(self, message_id):
        try:
            message = Message.objects.get(id=message_id)
            return message.user
        except Message.DoesNotExist:
            return None

    @database_sync_to_async
    def get_profile_image_url(self, user):
        if hasattr(user, 'userprofile') and user.userprofile.profile_image:
            return user.userprofile.profile_image.url
        return '/static/images/user-fallback.png'
