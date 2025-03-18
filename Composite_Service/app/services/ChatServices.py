from app.services.service_factory import ServiceFactory
from google.cloud.workflows.executions_v1.types import executions
from google.cloud.workflows import executions_v1

from google.cloud import workflows_v1
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from .pub_sub import Publisher, Subscriber
from dotenv import load_dotenv
import os, time, json
from .pub_sub_google import Publisher, Subscriber


class Chat:
    def __init__(self) -> None:
        service = ServiceFactory()
        self.compo_resource = service.get_service("CompositeResource")
    
    def get_chat(self, chat_id:int):
        data, status_code =  self.compo_resource.get_chat(chat_id)
        if status_code == 200:
            return data
        else:
            raise HTTPException(status_code=status_code, detail=data)
    
    def delete_chat_workflow(self, user_id: str,conversation_id:int, google_user:str, jwt_payload:str):
        load_dotenv()
        workflows_client = workflows_v1.WorkflowsClient()
        client = executions_v1.ExecutionsClient()
        project = os.getenv("PROJECT")
        location = os.getenv("LOCATION")
        workflow = os.getenv("WORKFLOW")
        parent = workflows_client.workflow_path(project, location, workflow)
        print(parent)
        service = ServiceFactory()
        config = service.get_service("CompositeResourceService")
        user_config = config.get_user_config()
        chat_config = config.get_chat_config()
        args = {
            
                "user_url": user_config,          # User service URL
                "user_id": user_id,                         # User ID
                "chat_url": chat_config,     # Chat service URL
                "chat_id": conversation_id,                         # Chat ID
                "google_token": google_user,        # Google token
                "authorization": jwt_payload   # Authorization header
            
        }
        argument_json = json.dumps(args)
        execution_request = executions_v1.CreateExecutionRequest(
            parent=parent,
            execution={
                "argument": argument_json
            }
        )
        
 
        response = client.create_execution(request=execution_request)
           
        print(f"Execution name: {response.name}")
        print(f"Execution State: {response.state}")
        execution_finished = False
        backoff_delay = 1  # Start wait with delay of 1 second
        print("Poll for result...")
        while not execution_finished:
            execution = client.get_execution(request={"name": response.name})
            execution_finished = execution.state != executions.Execution.State.ACTIVE

            # If we haven't seen the result yet, wait a second.
            if not execution_finished:
                print("- Waiting for results...")
                time.sleep(backoff_delay)
                # Double the delay to provide exponential backoff.
                backoff_delay *= 2
            else:
                print(f"Execution finished with state: {execution.state.name}")
                print(f"Execution results: {execution.result}")
                print(f"execution error {execution.error}")
                return execution

        
     

    def post_chat(self, user_id: str, conversation: dict, google_user:str, jwt_payload:str):

        print("started post service chat")
        '''
        
        pub = Publisher()
        user_sub = Subscriber("user_sub")
        chat_sub = Subscriber("chat_sub")
        compo_sub =  Subscriber("chat_response")
        
        pub.subscribe(user_sub, "get_user")
        pub.subscribe(chat_sub, "get_chat")
        pub.subscribe(compo_sub, "chat_response")
    
        pub.publish("Get User", "get_user", [user_id, google_user, jwt_payload])
        user_stat, response_data_get, status_code = user_sub.receive()

        #response_data_get, status_code = self.compo_resource.get_user(user_id,google_user)
        if not user_stat:
            raise HTTPException(status_code=status_code, detail=response_data_get)
       
        #if  status_code != 200:
            #raise HTTPException(status_code=status_code, detail=response_data_get)
       
        #this one works perfectly
        print("successful user")
        pub.publish("Get chat", "get_chat", [conversation])
        chat_stat, response_post, status_code = chat_sub.receive()
        if status_code != 200:
             raise HTTPException(status_code=status_code, detail=response_post)
        else:
            return JSONResponse(content={"detail": response_post}, status_code=200)

        '''
        '''
        
       
        response_post, status_code = self.compo_resource.post_chat(conversation)
        if status_code != 200:
            raise HTTPException(status_code=status_code, detail=response_post)
        else:
            print("chat created successfully")
            return JSONResponse(content={"detail": response_post}, status_code=200)
        '''

        http_data = {
            "user_id":user_id,
            "google_user": google_user,
            "jwt": jwt_payload,
            "conversation": conversation
        }
        pub = Publisher()
        pub.publish_message(http_data)
        sub = Subscriber()
        sub.subscribe()
        response, status = sub.get_response()
        return JSONResponse(content={"detail": response}, status_code=status)

    def delete_chat(self, user_id: str, chat_id:int, google_user:str, jwt_payload:str):
        
        response_data_get, status_code = self.compo_resource.get_user(user_id,google_user,jwt_payload)
       
        if  status_code != 200:
            raise HTTPException(status_code=status_code, detail=response_data_get)
        
        print("deleteing the chat")
        response_delete_data, status_code = self.compo_resource.delete_chat(chat_id)
        print(response_delete_data)
        if status_code != 201 or status_code!=200:
            raise HTTPException(status_code=status_code, detail=response_delete_data)
        else:
            return JSONResponse(content={"detail": response_delete_data}, status_code=200)
    
    def update_chat(self, user_id:str, chat_id:int, conversation:dict, google_user:str, jwt_payload:str):
        response_data_get, status_code = self.compo_resource.get_user(user_id,google_user, jwt_payload)
        if  status_code != 200:
            raise HTTPException(status_code=status_code, detail=response_data_get)
        response_put_data, status_code = self.compo_resource.update_chat(chat_id, conversation)
        print(status_code)
        if status_code != 200 :
            raise HTTPException(status_code=status_code, detail=response_put_data)
        else:
            return JSONResponse(content={"detail": response_put_data}, status_code=200)
    
    def get_all_chat(self):
       data, status_code = self.compo_resource.get_all_chat()
       if status_code == 200:
           return data
       raise HTTPException(status_code=status_code, detail=data)