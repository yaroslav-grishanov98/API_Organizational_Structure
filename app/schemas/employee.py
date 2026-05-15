from datetime import datetime, date
from pydantic import BaseModel, ConfigDict, Field


class EmployeeCreate(BaseModel):
    full_name: str = Field(..., min_length=1, max_length=200)
    position: str = Field(..., min_length=1, max_length=200)
    hired_at: date | None = None


class EmployeeUpdate(BaseModel):
    full_name: str | None = Field(None, min_length=1, max_length=200)
    position: str | None = Field(None, min_length=1, max_length=200)
    hired_at: date | None = None


class EmployeeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    department_id: int
    full_name: str
    position: str
    hired_at: date | None
    created_at: datetime
