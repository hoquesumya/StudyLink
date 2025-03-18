from typing import List, Optional
from pydantic import BaseModel

"""
    Currently not in use because we are just focusing on the API aspect of feeding the user their dashboard + the 
    students in their class, not the database.
"""


class Student(BaseModel):
    student_id: str  
    first_name: str
    last_name: str
    email: Optional[str] = None  
    university_id: str  

    class Config:
        json_schema_extra = {
            "example": {
                "student_id": "abc1234",  
                "first_name": "John",
                "last_name": "Doe",
                "email": "john.doe@example.com",
                "university_id": "123456"
            }
        }


class StudentsInCourse(BaseModel):
    course_id: int
    course_name: str
    students: List[Student] 

    class Config:
        json_schema_extra = {
            "example": {
                "course_id": 204283,
                "course_name": "Cloud Computing",
                "students": [
                    {
                        "student_id": "abc1234",  # Changed to a string
                        "first_name": "John",
                        "last_name": "Doe",
                        "email": "john.doe@example.com",
                        "university_id": "123456"
                    },
                    {
                        "student_id": "xyz9876",  # Another example of string student ID
                        "first_name": "Jane",
                        "last_name": "Smith",
                        "email": "jane.smith@example.com",
                        "university_id": "654321"
                    }
                ]
            }
        }
