from channels.consumer import AsyncConsumer
from channels.exceptions import StopConsumer
from channels.generic.websocket import AsyncWebsocketConsumer

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
        await self.send({
            "type": "websocket.send",
            "text": "Hello from Django socket"
        })

    async def websocket_disconnect(self, event):
        pass

    async def send_update(self, event):
        await self.send({
            "type": "websocket.send",
            "text": event["text"],
        })