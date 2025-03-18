from canvasapi import Canvas
from app.services.service_factory import ServiceFactory
from fastapi import HTTPException
import json  # To handle courses as JSON
import hashlib


class UserProfileService:
    def __init__(self):
        self.resource = ServiceFactory.get_service('UserProfileResource')

    def create_or_update_profile(self, user_id: str, token: str):
        try:
            # Initialize the Canvas API with the provided token
            canvas = Canvas("https://courseworks2.columbia.edu", token)

            # Fetch user details from Canvas
            user = canvas.get_user(user_id, "sis_user_id")
            user_profile = user.get_profile()  # Get detailed profile info

            # Extract the courses the user is enrolled in
            courses = user.get_courses()
            course_names = [course.name for course in courses]

            # Prepare the profile data
            profile_data = {
                "user_id": user_id,
                "first_name": user_profile.get("short_name", "").split()[0],
                "last_name": user_profile.get("short_name", "").split()[-1],
                "email": user_profile.get("primary_email", ""),
                "pronouns": user_profile.get("pronouns", ""),
                "short_name": user_profile.get("short_name", ""),
                "courses": json.dumps(course_names),  # Store courses as JSON
                "canvas_token": token
            }

            # Save the profile to the database
            self.resource.create_or_update_profile(profile_data)
            return profile_data
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error fetching user data: {str(e)}")

    def delete_user_profile(self, user_id: str):
        """Delete a user profile from the database."""
        self.resource.delete_profile(user_id)
        return {"message": f"User profile {user_id} deleted successfully"}

    def get_user_profile(self, user_id: str):
        """Retrieve a user profile from the database."""
        profile = self.resource.get_profile(user_id)
        if not profile:
            raise HTTPException(status_code=404, detail=f"User {user_id} not found")

        # Parse courses JSON back into a list
        profile["courses"] = json.loads(profile["courses"])
        return profile

    def get_users(self, skip: int = 0, limit: int = 10, name: str = None, course: str = None):
        """Retrieve a list of users with optional filters."""
        try:
            # Prepare query parameters
            filters = {}
            if name:
                filters["name"] = name
            if course:
                filters["course"] = course

            # Call the data service to fetch users with pagination
            return self.resource.get_users(skip=skip, limit=limit, filters=filters)
        except Exception as e:
            print(f"Error in get_users: {e}")
            raise HTTPException(status_code=500, detail="Error fetching users.")
