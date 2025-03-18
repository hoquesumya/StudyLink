from fastapi import APIRouter, Header, Query, Request
from app.services.ChatServices import Chat
from app.services.StudGroup import StudyGroup
from app.services.UserServices import UserService
from app.services.CourseEnrollment import CourseEnrolment
import asyncio
from typing import Any, Dict, List, Union

router = APIRouter()
group = StudyGroup()
chat =  Chat()
user = UserService()
course = CourseEnrolment()


# User Profile Service
@router.get("/StudyLink/v1/users/{user_id}/login", tags=["users"])
def get_user_login(
    user_id: str,
    google_token: str= Header(...),
):
        #google_user = json.loads(google_token)
        return user.get_user_login(user_id, google_token)

#def get_user_login(user_id:str, google_user:dict, jwt_payload:dict):
   #return user.get_user_login(user_id, google_user, jwt_payload)

@router.get("/StudyLink/v1/users/{user_id}/profile", tags=["users"])
def get_user_profile(user_id: str, google_token: str=Header(...),
                     authorization:str = Header(...)):
    """
    Retrieve the profile of a user by user ID.
    """
    print("calling the fuction")
    print(authorization)

    #jwt_payload =json.loads(authorization)
    return user.get_user(user_id, google_token, authorization)
   

#need to fix 
@router.post("/StudyLink/v1/users/{user_id}/profile", tags=["users"])
def post_user_profile(user_id: str, token: str,  google_token: str=Header(...)):
    """
    Create  the profile of a user by user ID.
    """
    return user.post_user(user_id, token, google_token)

@router.delete("/StudyLink/v1/users/{user_id}/profile", tags=["users"])
def delete_user_profile(user_id: str, 
                         google_token: str=Header(...), 
                         authorization:str = Header(...)):
   
    return  user.delete_user(user_id, google_token, authorization)

@router.get("/StudyLink/v1/users/", tags=["users"])
def get_all_users(google_token: str=Header(...), 
                authorization:str = Header(...)):
   
    return user.get_all_users(google_token, authorization)

#.................. Course Enrollment Service............
@router.get("/StudyLink/v1/course/{course_id}/students")
def get_all_students(course_id:str, token: str = Header(...)):
    print("staried finding all courses")
    return course.get_all_students(course_id, token)

@router.get("/StudyLink/v1/users/{student_id}/courses")
def get_allcourse(student_id: str, token: str = Header(...)):
    print("started the request for students course")
    return course.get_all_course(student_id, token)

# .................Chat Service..................
@router.post("/StudyLink/v1/{user_id}/conversations", tags=["conversations"])
def create_conversation(user_id: str, conversation: dict, google_token:str=Header(...), authorization:str=Header(...)):
    print("started chat")
   
    return chat.post_chat(user_id, conversation, google_token, authorization)

@router.put("/StudyLink/v1/{user_id}/conversations/{conversation_id}", tags=["conversations"])
def update_conversation(user_id: str, conversation_id: int, conversation: dict,  google_token:str=Header(...), authorization:str=Header(...)):
    """
    Update a conversation by conversation ID for a user by user ID.
    """
    return chat.update_chat(user_id, conversation_id, conversation, google_token, authorization)

@router.get("/StudyLink/v1/conversations/{conversation_id}", tags=["conversations"])
def get_conversation(conversation_id: int):
   return chat.get_chat(conversation_id)

@router.delete("/StudyLink/v1/{user_id}/conversations/{conversation_id}", tags=["conversations"])
def delete_convo(user_id: str, conversation_id: int, google_token:str=Header(...), authorization:str=Header(...)):
    print("printing delteing")
    chat.delete_chat_workflow(user_id, conversation_id, google_token, authorization)
    #return chat.delete_chat(user_id, conversation_id, google_token, authorization)

@router.get("/StudyLink/v1/conversations")
def get_all_chat():
    return chat.get_all_chat()
#......................StudyGroup.....................
@router.get("/StudyLink/v1/study-group/{group_id}", tags = ["study-group"])
def get_studyGroup( group_id:str):
    return group.get_group(group_id=group_id)

@router.get("/StudyLink/v1/study-group/", tags = ["studyGroup"])
def get_all_group():
    return group.get_all_group()

@router.post("/StudyLink/v1/{user_id}/study-group/", tags = ["study-group"])
async def post_studyGroup(user_id: str, group_data:dict, google_token:str=Header(...), authorization:str=Header(...)):
    print("statting the creating the group")
    #google_user = json.loads(google_token)
    res = await group.create_group(user_id,group_data, google_token, authorization)
    return res

@router.delete("/StudyLink/v1/{user_id}/study-group/{group_id}", tags = ["study-group"])
def get_studyGroup(user_id: str, group_id: int, google_token:str=Header(...), authorization:str=Header(...) ):
    #google_user = json.loads(google_token)
    return group.delete_group(user_id, group_id,google_token, authorization)

@router.put("/StudyLink/v1/{user_id}/study-group/{group_id}", tags = ["study-group"])
def update_study_group( user_id: str, group_id: int, update_data:dict, google_token:str=Header(...), authorization:str=Header(...)):
    print("update data", update_data)
   #google_user = json.loads(google_token)
    return group.update_group(user_id, group_id, update_data, google_token, jwt_payload=authorization)

