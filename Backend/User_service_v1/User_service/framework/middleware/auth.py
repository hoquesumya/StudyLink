from fastapi import Request, HTTPException
from typing import Optional
from google.oauth2 import id_token
from google.auth.transport import requests
import os

class GoogleAuthMiddleware:
    def __init__(self):
        self.google_client_id = os.getenv("GOOGLE_CLIENT_ID")
        self.public_keys = requests.Request()

    async def authenticate(self, request: Request) -> Optional[dict]:
        try:
            token = request.headers.get("Google-Token")
            if not token:
                print("No token found in cookie")
                return None

            idinfo = id_token.verify_oauth2_token(
                token,
                self.public_keys,
                self.google_client_id
            )

            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise ValueError('Wrong issuer.')

            return idinfo

        except Exception as e:
            raise HTTPException(
                status_code=401,
                detail=f"Invalid authentication credentials: {str(e)}"
            )

