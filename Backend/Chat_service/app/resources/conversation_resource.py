import logging
from typing import Any, List, Optional
import asyncio

# Configure logger
logger = logging.getLogger("ConversationResource")
logger.setLevel(logging.INFO)  # Adjust log level as needed

class ConversationResource:
    def __init__(self):
        from app.services.service_factory import ServiceFactory
        self.data_service = ServiceFactory.get_service('ConversationResourceService')

    async def create_conversation(self, conversation: dict) -> dict:
        try:
            inserted_id = await asyncio.to_thread(
                self.data_service.insert,
                database_name="p1_database",
                table="conversations",
                data=conversation
            )
            logger.info(f"Conversation created successfully with ID {inserted_id}.")
            return {"convo_id": inserted_id}  # Return as a dictionary for consistency
        except Exception as e:
            logger.error(f"Error creating conversation: {str(e)}")
            raise Exception(f"{str(e)}")
    
    def update_conversation(self, conversation_id: int, conversation: dict) -> dict:
        try:
            self.data_service.update(
                database_name="p1_database",
                table="conversations",
                data=conversation, 
                key_field="convo_id",
                key_value=conversation_id
            )
            logger.info(f"Conversation with ID {conversation_id} updated successfully.")
        except Exception as e:
            logger.error(f"Error updating conversation with ID {conversation_id}: {str(e)}")
            raise Exception(f"{str(e)}")

    def get_conversation(self, conversation_id: int) -> Optional[dict]:
        try:
            result = self.data_service.fetch_one(
                database_name="p1_database",
                table="conversations",
                key_field="convo_id",
                key_value=conversation_id
            )
            if result:
                logger.info(f"Conversation with ID {conversation_id} retrieved successfully.")
            else:
                logger.warning(f"No conversation found with ID {conversation_id}.")
            return result
        except Exception as e:
            logger.error(f"Error retrieving conversation with ID {conversation_id}: {str(e)}")
            raise Exception(f"{str(e)}")

    def get_all_conversations(self) -> List[dict]:
        try:
            result = self.data_service.fetch_all(
                database_name="p1_database",
                table="conversations"
            )
            logger.info(f"Successfully retrieved {len(result)} conversations.")
            return result
        except Exception as e:
            logger.error(f"Error retrieving all conversations: {str(e)}")
            raise Exception(f"{str(e)}")

    def get_paginated_conversations(self, page: int, limit: int) -> List[dict]:
        try:
            offset = (page - 1) * limit
            conversations = self.data_service.fetch_paginated(
                database_name="p1_database",
                table="conversations",
                offset=offset,
                limit=limit
            )
            logger.info(f"Successfully retrieved {len(conversations)} conversations (page: {page}, limit: {limit}).")
            return conversations
        except Exception as e:
            logger.error(f"Error retrieving paginated conversations: {str(e)}")
            raise Exception(f"{str(e)}")

    def delete_conversation(self, conversation_id: int) -> None:
        try:
            self.data_service.delete(
                database_name="p1_database",
                table="conversations",
                key_field="convo_id",
                key_value=conversation_id
            )
            logger.info(f"Conversation with ID {conversation_id} deleted successfully.")
        except Exception as e:
            logger.error(f"Error deleting conversation with ID {conversation_id}: {str(e)}")
            raise Exception(f"Error deleting conversation: {str(e)}")
        
    def get_total_conversation_count(self) -> int:
        try:
            count = self.data_service.count_all(
                database_name="p1_database",
                table="conversations"
            )
            logger.info(f"Total conversations count: {count}.")
            return count
        except Exception as e:
            logger.error(f"Error retrieving total conversation count: {str(e)}")
            raise Exception(f"Error retrieving total conversation count: {str(e)}")