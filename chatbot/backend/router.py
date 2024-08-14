# routers/websocket_router.py

from fastapi import APIRouter, WebSocket
from models import ConnectionManager
import asyncio

router = APIRouter()
manager = ConnectionManager()

@router.on_event("startup")
async def startup_event():
    await manager.connect_to_rabbitmq()
    await manager.db.create_table()
    asyncio.create_task(manager.rabbitmq_listener())

@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.handle_websocket(websocket, client_id)
