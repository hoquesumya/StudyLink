class UserProfileResource:
    def __init__(self):
        from app.services.service_factory import ServiceFactory
        self.data_service = ServiceFactory.get_service('UserProfileResourceDataService')

    def create_or_update_profile(self, profile: dict):
        """Create or update a user profile with new fields."""
        self.data_service.insert_or_update(
            table="user_profiles",
            data=profile,
            key_field="user_id"
        )

    def delete_profile(self, user_id: str):
        """Delete a user profile from the database."""
        self.data_service.delete(
            table="user_profiles",
            key_field="user_id",
            key_value=user_id
        )

    def get_profile(self, user_id: str):
        """Retrieve a user profile from the database."""
        return self.data_service.fetch_one(
            table="user_profiles",
            key_field="user_id",
            key_value=user_id
        )

    def get_users(self, skip: int, limit: int, filters: dict):
        """Retrieve filtered users."""
        users = self.data_service.get_users(
            skip=skip,
            limit=limit,
            filters=filters
        )
        # Ensure users is always a list
        return users if users else []
