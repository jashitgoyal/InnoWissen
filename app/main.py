from fastapi import FastAPI
from app.routes import interview

app = FastAPI(title="Voice Interview Bot API",
    description="Backend APIs for 2-way voice interview assistant using GCP & FastAPI.",
    version="1.0.0")

app.include_router(interview.router)
