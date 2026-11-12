from pydantic import BaseModel, Field


class ProjectGet(BaseModel):
    id: int
    name: str


class ProjectCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)


class ProjectUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
