from fastapi import FastAPI, Request
import uuid
import sys
import time
import logging
from fastapi.middleware.cors import CORSMiddleware
from app.routers.user_router import router as user_router

app = FastAPI()

# GOOGLE CLOUD LOGGING
# TO DO - Connect logging to GCP console
# from google.cloud import logging as gcp_logging
# gcp_client = gcp_logging.Client()
# gcp_client.setup_logging()
# logging.info("Google Cloud Logging has been configured.")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

app.include_router(user_router)

# Basic logging for EC2 instance
logging.basicConfig(level=logging.INFO,
                    handlers=[
                        logging.StreamHandler(sys.stdout)  # Send logs to stdout
                    ])

@app.get("/")
async def root():
    return {"message": "User Service is running"}


@app.middleware("http")
async def log_requests(request: Request, call_next):
    trace_id = str(uuid.uuid4())  # Generate a unique trace ID for the request
    request.state.trace_id = trace_id
    logging.info(f"TRACE_ID={trace_id} - Incoming Request: {request.method} {request.url}")

    start_time = time.time()
    response = await call_next(request)
    processing_time = time.time() - start_time

    logging.info(
        f"TRACE_ID={trace_id} - Completed Request: {request.method} {request.url} "
        f"with Status {response.status_code} in {processing_time:.4f}s"
    )
    response.headers["X-Trace-Id"] = trace_id
    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)