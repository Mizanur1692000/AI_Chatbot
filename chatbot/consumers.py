import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.cache import cache

def get_ai_response(message):
    # In a real application, this would make a call to an AI service.
    # For now, we'll just echo the message.
    # We'll add a small delay to simulate a network call.
    import time
    time.sleep(2)
    return f"AI response to: {message}"

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Check cache first
        cached_response = cache.get(message)
        if cached_response:
            await self.send(text_data=json.dumps({
                'message': cached_response
            }))
            return

        try:
            # Call AI service asynchronously
            ai_response = await asyncio.to_thread(get_ai_response, message)
            cache.set(message, ai_response, timeout=300) # Cache for 5 minutes
        except Exception as e:
            # Handle errors from the AI service
            ai_response = "Sorry, I'm having trouble connecting to the AI service."
            # Log the error
            print(f"Error calling AI service: {e}")

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': ai_response
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
