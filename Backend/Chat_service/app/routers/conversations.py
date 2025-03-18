import logging
from urllib.parse import urlencode
from fastapi import APIRouter, HTTPException, Query, BackgroundTasks, Request
from typing import Optional
from app.services.conversation_service import ConversationService
from fastapi.responses import JSONResponse
import uuid
import asyncio

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Set the logging level to INFO
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

router = APIRouter()
conversation_service = ConversationService()

# Simulate a task store to track background task statuses
task_store = {}

# To store background task if operation is too long
async def process_conversation_creation(task_id: str, conversation: dict): 
    """
    Simulate asynchronous processing of conversation creation.
    """
    try:
        await asyncio.sleep(5)  # Simulate a long-running task (e.g., database operation)
        conversation_id = await conversation_service.create_conversation(conversation)
        logger.info(f"Conversation created successfully for task_id: {task_id}")

        task_store[task_id] = {
            "status": "completed",
            "status_code": 201,
            "result": {"convo_id": conversation_id["convo_id"], "detail": "Conversation created successfully"}
        }
    except Exception as e:
        logger.error(f"Error processing conversation creation for task_id {task_id}: {str(e)}")
        task_store[task_id] = {"status": "failed","status_code": 500, "error": str(e)}


@router.post(
    "/conversations/",
    tags=["conversations"],
    responses={
        202: {"description": "Conversation creation request accepted for processing"},
        400: {"description": "Bad request - invalid parameters"},
        409: {"description": "Conflict - conversation already exists"}
    },
)
async def create_conversation(conversation: dict, background_tasks: BackgroundTasks, request: Request):
    """
    Accept a conversation creation request and process it asynchronously.
    """
    trace_id = getattr(request.state, "trace_id", "UNKNOWN")
    
    try:
        task_id = str(uuid.uuid4())
        logger.info(f"TRACE_ID={trace_id} - Received conversation creation request. Task ID: {task_id}")
        task_store[task_id] = {"status": "in_progress", "status_code": 202, "result": None}
        background_tasks.add_task(process_conversation_creation, task_id, conversation)
        logger.info(f"TRACE_ID={trace_id} - Conversation creation task {task_id} added to background tasks.")
        
        return JSONResponse(
            content={
                "task_id": task_id,
                "status": "in_progress",
                "status_url": f"/tasks/{task_id}",
                "detail": "Conversation creation request accepted. Processing in progress.",
                "_links": {
                    "self": {
                        "href": f"/conversations/",
                        "method": "POST"
                    },
                    "get_task_status": {
                        "href": f"/conversations/tasks/{task_id}",
                        "method": "GET"
                    },
                    "get_created_conversation": {
                        "href": "/conversations/{conversation_id}",
                        "method": "GET"
                    },
                    "delete_conversation": {
                        "href": "/conversations/{conversation_id}",
                        "method": "DELETE"
                    },
                    "list_conversations": {
                        "href": "/conversations/",
                        "method": "GET"
                    },
                    "create_conversation": {
                        "href": "/conversations/",
                        "method": "POST"
                    }
                }
            },
            status_code=202
        )
    except HTTPException as e:
        logger.error(f"TRACE_ID={trace_id} - HTTPException: {str(e)}")
        raise e
    
    except Exception as e:
        logger.exception(f"TRACE_ID={trace_id} - Error starting conversation creation task: {str(e)}")
        raise HTTPException(status_code=500, detail="Error starting conversation creation task.")

