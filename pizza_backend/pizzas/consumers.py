from channels.generic.websocket import AsyncJsonWebsocketConsumer

class PizzaConsumer(AsyncJsonWebsocketConsumer):
    groups = ['test']

    async def connect(self):
        await self.accept()

    async def receive_json(self, content, **kwargs):
        message_type = content.get('type')
        if message_type == 'echo.message':
            await self.send_json({
                'type': message_type,
                'data': content.get('data'),
            })

    async def echo_message(self, message):
        await self.send_json({
            'type': message.get('type'),
            'data': message.get('data'),
        })

    async def disconnect(self, code):
        await super().disconnect(code)
