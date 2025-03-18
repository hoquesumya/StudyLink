import json
from typing import Any, List, Dict
from framework.resources.base_resource import BaseResource
from app.models.course import CourseSection
from app.services.service_factory import ServiceFactory
import logging

logging.basicConfig(level=logging.INFO)

class CourseResource(BaseResource):
    def __init__(self, config):
        super().__init__(config)

        self.data_service = ServiceFactory.get_service("StudyResourceDataService")
        self.post_data_service = ServiceFactory.post_service("StudyResourceDataService")
        self.database = "p1_database"
        self.collection = "study_group"
        self.key_field="group_id"

    def get_all(self) -> List[CourseSection]:
        """
        Retrieve all study groups from the database.

        Returns:
            A list of CourseSection objects representing all study groups.
        """
        try:
            logging.info("Retrieving all study groups from the database")
            d_service = self.data_service
            results = d_service.get_all_objects(self.database, self.collection)

            # Convert raw data into CourseSection objects
            study_groups = []
            for result in results:
                if isinstance(result.get("members"), str):
                    try:
                        # Deserialize JSON-encoded string into a Python list
                        result["members"] = json.loads(result["members"])
                    except json.JSONDecodeError as e:
                        logging.error(f"Error decoding 'members': {e}")
                        result["members"] = []  # Default to an empty list if deserialization fails
                study_groups.append(CourseSection(**result))

            logging.info(f"Successfully retrieved {len(study_groups)} study groups")
            return study_groups
        except Exception as e:
            logging.error(f"Error retrieving all study groups: {e}")
            return []

    def get_by_id(self, group_id: int) -> CourseSection:
        """
        Retrieve a study group by its ID.

        Args:
            group_id: The ID of the study group to retrieve.

        Returns:
            A CourseSection object representing the study group.

        Raises:
            HTTPException: If the group is not found or if there's an error during retrieval.
        """
        try:
            # Use the data service to retrieve the group by ID
            logging.info(f"Retrieving study group with ID {group_id}")
            d_service = self.data_service
            result = d_service.get_data_object(
                self.database,
                self.collection,
                key_field="group_id",
                key_value=group_id
            )

            if not result:
                logging.warning(f"Study group with ID {group_id} not found.")
                raise ValueError(f"Study group with ID {group_id} not found.")

            # Deserialize 'members' field if it's a JSON string
            if isinstance(result.get("members"), str):
                try:
                    result["members"] = json.loads(result["members"])
                except json.JSONDecodeError as e:
                    logging.error(f"Error decoding 'members' field for group {group_id}: {e}")
                    result["members"] = []  # Default to empty list on failure

            # Convert result to a CourseSection object
            study_group = CourseSection(**result)
            logging.info(f"Successfully retrieved study group with ID {group_id}")
            return study_group

        except Exception as e:
            logging.error(f"Error retrieving study group with ID {group_id}: {e}")
            raise

    def get_by_key(self, key: str) -> CourseSection:
        """
       Retrieve a study group by a custom key.
       """
        try:
            logging.info(f"Retrieving study group with key {key}")
            d_service = self.data_service
            result = d_service.get_data_object(
                self.database,
                self.collection,
                key_field=self.key_field,
                key_value=key
            )
            if isinstance(result.get("members"), str):
                try:
                    result["members"] = json.loads(result["members"])
                except json.JSONDecodeError as e:
                    logging.error(f"Error decoding 'members' field for group with key {key}: {e}")
                    result["members"] = []
            logging.info(f"Successfully retrieved study group with key {key}")
            return CourseSection(**result)

        except Exception as e:
            logging.error(f"Error retrieving study group with key {key}: {e}")
            raise

    def post_group(
            self,
            created_by: str,
            created_at: str,
            course_id: str,
            group_name: str,
            members: List[str],
            is_recurring: bool,
            meeting_date: str,
            recurrence_frequency: str,
            recurrence_end_date: str,
            start_time: str,
            end_time: str
    ):
        """
        Create a new study group.
        """
        d_service = self.post_data_service
        try:
            if created_by not in members:
                members.append(created_by)
            logging.info(f"Creating study group '{group_name}' with members {members}")
            group_id = d_service.post_data_object(
                database_name=self.database,
                collection_name=self.collection,
                created_at=created_at,
                group_name=group_name,
                created_by=created_by,
                course_id=course_id,
                is_recurring=is_recurring,
                meeting_date=meeting_date,
                recurrence_frequency=recurrence_frequency,
                recurrence_end_date=recurrence_end_date,
                start_time=start_time,
                end_time=end_time,
                members=members
            )
            logging.info(f"Successfully created study group '{group_name}' with ID {group_id}")
            return group_id
        except Exception as e:
            logging.error(f"Failed to create study group '{group_name}': {e}")
            raise

    def post_by_uni_course(self, uni: str, courseid: int, group_name: str, members: List[str]):
        if len(members) == 0:
            members = [uni]
        d_service = self.post_data_service
        try:
            logging.info(f"Creating study group '{group_name}' by uni {uni} and course ID {courseid}")
            group_id = d_service.post_data_object(self.database, self.collection, group_name, uni, courseid, members)
            logging.info(f"Successfully created study group '{group_name}' with ID: {group_id}")
            return group_id
        except:
            logging.error(f"Failed to create study group '{group_name}': {e}")
            raise

    def group_exists(self, group_id: int) -> bool:
        """
        Check if a study group exists by its ID.
        """
        try:
            logging.info(f"Checking if study group with ID {group_id} exists")
            d_service = self.data_service
            result = d_service.get_data_object(
                self.database,
                self.collection,
                key_field="group_id",
                key_value=group_id
            )
            exists = result is not None
            logging.info(f"Study group with ID {group_id} exists: {exists}")
            return exists
        except Exception as e:
            logging.error(f"Error checking existence of study group with ID {group_id}: {e}")
            return False

    def delete_by_id(self, group_id: int) -> bool:
        """
        Delete a study group by its ID.
        """
        try:
            logging.info(f"Attempting to delete study group with ID {group_id}")
            success = self.data_service.delete_data_object(
                self.database,
                self.collection,
                key_field="group_id",
                key_value=group_id
            )
            if success:
                logging.info(f"Successfully deleted study group with ID {group_id}")
            else:
                logging.warning(f"Failed to delete study group with ID {group_id}")
            return success
        except Exception as e:
            logging.error(f"Error deleting study group with ID {group_id}: {e}")
            raise

    def update_by_id(self, group_id: int, update_data: Dict[str, Any]) -> bool:
        """
        Update a study group by its ID with the provided update data.
        """
        try:
            logging.info(f"Attempting to update study group with ID {group_id}")
            success = self.data_service.update_data_object(
                self.database,
                self.collection,
                key_field="group_id",
                key_value=group_id,
                update_data=update_data
            )
            if success:
                logging.info(f"Successfully updated study group with ID {group_id}")
            else:
                logging.warning(f"Failed to update study group with ID {group_id}")
            return success
        except Exception as e:
            logging.error(f"Error updating study group with ID {group_id}: {e}")
            raise

