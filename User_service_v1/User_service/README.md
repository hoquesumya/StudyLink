# User Profile Microservice

The user profile microservice is responsible for pulling user-specific information from Canvas API and the application database. 

When creating an account for StudyLink, the user authenticates their account via Google Login and a Canvas token. User information—full name, email address, enrolled courses, and pronouns—are retrieved from the user’s Canvas profile. As user profile information can be updated in Canvas, and active courses change every semester, the service updates this data accordingly. 

Upon signing up to the application, the user will receive an automatic email notification confirming they have signed up. This FaaS was implemented through Google Cloud Run Functions. The email is sent via an integration with SendGrid, which sends the user a dynamic email template, which updates based on the name of the new user.

## Create or Update Profile (POST)
```
POST /users/{user_id}/profile
curl -X POST "http://localhost:8000/users/{user_id}/profile" \
-H "Authorization: Bearer <JWT_TOKEN>" \ 
-H "Content-Type: application/json" \ 
-d '{ "token": "<PROFILE_TOKEN>" }'
```
Replace ```{user_id}``` with the user ID, ```<JWT_TOKEN>``` with the actual token, and ```<PROFILE_TOKEN>``` with the profile token.

## Get User Profile (GET)
```
GET /users/{user_id}/profile
curl -X GET "http://localhost:8000/users/{user_id}/profile" \
-H "Authorization: Bearer <JWT_TOKEN>"
```
Replace ```{user_id}``` and ```<JWT_TOKEN>``` with the user ID and token.


## Delete User Profile (DELETE)
```
DELETE /users/{user_id}/profile
curl -X DELETE "http://localhost:8000/users/{user_id}/profile" \
-H "Authorization: Bearer <JWT_TOKEN>"
```
Replace ```{user_id}``` and ```<JWT_TOKEN>``` with the user ID and token.

## Get Users List (GET)
```
GET /users
curl -X GET "http://localhost:8000/users?skip=0&limit=10&name=<NAME>&course=<COURSE>" \
-H "Authorization: Bearer <JWT_TOKEN>"
```
Replace ```<NAME>``` and ```<COURSE>``` with search parameters if needed. You can omit them for general listing. Replace ```<JWT_TOKEN>``` as required.

## User Login (GET)
```
GET /users/{user_id}/login
curl -X GET "http://localhost:8000/users/{user_id}/login" \
-H "Authorization: Bearer <JWT_TOKEN>"
```
Replace ```{user_id}``` and ```<JWT_TOKEN>``` with appropriate values.





