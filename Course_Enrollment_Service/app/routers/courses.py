from fastapi import APIRouter, HTTPException, Header, Request, Response
from services.courseworks_api import CourseWorksAPI
import uuid
"""
    Router in charge of connecting with `courseworks_api.py` to get the students enrolled in a class
"""
router = APIRouter()


# Fetch students enrolled in a course by course code (e.g., COMSW4153)
@router.get("/course/{course_code}/students", tags=["courses"])
async def get_course_students(request: Request, response: Response, course_code: str, token: str = Header(...)):
    correlation_id = request.headers.get("X-Correlation-ID", str(uuid.uuid4()))
    response.headers["X-Correlation-ID"] = correlation_id
    print(f"Correlation ID: {correlation_id} - Fetching students for course: {course_code}")
    api = CourseWorksAPI(token)
    students = api.get_course_students_by_code(course_code)
    return {"course_code": course_code, 
            "students": students, 
            "links":{
                "self": {
                    "href": f"/course/{course_code}/students"
                }
            }
           }
    
