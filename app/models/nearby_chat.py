from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Integer
from sqlalchemy.sql import func
import uuid
from app.core.database import Base


class NearbyChat(Base):
    __tablename__ = "nearby_chats"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    expires_at = Column(DateTime, nullable=False)


class NearbyChatMessage(Base):
    __tablename__ = "nearby_chat_messages"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    chat_id = Column(String(36), ForeignKey("nearby_chats.id"), nullable=False)
    sender_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    sender_name = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

