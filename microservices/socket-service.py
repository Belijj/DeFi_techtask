import asyncio
from typing import List
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import aio_pika

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

connected_websockets: List[WebSocket] = []

async def connect_to_rabbitmq():
    while True:
        try:
            connection = await aio_pika.connect_robust("amqp://guest:guest@localhost/")
            print("Connected to RabbitMQ")
            return connection
        except aio_pika.exceptions.AMQPConnectionError as e:
            print(f"Conn fail: {e}. Retry in 5 sec")
            await asyncio.sleep(5)

async def broadcast_message(message_body: str):
    for websocket in connected_websockets:
        try:
            await websocket.send_text(message_body)
        except Exception as e:
            print(f"Error sending msg to websocket: {e}")

async def rabbitmq_listener():
    connection = await connect_to_rabbitmq()
    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue('data_queue', durable=False)

        async for message in queue:
            async with message.process():
                message_body = message.body.decode()
                print(f"Received msg from rabbit: {message_body}")
                await broadcast_message(message_body)

async def handle_websocket(websocket: WebSocket):
    connected_websockets.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            print(f"Received msg from ws: {data}")

            connection = await connect_to_rabbitmq()
            async with connection:
                channel = await connection.channel()
                await channel.default_exchange.publish(
                    aio_pika.Message(body=data.encode()),
                    routing_key='data_queue',
                )
                print(f"Msg sent to rabbit: {data}")
    except Exception as e:
        print(f"Err: {e}")
    finally:
        connected_websockets.remove(websocket)
        await websocket.close()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    websocket_task = asyncio.create_task(handle_websocket(websocket))
    try:
        await websocket_task
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        websocket_task.cancel()
        await websocket.close()

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(rabbitmq_listener())
