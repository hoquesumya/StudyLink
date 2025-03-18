from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn, logging, sys,  uuid, google, secrets
from google.cloud.logging_v2.handlers import CloudLoggingHandler
from app.routers import stydylinkcompo
from jose import jwt, JWTError
from fastapi.responses import JSONResponse
SECRET_KEY = secrets.token_urlsafe(32)
ALGORITHM = "HS256"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
#formatter_cloud = cloud_logger.Formatter(fmt="%(asctime)s - %(levelname)s - %(message)s")
formatter = logging.Formatter(fmt="%(asctime)s - %(levelname)s - %(message)s")

stream_handler = logging.StreamHandler(sys.stdout)
error_handler = logging.FileHandler('composite.log')

stream_handler.setFormatter(formatter)
error_handler.setFormatter(formatter)

logger.handlers=[stream_handler,error_handler]

client = google.cloud.logging.Client()
handler = CloudLoggingHandler(client)

cloud_logger = logging.getLogger('cloudLogger')
cloud_logger.setLevel(logging.INFO)
cloud_logger.addHandler(handler)

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Your React app's URL
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
    expose_headers=["*"]

)
@app.middleware("http")
async def log_middleware(request: Request, call_next):

    correlation_id = request.headers.get('Correlation-ID', str(uuid.uuid4()))
    request.state.correlation_id = correlation_id
    log_dict = {
        'X-Correlation-ID':correlation_id,
        'url': request.url.path, 
        'method': request.method
    }
    logger.info(log_dict)
    cloud_logger.info(log_dict)
    response =  await call_next(request)
    response.headers["Correlation-ID"] = correlation_id
    return response

@app.middleware("http")
async def authentication_middleware(request:Request, call_next):
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith("Bearer "):
        return JSONResponse(status_code=401, content={"detail": "Authorization header missing or invalid"})
    token = auth_header.split("Bearer ")[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        request.state.user = payload  # Attach user info to the request
    except JWTError:
        return JSONResponse(status_code=401, content={"detail": "Invalid or expired token"})

    return await call_next(request)

app.include_router(stydylinkcompo.router)

@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)