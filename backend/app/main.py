from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import Base, engine
from .routers import auth, profile, applications
from .config import settings

import app.models  # ensure all models are registered before create_all

Base.metadata.create_all(bind=engine)

app = FastAPI(title="ATS API", version="1.0.0")

origins = (
    ["http://localhost:3000"]
    if settings.environment == "dev"
    else ["https://yourdomain.com"]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(profile.router)
app.include_router(applications.router)


@app.get("/health")
def health():
    return {"status": "ok", "environment": settings.environment}
