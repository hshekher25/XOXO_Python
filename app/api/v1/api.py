from fastapi import APIRouter
from app.api.v1.endpoints import auth, profiles, swipe, chat, chat_rooms, nearby, websocket

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(profiles.router, prefix="/profiles", tags=["profiles"])
api_router.include_router(swipe.router, prefix="/swipe", tags=["swipe"])
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])
api_router.include_router(chat_rooms.router, prefix="/chat-rooms", tags=["chat-rooms"])
api_router.include_router(nearby.router, prefix="/nearby", tags=["nearby"])
api_router.include_router(websocket.router, prefix="/ws", tags=["websocket"])

