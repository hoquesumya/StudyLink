from app.services.service_factory import ServiceFactory
from fastapi import HTTPException
import json  # To handle messages as JSON
import logging  # For logging
from typing import Optional  # Import Optional

# Configure logger
logger = logging.getLogger("ConversationService")
logger.setLevel(logging.DEBUG)  

class ConversationService:
    def __init__(self):
        self.resource = ServiceFactory.get_service('ConversationResource')

    async def create_conversation(self, conversation_data: dict) -> int:
        """Create a new conversation and return its ID."""
        try:
            formatted_conversation_data = {
                "name": conversation_data["name"],
                "participants": json.dumps(conversation_data["participants"]),  # Convert list to JSON string
                "messages": json.dumps(conversation_data["messages"]),  # Convert list of messages to JSON string
                "isGroup": bool(conversation_data["isGroup"])
            }

            conversation_id = await self.resource.create_conversation(formatted_conversation_data)
            if not conversation_id:
                logger.error("Failed to retrieve conversation ID after creation")
                raise Exception("Failed to retrieve conversation ID after creation.")

            logger.info(f"Conversation created successfully with ID: {conversation_id}")
            return conversation_id

        except Exception as e:
            logger.exception("Error occurred while creating conversation")
            raise HTTPException(status_code=400, detail=f"Error creating conversation: {str(e)}")

    def update_conversation(self, conversation_id: int, conversation_data: dict):
        """Update an existing conversation."""
        try:
            formatted_conversation_data = {
                "name": conversation_data["name"],
                "participants": json.dumps(conversation_data["participants"]),  # Convert list to JSON string
                "messages": json.dumps(conversation_data["messages"]),  # Convert list of messages to JSON string
                "isGroup": bool(conversation_data["isGroup"])
            }
            self.resource.update_conversation(conversation_id, formatted_conversation_data)
            logger.info(f"Conversation with ID {conversation_id} updated successfully")

        except Exception as e:
            logger.exception(f"Error occurred while updating conversation with ID: {conversation_id}")
            raise HTTPException(status_code=400, detail=f"Error updating conversation: {str(e)}")

    def get_conversation(self, conversation_id: int):
        """Retrieve a conversation by its ID."""
        try:
            conversation = self.resource.get_conversation(conversation_id)

            if not conversation:
                logger.warning(f"Conversation with ID {conversation_id} not found")
                raise HTTPException(status_code=404, detail=f"Conversation with ID {conversation_id} not found")

            logger.info(f"Conversation with ID {conversation_id} retrieved successfully")
            return conversation

        except Exception as e:
            logger.exception(f"Error occurred while fetching conversation with ID: {conversation_id}")
            raise HTTPException(status_code=500, detail=f"Error retrieving conversation: {str(e)}")

    def get_all_conversations(self):
        """Retrieve all conversations."""
        try:
            conversations = self.resource.get_all_conversations()

            if not conversations:
                logger.warning("No conversations found")
                raise HTTPException(status_code=404, detail="Conversations not found")

            logger.info("All conversations retrieved successfully")
            return conversations

        except Exception as e:
            logger.exception("Error occurred while fetching all conversations")
            raise HTTPException(status_code=500, detail=f"Error retrieving conversations: {str(e)}")

    def delete_conversation(self, conversation_id: int):
        """Delete a conversation by its ID."""
        try:
            self.resource.delete_conversation(conversation_id)
            logger.info(f"Conversation with ID {conversation_id} deleted successfully")

        except Exception as e:
            logger.exception(f"Error occurred while deleting conversation with ID: {conversation_id}")
            raise HTTPException(status_code=400, detail=f"Error deleting conversation: {str(e)}")

    def get_total_conversation_count(self) -> int:
        """Get the total count of conversations."""
        try:
            total_count = self.resource.get_total_conversation_count()
            logger.info(f"Total conversation count retrieved: {total_count}")
            return total_count

        except Exception as e:
            logger.exception("Error occurred while fetching total conversation count")
            raise HTTPException(status_code=500, detail=f"Error retrieving total conversation count: {str(e)}")

    def get_paginated_conversations(self, page: int, limit: int):
        """Get a paginated list of conversations."""
        try:
            conversations = self.resource.get_paginated_conversations(page, limit)

            if not conversations:
                logger.warning(f"No conversations found for Page: {page}, Limit: {limit}")
                raise HTTPException(status_code=404, detail="Conversations not found")

            logger.info(f"Paginated conversations retrieved successfully - Page: {page}, Limit: {limit}")
            return conversations

        except Exception as e:
            logger.exception(f"Error occurred while fetching paginated conversations - Page: {page}, Limit: {limit}")
            raise HTTPException(status_code=500, detail=f"Error retrieving paginated conversations: {str(e)}")