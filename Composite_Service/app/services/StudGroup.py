from app.services.service_factory import ServiceFactory
from fastapi import HTTPException
from fastapi.responses import JSONResponse
import asyncio
class StudyGroup:
    def __init__(self) -> None:
        service = ServiceFactory()
        self.compo_resource = service.get_service("CompositeResource")
    
    def get_group(self, group_id:str):
        response_data, status_code = self.compo_resource.get_group(group_id)
        if status_code == 200:
            return response_data
        else:
           raise HTTPException(status_code=status_code, detail=response_data)
    
    def get_all_group(self):
        response_data, status_code = self.compo_resource.get_all_group()
        if status_code == 200:
            return response_data
        else:
           raise HTTPException(status_code=status_code, detail=response_data)
    #synchronoulsy runnnalble data
    
    async def create_group(self,  user_id:str, group_data:dict, google_user:str, jwt_payload:str):
        print("staring the create group ops")
        response_get, response_post = await asyncio.gather(
            self.compo_resource.get_user_sync_internal(user_id, google_user, jwt_payload), 
            self.compo_resource.create_group(group_data)
            )
        print(response_post)
        data, response_get_status =  response_get
        
        response_data, response_post_status=  response_post
       
        print(f"GET Response Status: {response_get_status}")
        print(f"POST Response Status: {response_post_status}")
    
    # Now handle the conditions based on the status codes
        if response_get_status == 200 and response_post_status != 200:
            raise HTTPException(status_code=response_post_status, detail=response_data)
       
        elif response_get_status == 200 and response_post_status == 200 or response_post_status == 201:
            return {"message": response_data}
        
        elif response_get_status != 200 and response_post_status == 200:
           
            group_id = response_data.get("group_id")
            response_delete_data, status_delete = await self.compo_resource.delete_group_async(group_id)

            if status_delete != 200:
                raise HTTPException(status_code=status_delete, detail=f"rollback failed,{response_delete_data}")
            
            raise HTTPException(status_code=400, detail="GET request failed, rollback succedded, Post Suspended")
        
        elif response_get_status != 200 and (response_post_status != 200  and response_post_status !=201):
            print("Both GET and POST requests failed.")
            raise HTTPException(status_code=response_post_status, detail=response_data)


    def delete_group(self, user_id:str, group_id: int, google_user:str, jwt_payload:str):
        #synchronous --> Structural coding pattern
        response_data_get, status_code = self.compo_resource.get_user(user_id,google_user, jwt_payload)
       
        if  status_code != 200:
            raise HTTPException(status_code=status_code, detail=response_data_get)
        
        response_data, status_code = self.compo_resource.delete_group(group_id)

        if  status_code != 200:
            raise HTTPException(status_code=400, detail=response_data)
        else:
            return response_data
    
    def update_group(self,user_id:str, group_id:int, update_data:dict, google_user:str, jwt_payload:str):
       
        response_data_get, status_code = self.compo_resource.get_user(user_id,google_user, jwt_payload)
       
        if  status_code != 200:
            raise HTTPException(status_code=status_code, detail=response_data_get)
    
        print("update data1", update_data)
        response_data, status_code = self.compo_resource.update_group(group_id, update_data)
       
        if status_code != 200:
           
            raise HTTPException(status_code=status_code, detail=response_data)
        else:
            return response_data
        
        
