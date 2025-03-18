from typing import List, Optional
from pydantic import BaseModel


# User Service Models
class UserProfile(BaseModel):
    student_id: str  # id
    uni: str  # sis_user_id
    first_name: str
    last_name: str
    pronouns: str
    email: Optional[str] = None
    courses: Optional[List[str]] = None  # List of course names or IDs
    access_token: str

    class Config:
        schema_extra = {
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


# Chat Service Models
class Conversation(BaseModel):
    conversation_id: Optional[int] = None
    user_id: str
    participants: List[str]
    last_message: Optional[str] = None
    last_updated: Optional[str] = None  # ISO 8601 format

    class Config:
        schema_extra = {
            "example": {
                "conversation_id": 1,
                "user_id": "sh1234",
                "participants": ["sh1234", "js5678"],
                "last_message": "Looking forward to our study group!",
                "last_updated": "2024-04-06T12:30:00Z",
            }
        }


class CreateConversationRequest(BaseModel):
    participants: List[str]

    class Config:
        schema_extra = {
            "example": {
                "participants": ["sh1234", "js5678"]
            }
        }


# Study Group Models
class StudyGroup(BaseModel):
    group_id: int
    group_name: str
    course_id: int
    members: List[str]
    created_at: str  # ISO 8601 format

    class Config:
        schema_extra = {
            "example": {
                "group_id": 204283,
                "group_name": "COMS4153 Project",
                "course_id": 3456,
                "members": ["sh1234", "js5678", "ak8910"],
                "created_at": "2024-04-05T00:58:50Z",
            }
        }


class AddMemberRequest(BaseModel):
    group_id: int
    user_id: str

    class Config:
        schema_extra = {
            "example": {
                "group_id": 204283,
                "user_id": "ak8910"
            }
        }


# Course Enrollment Models
class CourseEnrollment(BaseModel):
    course_id: int
    course_name: str
    enrolled_students: List[str]

    class Config:
        schema_extra = {
            "example": {
                "course_id": 3456,
                "course_name": "Distributed Systems",
                "enrolled_students": ["sh1234", "js5678"],
            }
        }


class EnrollStudentRequest(BaseModel):
    course_id: int
    user_id: str

    class Config:
        schema_extra = {
            "example": {
                "course_id": 3456,
                "user_id": "sh1234"
            }
        }


# Composite Service Models
class CompositeResponse(BaseModel):
    user_profile: Optional[UserProfile] = None
    study_groups: Optional[List[StudyGroup]] = None
    conversations: Optional[List[Conversation]] = None
    enrolled_courses: Optional[List[CourseEnrollment]] = None

    class Config:
        schema_extra = {
            "example": {
                "user_profile": {
                    "user_id": "sh1234",
                    "name": "Sumya Hoque",
                    "email": "sumya@example.com",
                    "university": "Columbia University",
                    "major": "Computer Science",
                    "created_at": "2024-04-05T00:58:50Z",
                },
                "study_groups": [
                    {
                        "group_id": 204283,
                        "group_name": "COMS4153 Project",
                        "course_id": 3456,
                        "members": ["sh1234", "js5678", "ak8910"],
                        "created_at": "2024-04-05T00:58:50Z",
                    }
                ],
                "conversations": [
                    {
                        "conversation_id": 1,
                        "user_id": "sh1234",
                        "participants": ["sh1234", "js5678"],
                        "last_message": "Looking forward to our study group!",
                        "last_updated": "2024-04-06T12:30:00Z",
                    }
                ],
                "enrolled_courses": [
                    {
                        "course_id": 3456,
                        "course_name": "Distributed Systems",
                        "enrolled_students": ["sh1234", "js5678"],
                    }
                ],
            }
        }



