from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class Message(BaseModel):
    sender: str  # "scammer" or "user"
    text: str
    timestamp: datetime


class Metadata(BaseModel):
    channel: Optional[str] = None
    language: Optional[str] = None
    locale: Optional[str] = None


class IncomingRequest(BaseModel):
    sessionId: str
    message: Message
    conversationHistory: Optional[List[Message]] = []
    metadata: Optional[Metadata] = None
