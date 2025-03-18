from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import students, courses
import logging
from logging.handlers import RotatingFileHandler

"""
    Group Project for Cloud Computing Course!!
    
"""

logging.basicConfig(
    handlers=[RotatingFileHandler('/var/log/course-enrollment.log', maxBytes=100000, backupCount=5)],
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
)

logger = logging.getLogger(__name__)

app = FastAPI()

# Enable CORS for development purposes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Your React app's URL
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
    expose_headers=["*"]
)

# Include the routes from the students and courses routers
app.include_router(students.router)
app.include_router(courses.router)

@app.get("/")
async def root():
    return {"message": "Course Enrollment Microservice is Running!"}

@app.middleware("http")
async def log_requests(request, call_next):
    logger.info(f"Request path: {request.url.path} - Correlation-ID: {request.headers.get('X-Correlation-ID', 'Not provided')}")
    response = await call_next(request)
    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
