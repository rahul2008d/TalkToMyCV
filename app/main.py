from fastapi import FastAPI, Request, Response
from app.api.resume import router as resume_router
from fastapi.middleware.cors import CORSMiddleware
from uuid import uuid4
from mangum import Mangum

app = FastAPI()

origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(resume_router, prefix="/resume", tags=["Resume"])


# Middleware to add a unique user_id cookie to each user
@app.middleware("http")
async def add_user_id_cookie(request: Request, call_next):
    user_id = request.cookies.get("user_id")
    if not user_id:
        user_id = str(uuid4())  # Generate a new UUID
    request.state.user_id = user_id  # Store user_id in request state
    response = await call_next(request)
    if not request.cookies.get("user_id"):
        response.set_cookie(key="user_id", value=user_id)
    return response


handler = Mangum(app)
