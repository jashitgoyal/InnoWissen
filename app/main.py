# from fastapi import FastAPI
# from app.routes import interview
# app = FastAPI(title="Voice Interview Bot API",
#     description="Backend APIs for 2-way voice interview assistant using GCP & FastAPI.",
#     version="1.0.0")



from fastapi import FastAPI
from app.routes import teams  # 👈 Import your teams router

app = FastAPI()

# Include Teams router
app.include_router(teams.router, prefix="/api")



# app.include_router(interview.router)
