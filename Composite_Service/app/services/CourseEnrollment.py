from app.services.service_factory import ServiceFactory
from fastapi import HTTPException
class CourseEnrolment:
    def __init__(self) -> None:
        service = ServiceFactory()
        self.compo_resource = service.get_service("CompositeResource")
 
    def get_all_students(self, course_id:str, token:str):
            data, status_code = self.compo_resource.get_all_students_per_course(course_id, token)
            if status_code == 200:
                  return data
            else:
                  raise HTTPException(status_code=status_code, details=data)

        
    def get_all_course(self, user_id: str, token:str):
  
            print("statrted the course info")
            data, status_code = self.compo_resource.get_course(user_id, token)
            if status_code == 200:
                  return data
            else:
                  raise HTTPException(status_code=status_code, details=data)
    