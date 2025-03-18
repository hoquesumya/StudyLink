# COMS-4153-Project-composite-microservice
## User Service
- Get /StudyLink/v1/users/{user_id}/login  → call the user microservice logging endpoint
- Get  /StudyLink/v1/users/{user_id}/profile → get request, has jwt and google token as a header, pass along to the user service to verify
- Post /StudyLink/v1/users/{user_id}/profile → post request, has query parameters canvas token
- Delete /StudyLink/v1/users/{user_id}/profile → delete request, has  jwt and google token as a header, pass along to the user service to verify
- Get /StudyLink/v1/users/ → retriever all users along with jwt and google token as the header

## Study Service
- Get /StudyLink/v1/study-group/{group_id}  → get request to the study-group microservice
- Get /StudyLink/v1/study-group/" → get a request to the study-group microservice (retrieve all group)
- Post /StudyLink/v1/{user_id}/study-group/ → asynchronous post request to user service + study-group + - perform rollback operation if the post is successful but the get is not successful
- Delete /StudyLink/v1/{user_id}/study-group/{group_id} → synchronous call to user service + study-group to delete a group
- Put /StudyLink/v1/{user_id}/study-group/{group_id}" → synchronous call to user service + study-group to update a group

## Course Enrollment
Two get requests to retrieve a student's courses and find students of the course

## Chat Service
- Post /StudyLink/v1/{user_id}/conversations → post a chat; --> Has choreography pattern to call the user and chat service. Used FaaS to act as the subscriber + publisher. FaaS is triggered wby the cloud pub-sub events.
    - ![Pub Sub Implementations!](/imgaes/pub-sub.png)

- Delete "/StudyLink/v1/{user_id}/conversations/{conversation_id}", → Has google workflow to call the user and chat services
- Put /StudyLink/v1/conversations/{conversation_id} → Synchronous call between the user and chat service
- Get StudyLink/v1/{user_id}/conversations/{conversation_id} → Retrieves conversation
- Get /StudyLink/v1/conversations → Get all the conversations

## Run App
uvicorn app.main:app --reload --port 8000
## To create the google Workflow follow the below link:
    https://cloud.google.com/workflows/docs/
## To Deploy app in PaaS
    1. install gcloud
    2. create app.yaml 
    3. gcloud app deploy
    4. gcloud app browse
    5. gcloud app logs tail -s default  

## FaaS Deployment
Follow this: https://cloud.google.com/functions/docs/tutorials/pubsub to trigeer the FaaS from cloud event e.g, pub-sub
 gcloud functions deploy python-pubsub-function --gen2 --runtime=python312 --region=? --source=app/pub-sub/ --entry-point=subscribe --trigger-topic=?
 To read the log: gcloud functions logs read  --gen2 --region=? --limit=5 python-pubsub-function

## MiddleWares
The middleware handles logging with a correlation ID and forwards logs to Google Cloud Logging; similarly, it validates JWT tokens.