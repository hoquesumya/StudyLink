from canvasapi import Canvas
from fastapi import HTTPException
# from app.resources.course_resource import CourseResource
# import os

"""
    File in charge of connecting with the courseworks api to get desired results. Currently Hardcoded with Jeannie's 
    courseworks token, we'll have to figure out a way to get each user's token when they use this app....
"""
class CourseWorksAPI:
    def __init__(self, token):
        self.token = token
        self.base_url = "https://courseworks2.columbia.edu"
        self.canvas = Canvas(self.base_url, self.token)

    def get_student_courses(self, student_id: str):
        """
        Get the list of courses for a specific student.
        """
        try:
            user = self.canvas.get_user(student_id, "sis_user_id")
            courses = user.get_courses()
            courses_list = []
            # Iterate over the PaginatedList and add each course to the list
            for course in courses:
                if "2024_3" in course.course_code:
                    courses_list.append(course.course_code)
            return courses_list
        except Exception as e:
            raise HTTPException(status_code=404, detail=f"Error fetching courses for student {student_id}: {str(e)}")

    def get_course_students_by_code(self, course_code: str):
        """
        Get the list of students (+ their id) enrolled in a course by course_code.
        """
        try:
            courses = self.canvas.get_courses()
            for course in courses:
                filtered_course_code = str(course.course_code.split(" ")[0])
                if filtered_course_code == str(course_code):
                    enrollments = course.get_enrollments()
                    students = []
                    for enrollment in enrollments:
                        if enrollment.type == "StudentEnrollment":
                            # Add the student information to the students list
                            students.append({
                                "name": enrollment.user['name'],
                                "id": enrollment.user.get('id', 'N/A')
                            })
                    return students
            if not courses:
                raise HTTPException(status_code=404, detail=f"No course found with course_code {course_code}")
        except Exception as e:
            raise HTTPException(status_code=404, detail=f"Error fetching students for course {course_code}: {str(e)}")
