from typing import Optional
from fastapi import Request, HTTPException
from framework.middleware.auth import GoogleAuthMiddleware


auth_middleware = GoogleAuthMiddleware()

async def get_current_user(request: Request) -> Optional[dict]:
    user = await auth_middleware.authenticate(request)
    print('user', user)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Not authenticated"
        )
    return user