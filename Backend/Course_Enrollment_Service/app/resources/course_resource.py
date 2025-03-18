"""
from typing import Any
from framework.resources.base_resource import BaseResource
from models.course import CourseSection
from services.service_factory import ServiceFactory


class CourseResource(BaseResource):
    def __init__(self, config):
        super().__init__(config)
        self.data_service = ServiceFactory.get_service("CourseResourceDataService")
        self.database = "CloudComputing_CE"

    def create_or_update_student(self, profile: dict):
        self.data_service.insert_or_update(
            table="students",
            data=profile,
            key_field="student_id"
        )

    def create_or_update_course(self, course: dict):
        self.data_service.insert_or_update(
            table="courses",
            data=course,
            key_field="course_code"
        )

    def get_courses(self, student_id: str):
        return self.data_service.get_courses_for_student(student_id)

    def get_students(self, course_code: str):
        return self.data_service.get_students_in_course(course_code)
        """
