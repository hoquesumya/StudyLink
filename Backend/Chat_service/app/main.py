import uuid
from fastapi import Depends, FastAPI, Request
import logging
import uvicorn
import time
from app.routers import conversations
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware


app = FastAPI()


# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Your React app's URL
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
    expose_headers=["*"]
)

# Include routers
app.include_router(conversations.router)

@app.get("/")
async def root():
    return {"message": "Chat service running"}

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
    uvicorn.run(app, host="0.0.0.0", port=8080)