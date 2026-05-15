from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, field_validator
from app.schemas.employee import EmployeeResponse


class DepartmentCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    parent_id: int | None = None

    @field_validator("name", mode="before")
    @classmethod
    def strip_name(cls, v:str) -> str:
        if isinstance(v, str):
            v = v.strip()
        if not v:
            raise ValueError("name cannot be empty or whitespace")
        return v


class DepartmentUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=200)
    parent_id: int | None = None

    @field_validator("name", mode="before")
    @classmethod
    def strip_name(cls, v: str | None) -> str | None:
        if isinstance(v, str):
            v = v.strip()
        if not v:
            raise ValueError("name cannot be empty or whitespace")
        return v


class DepartmentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    parent_id: int | None
    created_at: datetime


class DepartmentDetail(BaseModel):
    employees: [list[EmployeeResponse], Field(default_factory=list)]
    children: [list["DepartmentDetail"], Field(default_factory=list)]

DepartmentDetail.model_rebuild()
