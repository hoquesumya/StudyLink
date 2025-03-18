import uuid
from fastapi import Depends, FastAPI, Request
import logging
import sys
# import watchtower
# import boto3
import time
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

from app.routers import study_group

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Your React app's URL
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
    expose_headers=["*"]
)

app.include_router(study_group.router)
logging.basicConfig(level=logging.INFO,
                    handlers=[
                        logging.StreamHandler(sys.stdout)  # Send logs to stdout
                    ])

# TODO: aws creds for cloudwatch
# boto3.setup_default_session(region_name="us-east-1")  # Replace with your region

# log_handler = watchtower.CloudWatchLogHandler(
#     log_group="study-groups-log",
#     stream_name="study-group-stream"
# )
# Add the CloudWatch log handler to the root logger
# logger = logging.getLogger(__name__)
# logger.setLevel(logging.INFO)
# logger.addHandler(log_handler)

@app.get("/")
async def root():
    return {"message": "Study Groups Service running"}

@app.middleware("http")
async def log_requests (request: Request, call_next):
    trace_id = str(uuid.uuid4())
    request.state.trace_id = trace_id  # Attach trace_id to request state for access within handlers
    logging.info(f"TRACE_ID={trace_id} - Incoming Request: {request.method} {request.url}")

    start_time = time.time()
    response = await call_next(request)
    processing_time = time.time() - start_time

    logging.info(
        f"TRACE_ID={trace_id} - Completed Request: {request.method} {request.url} "
        f"with Status {response.status_code} in {processing_time:.4f}s"
    )
    response.headers["X-Trace-Id"] = trace_id  # Include trace ID in response headers
    return response


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)



