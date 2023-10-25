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
        print(222)
        await self.send({
            "type": "websocket.send",
            "text": "Hello from Django socket"
        })

    async def websocket_disconnect(self, event):
        print(111)
        pass

    async def disconnect(self, close_code):
        print(close_code)
        await self.channel_layer.group_discard(
            self.channel_name
        )
        raise StopConsumer()

    async def send_update(self, event):
        print(123123)
        await self.send({
            "type": "websocket.send",
            "text": event["text"],
        })


# class YourConsumer(AsyncConsumer):
#
#     async def websocket_connect(self, event):
#         await self.send({"type": "websocket.accept"})
#         await self.channel_layer.group_add("domains_group", self.channel_name)
#
#     async def websocket_receive(self, event):
#         print(123123123)
#         text_data = event.get('text')
#
#         if text_data:
#             # Обработка входящего сообщения
#             print("Received message:", text_data)
#
#             # Отправка ответа клиенту (пример)
#             await self.send({
#                 'type': 'websocket.send',
#                 'text': 'Response from server: {}'.format(text_data)
#             })
#
#     async def websocket_disconnect(self, event):
#         pass