from typing import List, Optional


from fastapi import APIRouter, HTTPException, FastAPI, Form, Body, Request

from app.models.course import CourseSection
from app.resources.course_resource import CourseResource
from app.services.service_factory import ServiceFactory
import logging

logging.basicConfig(level=logging.INFO)

router = APIRouter()

@router.get("/study-group", tags=["study_group"])
async def get_all_study_groups(request: Request):
    trace_id = request.state.trace_id
    try:
        logging.info(f"TRACE_ID={trace_id} - Fetching all study groups")
        res = ServiceFactory.get_service("StudyResource")
        study_groups = res.get_all()

        if not study_groups:
            logging.warning(f"TRACE_ID={trace_id} - No study groups found")
            raise HTTPException(status_code=404, detail="No study groups found")

        data = []
        for group in study_groups:
            # logging.info(group)
            data.append({
                "group_id": group.group_id,
                "group_name": group.group_name,
                "created_by": group.created_by,
                "created_at": group.created_at,
                "is_recurring": group.is_recurring,
                "meeting_date": group.meeting_date if group.meeting_date else None,
                "recurrence_frequency": group.recurrence_frequency,
                "start_time": group.start_time if group.start_time else None,
                "end_time": group.end_time if group.end_time else None,
                "recurrence_end_date": group.recurrence_end_date,
                "course_id": group.course_id,
                "members": group.members,
                "_links": {
                    "self": {"href": f"/study-group/{group.group_id}"},
                    "edit": {"href": f"/study-group/{group.group_id}", "method": "PUT"},
                    "delete": {"href": f"/study-group/{group.group_id}", "method": "DELETE"},
                }
            })

        logging.info(f"TRACE_ID={trace_id} - Successfully fetched {len(study_groups)} study groups")
        return {
            "status": "success",
            "data": data,
            "message": f"Fetched {len(study_groups)} study group(s)"
        }

    except HTTPException as he:
        raise he
    except Exception as e:
        logging.error(f"TRACE_ID={trace_id} - Error fetching study groups: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while fetching study groups")


@router.get("/study-group/{group_id}", tags=["study_group"])
async def get_single_study_group(group_id: str, request: Request):
    trace_id = request.state.trace_id
    logging.info(f"TRACE_ID={trace_id} - Fetching study group with ID: {group_id}")

    try:
        res = ServiceFactory.get_service("StudyResource")
        result = res.get_by_id(group_id)

        if not result:
            logging.warning(f"TRACE_ID={trace_id} - Study group with ID {group_id} not found")
            raise HTTPException(status_code=404, detail=f"Study group with ID {group_id} not found")

        logging.info(f"TRACE_ID={trace_id} - Successfully fetched study group with ID: {group_id}")
        return {
            "status": "success",
            "data": result,
            "_links": {
                "self": {"href": f"/study-group/{group_id}"},
                "edit": {"href": f"/study-group/{group_id}", "method": "PUT"},
                "delete": {"href": f"/study-group/{group_id}", "method": "DELETE"},
                "list": {"href": "/study-group", "method": "GET"}
            },
            "message": f"Fetched study group"
        }
    except ValueError as ve:
        # Catch ValueError raised in get_by_id and raise HTTPException with 404
        logging.warning(f"TRACE_ID={trace_id} - {ve}")
        raise HTTPException(status_code=404, detail=str(ve))
    except HTTPException as he:
        raise he
    except Exception as e:
        logging.error(f"TRACE_ID={trace_id} - Error fetching study group with ID {group_id}: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while fetching study group")

@router.post("/study-group", tags=["study_group"])
async def post_study_group(request: Request,
    group_data: dict = Body(..., example={
        "group_name": "Test Study Group",
        "created_by": "test_user",
        "created_at": "2025-06-30",
        "course_id": "1234",
        "is_recurring": True,
        "meeting_date": "2025-06-30",
        "recurrence_frequency": "weekly",
        "recurrence_end_date": "2025-06-30",
        "start_time": "9:00:00",
        "end_time": "10:00:00",
        "members": ["user1", "user2"]
    })
):
    trace_id = request.state.trace_id

    try:
        logging.info(f"TRACE_ID={trace_id} - Creating study group: {group_data.get('group_name')}")

        if "members" not in group_data or not group_data["members"]:
            group_data["members"] = []

        # Ensure the creator is in the members list
        if group_data["created_by"] not in group_data["members"]:
            group_data["members"].append(group_data["created_by"])

        res = ServiceFactory.post_service("StudyResource")

        group_id = res.post_group(
            group_name=group_data["group_name"],
            created_by=group_data["created_by"],
            created_at=group_data["created_at"],
            course_id=group_data["course_id"],
            is_recurring=group_data["is_recurring"],
            meeting_date=group_data["meeting_date"],
            recurrence_frequency=group_data["recurrence_frequency"],
            recurrence_end_date=group_data["recurrence_end_date"],
            start_time=group_data["start_time"],
            end_time=group_data["end_time"],
            members=group_data["members"]
        )

        logging.info(f"TRACE_ID={trace_id} - Created study group with ID: {group_id}")

        return {
                    "status": "success",
                    "message": f"Group '{group_data['group_name']}' created successfully.",
                    "group_id": group_id,
                    "data": group_data,
                    "_links": {
                        "self": {"href": f"/study-group/{group_id}"},
                        "list": {"href": "/study-group"}
                    }
                }
    except Exception as e:
        logging.error(f"TRACE_ID={trace_id} - Error creating study group: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while creating the study group.")