@router.get(
    "/tasks/{task_id}",
    tags=["tasks"],
    responses={
        200: {"description": "Task status retrieved successfully"},
        404: {"description": "Task not found"},
    },
)
async def get_task_status(task_id: str):
    """
    Retrieve the status of a background task by its task_id.
    """
    task = task_store.get(task_id)
    if not task:
        logger.warning(f"Task with task_id {task_id} not found.")
        raise HTTPException(status_code=404, detail="Task not found.")
    return JSONResponse(
        content={
            "status": task["status"],
            "result": task["result"],
            "_links": {
                "self": {
                    "href": f"/tasks/{task_id}",
                    "method": "GET"
                },
                "get_created_conversation": {
                    "href": f"/conversations/{task['result']['convo_id']}",
                    "method": "GET"
                },
                "delete_conversation": {
                    "href": f"/conversations/{task['result']['convo_id']}",
                    "method": "DELETE"
                },
                "list_conversations": {
                    "href": "/conversations/",
                    "method": "GET"
                },
                "create_conversation": {
                    "href": "/conversations/",
                    "method": "POST"
                }
            }
        },
        status_code=task["status_code"]
    )


@router.put("/conversations/{conversation_id}",
            tags=["conversations"],
            responses={
                200: {"description": "Conversation updated successfully"},
                404: {"description": "Conversation not found"},
                400: {"description": "Bad request - invalid parameters"}
            })
