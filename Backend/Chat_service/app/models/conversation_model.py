# models/conversation_model.py

from __future__ import annotations
from typing import Optional, List, Optional
from pydantic import BaseModel

class Message(BaseModel):
    text: str
    sender: str
    timestamp: str

class Conversation(BaseModel):
    id: Optional[int] = None  # Optional for cases when creating a new conversation
    name: str
    participants: List[str]  # List of participant names
    messages: Optional[List[Message]] = None  # List of messages
    is_group: bool = False  # Indicates if it's a group conversation

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "John Doe",
                "participants": ["John Doe", "CurrentUser"],
                "messages": [
                    {"text": "Hey, how are you?", "sender": "CurrentUser", "timestamp": "10:00 AM"},
                    {"text": "I am doing well! How about you?", "sender": "John Doe", "timestamp": "10:05 AM"}
                ],
                "is_group": False
            }
        }