# models/user_model.py

from __future__ import annotations
from typing import Optional, List
from pydantic import BaseModel


class User(BaseModel):
    student_id: str  # id
    uni: str  # sis_user_id
    first_name: str
    last_name: str
    pronouns: str
    email: Optional[str] = None
    courses: Optional[List[str]] = None  # List of course names or IDs
    access_token: str

    class Config:
        json_schema_extra = {
            "example": {
                "student_id": "123456",
                "uni": "abc1234",
                "first_name": "John",
                "last_name": "Doe",
                "pronouns": "he/him",
                "email": "john.doe@example.com",
                "courses": ["Cloud Computing", "Data Science"],
                "canvas_token": "your_canvas_access_token"

            }
        }