async def update_conversation(conversation_id: int, conversation: dict, request: Request):
    try:
        trace_id = getattr(request.state, "trace_id", "UNKNOWN")
        conversation_service.update_conversation(conversation_id, conversation)
        logger.info(f"TRACE_ID={trace_id} - Conversation with ID {conversation_id} updated successfully.")
        
        return JSONResponse(
            content={
                "detail": "Conversation updated successfully",
                "_links": {
                    "self": {
                        "href": f"/conversations/{conversation_id}",
                        "method": "PUT"
                    },
                    "get_conversation": {
                        "href": f"/conversations/{conversation_id}",
                        "method": "GET"
                    },
                    "delete_conversation": {
                        "href": f"/conversations/{conversation_id}",
                        "method": "DELETE"
                    },
                    "list_conversations": {
                        "href": "/conversations/",
                        "method": "GET"
                    },
                    "create_conversation": {
                        "href": "/conversations/",
                        "method": "POST"
                    }
                }
            },
            status_code=200
        )
    
    except HTTPException as e:
        logger.error(f"TRACE_ID={trace_id} - HTTPException while updating conversation ID {conversation_id}: {e.detail}")
        raise e
    except Exception as e:
        logger.exception(f"TRACE_ID={trace_id} - Error updating conversation ID {conversation_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get(
    "/conversations/{conversation_id}",
    tags=["conversations"],
    responses={
        200: {"description": "Conversation retrieved successfully"},
        404: {"description": "Conversation not found"},
        400: {"description": "Bad request - invalid parameters"},
    },
)
async def get_conversation(conversation_id: int, request: Request):
    try:
        trace_id = getattr(request.state, "trace_id", "UNKNOWN")
        conversation = conversation_service.get_conversation(conversation_id)
        
        if not conversation:
            logger.warning(f"TRACE_ID={trace_id} - Conversation with ID {conversation_id} not found.")
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        logger.info(f"TRACE_ID={trace_id} - Successfully retrieved conversation with ID {conversation_id}")
        return JSONResponse(
            content={
                "detail": conversation,
                "_links": {
                    "self": {
                        "href": f"/conversations/{conversation_id}",
                        "method": "GET"
                    },
                    "update_conversation": {
                        "href": f"/conversations/{conversation_id}",
                        "method": "PUT"
                    },
                    "delete_conversation": {
                        "href": f"/conversations/{conversation_id}",
                        "method": "DELETE"
                    },
                    "list_conversations": {
                        "href": "/conversations/",
                        "method": "GET"
                    },
                    "create_conversation": {
                        "href": "/conversations/",
                        "method": "POST"
                    }
                }
            },
            status_code=200
        )
    
    except HTTPException as e:
        logger.error(f"TRACE_ID={trace_id} - HTTPException while retrieving conversation ID {conversation_id}: {e.detail}")
        raise e
    
    except Exception as e:
        logger.exception(f"TRACE_ID={trace_id} - Unexpected error while retrieving conversation ID {conversation_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
        

@router.get("/conversations/",
            tags=["conversations"],
            responses={
                200: {"description": "Conversation retrieved successfully"},
                404: {"description": "Conversation not found"},
                400: {"description": "Bad request - invalid parameters"}
            })
async def get_all_conversations(
    request: Request,
    page: Optional[int] = Query(None, gt=0),
    limit: Optional[int] = Query(None, gt=0)
):
    try:
        trace_id = getattr(request.state, "trace_id", "UNKNOWN")
        if page is not None and limit is not None:
            total_conversations = conversation_service.get_total_conversation_count()
            conversations = conversation_service.get_paginated_conversations(page, limit)
            total_pages = (total_conversations + limit - 1) // limit
            logger.info(f"TRACE_ID={trace_id} - Successfully retrieved paginated conversations: page={page}, limit={limit}, total_pages={total_pages}")
            
            return JSONResponse(
                content={
                    "detail": conversations,
                    "total": total_conversations,
                    "page": page,
                    "limit": limit,
                    "total_pages": total_pages
                },
                status_code=200
            )
        else:
            conversations = conversation_service.get_all_conversations()
            logger.info(f"TRACE_ID={trace_id} - Successfully retrieved all conversations without pagination.")
            
        return JSONResponse(
            content={
                "detail": conversations,
                "_links": {
                    "self": {
                        "href": f"/conversations/conversation_id",
                        "method": "GET"
                    },
                    "update_conversation": {
                        "href": f"/conversations/conversation_id",
                        "method": "PUT"
                    },
                    "delete_conversation": {
                        "href": f"/conversations/conversation_id",
                        "method": "DELETE"
                    },
                    "list_conversations": {
                        "href": "/conversations/",
                        "method": "GET"
                    },
                    "create_conversation": {
                        "href": "/conversations/",
                        "method": "POST"
                    }
                }
            },
            status_code=200
        )
    
    except HTTPException as e:
        logger.error(f"TRACE_ID={trace_id} - HTTPException while retrieving all conversations: {e.detail}")
        raise e
    
    except Exception as e:
        logger.exception(f"TRACE_ID={trace_id} - Error retrieving all conversations: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.delete(
    "/conversations/{conversation_id}",
    tags=["conversations"],
    responses={
        200: {"description": "Conversation deleted successfully"},
        404: {"description": "Conversation not found"},
        400: {"description": "Bad request - invalid parameters"}
    }
)
async def delete_conversation(conversation_id: int, request: Request):
    """
    Deletes a conversation by its ID and provides HATEOAS links for further actions.
    """
    trace_id = getattr(request.state, "trace_id", "UNKNOWN")
    try:
        conversation_service.delete_conversation(conversation_id)
        logger.info(f"TRACE_ID={trace_id} - Conversation with ID {conversation_id} deleted successfully.")
        
        # Return response with HATEOAS links
        return JSONResponse(
            content={
                "detail": "Conversation deleted successfully",
                "_links": {
                    "self": {
                        "href": f"/conversations/{conversation_id}",
                        "method": "DELETE"
                    },              
                    "update_conversation": {
                        "href": f"/conversations/{conversation_id}",
                        "method": "PUT"
                    },
                    "delete_conversation": {
                        "href": f"/conversations/{conversation_id}",
                        "method": "DELETE"
                    },
                    "get_conversation": {
                        "href": f"/conversations/conversation_id",
                        "method": "GET"
                    },
                    "get_all_conversations": {
                        "href": "/conversations/",
                        "method": "GET"
                    },
                    "create_conversation": {
                        "href": "/conversations/",
                        "method": "POST"
                    },
                }
            },
            status_code=200
        )
    except HTTPException as e:
        logger.error(f"TRACE_ID={trace_id} - HTTPException while deleting conversation ID {conversation_id}: {str(e)}")
        raise e
    except Exception as e:
        logger.error(f"TRACE_ID={trace_id} - Error deleting conversation ID {conversation_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))