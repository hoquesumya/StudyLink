from fastapi import APIRouter, HTTPException, Header, Request, Response
from services.courseworks_api import CourseWorksAPI
import uuid
"""
    Router in charge of connecting with `courseworks_api.py` to get the courses a student is enrolled in.
"""
router = APIRouter()


# Fetch courses for a student by student_id (uni)
@router.get("/users/{student_id}/courses", tags=["students"])
async def get_student_courses(request: Request, response: Response, student_id: str, token: str = Header(...)):
    correlation_id = request.headers.get("X-Correlation-ID", str(uuid.uuid4()))
    response.headers["X-Correlation-ID"] = correlation_id  
    print(f"Correlation ID: {correlation_id} - Fetching courses for student: {student_id}")
    api = CourseWorksAPI(token)
    try:
        courses = api.get_student_courses(student_id)
        return {
            "student_id": student_id, 
            "courses": courses, 
            "links": {
                "self": {
                        "href": f"/users/{student_id}/courses"
                }
            }
        }
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Error fetching courses for student {student_id}: {str(e)}")

