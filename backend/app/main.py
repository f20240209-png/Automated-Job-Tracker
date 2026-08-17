from fastapi import FastAPI
import app.models  # noqa: F401
from app.routes import applications, jobs, auth

app = FastAPI(title="Job Application Tracker")

app.include_router(auth.router)
app.include_router(applications.router)
app.include_router(jobs.router)


@app.get("/")
def root():
    return {"message": "Job tracker API is running"}