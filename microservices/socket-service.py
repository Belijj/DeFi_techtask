import asyncio
import json
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

async def rabbitmq_listener(websocket: WebSocket):
    connection = await aio_pika.connect_robust("amqp://guest:guest@localhost/")
    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue("data_queue", durable=False)

        async for message in queue:
            async with message.process():
                print(f"Received message: {message.body}")
                await websocket.send_text(message.body.decode())

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        await rabbitmq_listener(websocket)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await websocket.close()
