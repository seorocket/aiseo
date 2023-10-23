from channels.consumer import AsyncConsumer
import json

# class YourConsumer(AsyncConsumer):
#
#     async def websocket_connect(self, event):
#         await self.send({"type": "websocket.accept"})
#
#     async def websocket_receive(self, text_data):
#         await self.send({
#             "type": "websocket.send",
#             "text": "Hello from Django socket"
#         })
#
#     async def websocket_disconnect(self, event):
#         pass


class YourConsumer(AsyncConsumer):

    async def websocket_connect(self, event):
        await self.send({"type": "websocket.accept"})
        await self.channel_layer.group_add("domains_group", self.channel_name)

    async def websocket_receive(self, text_data):
        # Обработка входящих сообщений, если это необходимо
        pass

    async def websocket_disconnect(self, event):
        # Обработка отключения пользователя от WebSocket
        pass

    async def send_update(self, event):
        await self.send({
            "type": "websocket.send",
            "text": event["text"],
        })