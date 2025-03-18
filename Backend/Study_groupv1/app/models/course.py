from __future__ import annotations

# from datetime import date, timedelta
from typing import Optional, List

from pydantic import BaseModel


class CourseSection(BaseModel):
    group_id: Optional[int] = None
    group_name: Optional[str] = None
    created_by: Optional[str] = None
    created_at: Optional[str] = None
    is_recurring: Optional[bool] = None
    meeting_date: Optional[str] = None
    recurrence_frequency: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    recurrence_end_date: Optional[str] = None
    course_id: Optional[str] = None
    members: Optional[List[str]] = None

    class Config:
        json_schema_extra = {
            "example": {
                "group_id": 1,
                "group_name": "IEORE4150 PROJECT",
                "created_by": "er2788",
                "created_at": "2024-04-05T00:58:50Z",
                "is_recurring": False,
                "meeting_date": "2024-11-05",
                "recurrence_frequency": None,
                "start_time": "09:00:00",
                "end_time": "10:00:00",
                "recurrence_end_date": None,
                "course_id": 'IEORE4150_001_2024_3 - INTRO-PROBABILITY & STATISTICS',
                "members": ["er2788", "sh1234"]
            }
        }