@router.delete("/study-group/{group_id}", tags=["study_group"])
async def delete_study_group(group_id: int, request: Request):
    """
    Delete a study group by its ID.
    """
    trace_id = request.state.trace_id
    logging.info(f"TRACE_ID={trace_id} - Attempting to delete study group with ID: {group_id}")

    try:
        res = ServiceFactory.get_service("StudyResource")
        # Verify group exists before deletion
        if not res.group_exists(group_id):
            logging.warning(f"TRACE_ID={trace_id} - Study group with ID {group_id} not found")
            raise HTTPException(status_code=404, detail=f"Study group with ID {group_id} not found")

        res.delete_by_id(group_id)
        logging.info(f"TRACE_ID={trace_id} - Successfully deleted study group with ID: {group_id}")
        return {"status": "success", "message": f"Study group {group_id} has been deleted"}
    except HTTPException as he:
        raise he
    except Exception as e:
        logging.error(f"TRACE_ID={trace_id} - Error deleting study group with ID {group_id}: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while deleting the study group")


@router.put("/study-group/{group_id}", tags=["study_group"])
async def edit_study_group(group_id: int, request: Request, update_data: dict = Body(..., example={
    "group_name": "Updated Study Group Name",
    "is_recurring": False,
    "meeting_date": "2025-06-30",
    "recurrence_frequency": None,
    "recurrence_end_date": "2025-07-30",
    "start_time": "09:30:00",
    "end_time": "10:30:00",
    "members": ["user3", "user4"]
    })):
    """
    Edit a study group's details by its ID.
    At least one optional parameter must be provided to make changes.
    """
    trace_id = request.state.trace_id
    logging.info(f"TRACE_ID={trace_id} - Attempting to edit study group with ID: {group_id}")

    try:
        if not update_data:
            logging.warning(f"TRACE_ID={trace_id} - No update fields provided for group ID: {group_id}")
            raise HTTPException(status_code=400, detail="No update fields provided")

        # if "meeting_date" in update_data:
        #     update_data["meeting_date"] = datetime.strptime(update_data["meeting_date"], "%Y-%m-%d").date().isoformat()
        #
        # if "recurrence_end_date" in update_data:
        #     update_data["recurrence_end_date"] = datetime.strptime(update_data["recurrence_end_date"], "%Y-%m-%d").date().isoformat()
        #
        # if "start_time" in update_data:
        #     update_data["start_time"] = str(datetime.strptime(update_data["start_time"], "%H:%M:%S").time())
        #
        # if "end_time" in update_data:
        #     update_data["end_time"] = str(datetime.strptime(update_data["end_time"], "%H:%M:%S").time())
            
        res = ServiceFactory.get_service("StudyResource")

        # Verify group exists before editing
        if not res.group_exists(group_id):
            logging.warning(f"TRACE_ID={trace_id} - Study group with ID {group_id} not found")
            raise HTTPException(status_code=404, detail=f"Study group with ID {group_id} not found")

        res.update_by_id(group_id, update_data)
        logging.info(f"TRACE_ID={trace_id} - Successfully updated study group with ID: {group_id}")

        return {
            "status": "success",
            "message": f"Study group {group_id} has been updated successfully",
            "updated_fields": update_data,
            "_links": {
                "self": {"href": f"/study-group/{group_id}"},
                "list": {"href": "/study-group"},
                "edit": {"href": f"/study-group/{group_id}", "method": "PUT"},
                "delete": {"href": f"/study-group/{group_id}", "method": "DELETE"}
            }
        }
    except HTTPException as he:
        logging.warning(f"TRACE_ID={trace_id} - HTTPException encountered: {he.detail}")
        raise he
    except ValueError as ve:
        logging.error(f"TRACE_ID={trace_id} - Invalid date or time format: {ve}")
        raise HTTPException(status_code=400, detail="Invalid date or time format")
    except Exception as e:
        logging.error(f"TRACE_ID={trace_id} - Unexpected error updating group {group_id}: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while updating the study group")

