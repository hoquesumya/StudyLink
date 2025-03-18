# COMS-4153-Project-CourseEnrollment-Microservice

Course Enrollment microservice application part of COMS-4153-Project for W4153 Cloud Computing.

**Functionality (FastAPI)**
-  Get courses for student: 
   `curl -X 'GET' \ 'http://35.174.4.121:8000/users/<uni>/courses' \
   -H 'accept: application/json' \
   -H 'token: <*courseworks token without quotes>’`
- Get students in course: 
  `curl -X ‘GET'\'http://35.174.4.121:8000/course/<*coursecode>
  /students' \ 
  -H 'accept: application/json' \ 
  -H 'token: <*courseworks token without quotes>'`

   -- *courseworks token = token generated from courseworks that allows       
     us to access student’s profile*<br>
   -- *coursecode = code of the form: "COMSW4153_001_2024_3"*

**Functionality**
- Communicates with Courseworks via API
- Searches through student’s current, active courses
- Communicates with other Microservices
- “Deployed on Commit” through GitHub

**Middleware and Logging:**
- Uses CloudWatch for logging
- try `sudo tail -f /var/log/course-enrollment.log` on the EC2 instance to
  view the logs as well
