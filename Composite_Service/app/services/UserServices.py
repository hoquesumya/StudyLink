from app.services.service_factory import ServiceFactory
from fastapi.responses import JSONResponse
from fastapi import HTTPException
class UserService:
    def __init__(self) -> None:
        service = ServiceFactory()
        self.compo_resource = service.get_service("CompositeResource")
    
    def get_user_login(self, user_id:str, google_user:str):
        print("let me check the google user login")
        data, status = self.compo_resource.get_user_login(user_id, google_user)
        if status == 200:
                return data
        else:
                raise HTTPException(status_code=status, detail=data)
        
    def get_user(self, user_id:str, google_user:str, jwt_payload:str):
            print("calling the function for use ")
            data, status = self.compo_resource.get_user(user_id, google_user, jwt_payload)
            if status == 200:
                return data
            else:
                raise HTTPException(status_code=status, detail=data)

    def get_all_users(self, google_user:str,jwt_payload:str):
        data, status = self.compo_resource.get_all_users(google_user, jwt_payload)
        if status == 200:
             return data
        else:
            raise HTTPException(status_code=status, detail=data)

    def post_user(self, user_id: str, token:str, google_token:str):
        print("starting he request")
        data, status = self.compo_resource.post_user(user_id, token, google_token)
        if status == 200 or status == 201:
            return data
        else:
            raise HTTPException(status_code=status, detail=data)

    def delete_user(self, user_id: str, google_user:str, jwt_payload:str):
        data, status = self.compo_resource.delete_user(user_id, google_user, jwt_payload)
        print("from delete", data, status)
        if status == 200 or status == 201:
            return data
        else:
            raise HTTPException(status_code=status, detail=data)