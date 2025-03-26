import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from .models import Message
from asgiref.sync import sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Add user to the group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Remove user from the group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    async def chat_message(self, event):
        message = event["message"]
        sender = event["sender"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            "message": message,
            "sender": sender
        }))

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data["message"]
        sender = self.scope["user"]  # Logged-in user
        
        print(f"📥 Received message: {message} from {sender.username}")

        # Extract receiver's username from room_name
        try:
            # Extract usernames correctly
            usernames = self.room_name.split("_")[1:]  # Removes "chat_" prefix
            print(f"🔍 Debug: usernames extracted = {usernames}")  # Debugging

            # Identify receiver (the one who is NOT the sender)
            other_username = [u for u in usernames if u != sender.username][0]  
            print(f"✅ Extracted receiver username: {other_username}")

            # Retrieve receiver user object
            receiver = await sync_to_async(User.objects.get)(username=other_username)
            print(f"👥 Chat between {sender.username} and {receiver.username}")

            # Save message to database
            await self.save_message(sender, receiver, message)
            print("✅ Message saved successfully")

            # Broadcast message
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "message": message,
                    "sender": sender.username
                }
            )
        except Exception as e:
            print(f"❌ Error: {e}")  # Debugging error



    @sync_to_async
    def save_message(self, sender, receiver, message):
        try:
            msg = Message.objects.create(sender=sender, receiver=receiver, message=message)
            print(f"📝 Saved message: {msg}")
        except Exception as e:
            print(f"❌ Error saving message: {e}")

