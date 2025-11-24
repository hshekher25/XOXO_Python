from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.websocket.chat_websocket import manager
import json

router = APIRouter()


@router.websocket("/chat-rooms/{room_id}")
async def chat_room_websocket(websocket: WebSocket, room_id: str):
    await manager.connect(websocket, room_id)
    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            # Broadcast to all connections in the room
            await manager.broadcast(json.dumps(message_data), room_id)
    except WebSocketDisconnect:
        manager.disconnect(websocket, room_id)


@router.websocket("/chat/{match_id}")
async def match_chat_websocket(websocket: WebSocket, match_id: str):
    await manager.connect(websocket, match_id)
    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            await manager.broadcast(json.dumps(message_data), match_id)
    except WebSocketDisconnect:
        manager.disconnect(websocket, match_id)


@router.websocket("/nearby-chat/{chat_id}")
async def nearby_chat_websocket(websocket: WebSocket, chat_id: str):
    await manager.connect(websocket, chat_id)
    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            await manager.broadcast(json.dumps(message_data), chat_id)
    except WebSocketDisconnect:
        manager.disconnect(websocket, chat_id)

