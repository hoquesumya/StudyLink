from fastapi import Depends, HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt.exceptions import InvalidTokenError
from app.services.user_service import UserProfileService
from ..utils.auth import get_current_user
import httpx
from fastapi import APIRouter
from google.auth.transport.requests import Request
from google.oauth2 import service_account
import os
import base64
import json
import jwt
import logging
from datetime import datetime, timedelta, timezone
from framework.middleware.jwt_middleware import JWTMiddleware

# GOOGLE CLOUD PLATFORM LOGGING
# from google.cloud import logging as gcp_logging
# TO DO - Add logging to GCP console
# gcp_client = gcp_logging.Client()
# gcp_client.setup_logging()
# logging.info("Google Cloud Logging configured in router.")

# Logging for EC2 instance
logging.basicConfig(level=logging.INFO)

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")  
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_DELTA = timedelta(days=1)


# Reusable function to generate HATEOAS links
def generate_hateoas_links(user_id: str) -> dict:
    return {
        "self": {"href": f"/users/{user_id}/profile", "method": "GET"},
        "update": {"href": f"/users/{user_id}/profile", "method": "POST"},
        "delete": {"href": f"/users/{user_id}/profile", "method": "DELETE"},
        "all_users": {"href": "/users", "method": "GET"}
    }


# Utility for JWT tokens
def generate_jwt_token(user_id: str, email: str, grants: list = None) -> str:
    """Generate a JWT token for the user."""
    payload = {
        "user_id": user_id,
        "email": email,
        "grants": grants or [],
        "exp": datetime.now(timezone.utc) + JWT_EXPIRATION_DELTA,
        "iat": datetime.now(timezone.utc)
    }
    return jwt.encode(payload, str(JWT_SECRET_KEY), algorithm=JWT_ALGORITHM)


# Initialize dependencies
jwt_middleware = JWTMiddleware()
router = APIRouter()
user_profile_service = UserProfileService()

# Decode Google Application Credentials
encoded_credentials = os.getenv("GOOGLE_APPLICATION_CREDENTIALS_JSON_BASE64")
decoded_credentials = base64.b64decode(encoded_credentials).decode("utf-8")
credentials_data = json.loads(decoded_credentials)


def get_identity_token_audience(audience: str) -> str:
    """Fetch the identity token for a specific audience."""
    # Load service account credentials
    credentials = service_account.IDTokenCredentials.from_service_account_info(
        credentials_data,
        target_audience=audience
    )
    request = Request()
    credentials.refresh(request)
    return credentials.token


@router.post("/users/{user_id}/profile", tags=["users"])
async def create_or_update_profile(user_id: str, token: str):
    """Create or update user profile"""
    try:
        logging.info(f"Creating or updating profile for user_id={user_id}")
        user_profile_service.create_or_update_profile(user_id, token)
        profile_data = user_profile_service.get_user_profile(user_id)
        grants = ['user:read', 'user:delete', 'user:post', 'user:put']
        jwt_token = generate_jwt_token(user_id, profile_data['email'], grants=grants)
        profile_data['jwt_token'] = jwt_token
        profile_data["_links"] = generate_hateoas_links(user_id)

        # Trigger the Pub/Sub function
        pubsub_function_url = "https://us-central1-auth-443323.cloudfunctions.net/python-pubsub-function"
        pubsub_headers = {
            "Authorization": f"Bearer {get_identity_token_audience(pubsub_function_url)}",
            "Content-Type": "application/json",
            "ce-id": "1234567890",
            "ce-specversion": "1.0",
            "ce-type": "google.cloud.pubsub.topic.v1.messagePublished",
            "ce-time": "2020-08-08T00:11:44.895529672Z",
            "ce-source": "//pubsub.googleapis.com/projects/auth-443323/topics/user_signup"
        }
        email = base64.b64encode(json.dumps({"to_email": profile_data['email']}).encode("utf-8")).decode("utf-8")
        pubsub_data = {
            "message": {
                "data": email
            }
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(pubsub_function_url, json=pubsub_data, headers=pubsub_headers)

        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=f"Pub/Sub function error: {response.text}")

        headers = {"Location": f"/users/{user_id}/profile"}
        return {
            "message": f"Profile for {user_id} created successfully",
            "profile": profile_data
        }, 201, headers

    except Exception as e:
        logging.exception(f"Error creating profile for user_id={user_id}: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Error creating profile: {str(e)}")


@router.get("/users/{user_id}/profile", tags=["users"])
async def get_user_profile(
        user_id: str,
        google_user: dict = Depends(get_current_user),
        jwt_payload: dict = Depends(jwt_middleware.verify_read)):
    """Retrieve a user profile."""
    try:
        logging.info(f"Fetching profile for user_id={user_id}")
        profile = user_profile_service.get_user_profile(user_id)
        profile["_links"] = generate_hateoas_links(user_id)
        return profile
    except Exception as e:
        logging.exception(f"Error fetching profile for user_id={user_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching profile: {str(e)}")


@router.delete("/users/{user_id}/profile", tags=["users"])
async def delete_user_profile(
    user_id: str,
    google_user: dict = Depends(get_current_user),
    jwt_payload: dict = Depends(jwt_middleware.verify_delete)):
    """Delete a user profile."""
    try:
        logging.info(f"Deleting profile for user_id={user_id}")
        if google_user.get('email').split('@')[0] != user_id:
            logging.warning(f"Unauthorized deletion attempt for user_id={user_id} by {google_user.get('email')}")
            raise HTTPException(status_code=403, detail="You can only delete your own profile")

        user_profile_service.delete_user_profile(user_id)
        return {"message": f"Profile for user_id={user_id} deleted successfully"}
    except Exception as e:
        logging.exception(f"Error deleting profile for user_id={user_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error deleting profile: {str(e)}")


@router.get("/users", tags=["users"])
async def get_users(
    skip: int = 0, 
    limit: int = 10, 
    name: str = None, 
    course: str = None, 
    google_user: dict = Depends(get_current_user),
    jwt_payload: dict = Depends(jwt_middleware.verify_read)):
    """Retrieve user profiles by optional filters."""
    try:
        logging.info(f"Fetching users with skip={skip}, limit={limit}, name={name}, course={course}")
        users = user_profile_service.get_users(
            skip=skip, 
            limit=limit, 
            name=name, 
            course=course
        )
        
        if not users:
            return {
                "users": [], 
                "count": 0, 
                "message": "No users found matching the criteria"
            }
            
        return {
            "users": users,
            "count": len(users),
            "_links": {
                "self": {"href": "/users", "method": "GET"}
            }
        }
        
    except Exception as e:
        logging.exception(f"Error fetching users: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Error fetching users: {str(e)}"
        )


@router.get("/users/{user_id}/login", tags=["users"])
async def user_login(user_id: str, google_user: dict = Depends(get_current_user)):
    """Retrieve a user profile."""
    try:
        logging.info(f"Logging in user_id={user_id}")
        profile = user_profile_service.get_user_profile(user_id)
        grants = ['user:read', 'user:delete', 'user:post', 'user:put']
        jwt_token = generate_jwt_token(user_id, google_user.get('email'), grants=grants)
        profile['jwt_token'] = jwt_token
        profile["_links"] = generate_hateoas_links(user_id)
        return profile
    except Exception as e:
        logging.exception(f"Error during login for user_id={user_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error during login: {str(e)}")
