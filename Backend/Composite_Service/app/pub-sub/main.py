import base64, json, requests, os
from requests.exceptions import HTTPError, RequestException
from google.cloud import pubsub_v1
from cloudevents.http import CloudEvent
import functions_framework

def post_chat(conversation:dict):
        chat_config = os.environ.get("CHAT")
        url = f"{chat_config}/conversations/"
        try:
            response = requests.post(url, json=conversation, timeout=10)
            response.raise_for_status()
            return (response.json(), response.status_code)
       
        except requests.exceptions.Timeout:
            print("The request timed out!")
            return( {"error": "The request timed out"}, 408
            )
        except HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            return (response.json(), response.status_code)
def get_user(user_id:str, google:str, jwt_payload:str):
        user_config = os.environ.get("USER_URL")
        print(user_config)
        url = f"{user_config}/users/{user_id}/profile"
        try:
            
            print(google, jwt_payload)
            payload = { "Google-Token": google, 
                       "Authorization": jwt_payload}
            print("calling get user",google)
            response = requests.get(url, headers=payload, timeout=10)
            response.raise_for_status()
            
            return (response.json(), response.status_code)
        except requests.exceptions.Timeout:
            print("The request timed out!")
            return (
                {"error": "The request timed out"},408
            )
        except HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            try:
            # Try to parse the response as JSON
                response_data = response.json()  # This is from the external service
                print(f"External service response (JSON): {response_data}")
            except ValueError:
            # If it's not JSON, log the raw text response
             response_data = response.text
            print(f"HTTP errors occurred: {http_err}", response.status_code, response_data)
            return (response_data, response.status_code)
# Triggered from a message on a Cloud Pub/Sub topic.
@functions_framework.cloud_event
def subscribe(cloud_event: CloudEvent) -> None:
    # Print out the data from Pub/Sub, to prove that it worked
        # Decode the Pub/Sub message

        decoded_message = base64.b64decode(cloud_event.data["message"]["data"]).decode("utf-8")
        # Split lines to extract key-value pairs
       
        try:
            message_data = json.loads(decoded_message)
            # Extract the relevant fields
            user_id = message_data.get('user_id', '')
            google_user = message_data.get('google_user', '')
            jwt = message_data.get('jwt', '')
            conversation = message_data.get('conversation', {})
            

            response, status = get_user(user_id, google_user, jwt)
            print(response, status)
            publisher = pubsub_v1.PublisherClient()
        # The `topic_path` method creates a fully qualified identifier
        # in the form `projects/{project_id}/topics/{topic_id}`
            project_id = os.environ.get("PROJECT")
            topic_id = os.environ.get("TOPIC_USER_CHAT")
            topic_path = publisher.topic_path(project_id, topic_id)
            
            element_http = {
                 "response": response,
                 "status": status
            }
            if status == 200 or status == 201:
                response, status = post_chat(conversation)
                element_http = {
                    "response": response,
                    "status": status
                }
            
            json_string = json.dumps(element_http)
            data = json_string.encode("utf-8")
            future = publisher.publish(topic_path, data)
            print(future.result())  
            
        
        except json.JSONDecodeError as e:
             print(f"Error decoding JSON: {e}")