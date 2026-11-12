from fastapi import FastAPI
from app.api.tasks import router as tasks_router
from app.api.projects import router as projects_router


app = FastAPI()

app.include_router(tasks_router)
app.include_router(projects_router)
