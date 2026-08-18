from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import app.models  # noqa: F401
from app.routes import applications, jobs, auth

app = FastAPI(title="Job Application Tracker")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten this to your Netlify URL once deployed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(applications.router)
app.include_router(jobs.router)


@app.get("/")
def root():
    return {"message": "Job tracker API is running"}