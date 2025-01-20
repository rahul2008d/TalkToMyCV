from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(title="TalkToMyCV")

# Include routes
app.include_router(router)
