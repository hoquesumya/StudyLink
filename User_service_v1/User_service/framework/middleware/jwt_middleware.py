from fastapi import HTTPException, Security, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt.exceptions import InvalidTokenError
import jwt
import os
from app.utils.auth import get_current_user  # Adjusted import path

class JWTMiddleware:
    def __init__(self):
        self.security = HTTPBearer()
        self.jwt_secret_key = os.getenv("JWT_SECRET_KEY")
        self.jwt_algorithm = "HS256"
        
        if self.jwt_secret_key is None:
            raise ValueError("JWT_SECRET_KEY environment variable is not set")

    async def verify_jwt_and_grant(self, required_grant: str, 
                                 credentials: HTTPAuthorizationCredentials = Security(HTTPBearer()),
                                 google_user: dict = Depends(get_current_user)):
        """
        Verify JWT token and check for specific grant permission and email match.
        """
        print('jwt_secret_key', self.jwt_secret_key)
        print('jwt_algorithm', self.jwt_algorithm)
        try:
            print("Verifying JWT token...")
            print("Credentials:", credentials)
            print("Google user:", google_user)
            
            token = credentials.credentials
            print("Token:", token)
            
            payload = jwt.decode(
                token, 
                str(self.jwt_secret_key), 
                algorithms=[self.jwt_algorithm]
            )
            print("Decoded payload:", payload)
            
            # Verify email matches
            jwt_email = payload.get('email')
            google_email = google_user.get('email')
            print(f"Comparing emails - JWT: {jwt_email}, Google: {google_email}")
            
            if not jwt_email or jwt_email != google_email:
                raise HTTPException(
                    status_code=403,
                    detail="JWT token email does not match authenticated user"
                )

            # Verify grant
            print(f"Checking for required grant: {required_grant}")
            if required_grant not in payload.get('grants', []):
                raise HTTPException(
                    status_code=403,
                    detail=f"Insufficient permissions. Required grant: {required_grant}"
                )
            
            print("Verification successful, returning payload")
            return payload
            
        except InvalidTokenError as e:
            print(f"Invalid token error: {str(e)}")
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            raise

    async def verify_delete(self, 
                          credentials: HTTPAuthorizationCredentials = Security(HTTPBearer()),
                          google_user: dict = Depends(get_current_user)):
        return await self.verify_jwt_and_grant("user:delete", credentials, google_user)

    async def verify_read(self, 
                         credentials: HTTPAuthorizationCredentials = Security(HTTPBearer()),
                         google_user: dict = Depends(get_current_user)):
        print("verify_read called")
        print("credentials:", credentials)
        print("google_user:", google_user)
        return await self.verify_jwt_and_grant("user:read", credentials, google_user)

    async def verify_post(self, 
                         credentials: HTTPAuthorizationCredentials = Security(HTTPBearer()),
                         google_user: dict = Depends(get_current_user)):
        return await self.verify_jwt_and_grant("user:post", credentials, google_user)

    async def verify_put(self, 
                        credentials: HTTPAuthorizationCredentials = Security(HTTPBearer()),
                        google_user: dict = Depends(get_current_user)):
        return await self.verify_jwt_and_grant("user:put", credentials, google_user)