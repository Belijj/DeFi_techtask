# models.py

import asyncio
from typing import Dict, List
from fastapi import WebSocket, WebSocketDisconnect
import aio_pika
from dbase import DataBase
import logging

logger = logging.getLogger(__name__)

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, WebSocket] = {}
        self.rabbitmq_connection = None
        self.rabbitmq_channel = None
        self.db = DataBase()
        self.max_retries = 5

    async def connect(self, websocket: WebSocket, client_id: int):
        await websocket.accept()
        self.active_connections[client_id] = websocket
        logger.info(f"WebSocket connected: {client_id}")

    async def disconnect(self, client_id: int):
        websocket = self.active_connections.pop(client_id, None)
        if websocket:
            await websocket.close()
            logger.info(f"WebSocket disconnected: {client_id}")

    async def send_personal_message(self, message: str, websocket: WebSocket):
        try:
            await websocket.send_text(message)
        except RuntimeError:
            await self.disconnect(next((cid for cid, ws in self.active_connections.items() if ws == websocket), None))

    async def broadcast(self, message: str):
        tasks = [self._send_message(ws, message) for ws in self.active_connections.values()]
        await asyncio.gather(*tasks, return_exceptions=True)

    async def _send_message(self, websocket: WebSocket, message: str):
        try:
            await websocket.send_text(message)
        except RuntimeError:
            await self.disconnect(next((cid for cid, ws in self.active_connections.items() if ws == websocket), None))

    async def connect_to_rabbitmq(self):
        retry_count = 0
        while retry_count < self.max_retries:
            try:
                self.rabbitmq_connection = await aio_pika.connect_robust("amqp://guest:guest@localhost/")
                self.rabbitmq_channel = await self.rabbitmq_connection.channel()
                await self.rabbitmq_channel.set_qos(prefetch_count=100)
                logger.info("Connected to RabbitMQ")
                return
            except aio_pika.exceptions.AMQPConnectionError as e:
                retry_count += 1
                logger.error(f"Conn failed: {e}. Retrying in 5 sec({retry_count}/{self.max_retries})")
                await asyncio.sleep(5)
        logger.error("Failed to connect to rabbit")

    async def rabbitmq_listener(self):
        while True:
            if not self.rabbitmq_channel or self.rabbitmq_connection.is_closed:
                await self.connect_to_rabbitmq()

            try:
                queue = await self.rabbitmq_channel.declare_queue('data_queue', durable=True)

                async for message in queue:
                    async with message.process():
                        try:
                            message_body = message.body.decode()
                            logger.info(f"Msg from Rabbit: {message_body}")
                            await self.handle_message(message_body)
                        except Exception as e:
                            logger.error(f"Failed to process msg: {e}")
                            await message.nack(requeue=True)
            except Exception as e:
                logger.error(f"Error in Rabbit: {e}")
                await asyncio.sleep(5)

    async def handle_message(self, message_body: str):
        await self.db.add_message(message_body)
        asyncio.create_task(self.broadcast(message_body))
        logger.info(f"Procees succesfully: {message_body}")

    async def publish_message(self, message: str):
        if not self.rabbitmq_channel:
            await self.connect_to_rabbitmq()

        try:
            await self.rabbitmq_channel.default_exchange.publish(
                aio_pika.Message(body=message.encode()),
                routing_key='data_queue',
            )
            logger.info(f"Message sent to Rabbit: {message}")
        except Exception as e:
            logger.error(f"Error sending to Rabbit: {e}")

    async def handle_websocket(self, websocket: WebSocket, client_id: int):
        await self.connect(websocket, client_id)

        last_messages: List[tuple] = await self.db.retrieve_messages()
        for msg in last_messages:
            await self.send_personal_message(msg[1], websocket)
        try:
            async for data in websocket.iter_text():
                logger.info(f"Received msg from WS: {data}")

                await self.db.add_message(data)

                broadcast_message = f"Client #{client_id} says: {data}"
                await self.publish_message(broadcast_message)

        except WebSocketDisconnect:
            await self.disconnect(client_id)
        except Exception as e:
            logger.error(f"Error handling WebSocket: {e}")
            await self.disconnect(client_id)
