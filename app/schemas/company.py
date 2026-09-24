from pydantic import BaseModel, Field, ConfigDict
import re
from app.core import enums
from datetime import date

class AddJob(BaseModel):
    title: str
    description: str
    department_id: int = Field(
        ge=1
    )

class JobResponse(BaseModel):
    id: int
    title: str
    department: DepartmentResponse
    model_config=ConfigDict(from_attributes=True)

class AddDepartment(BaseModel):
    name: str
    description: str
    location_id: int = Field(
        ge=1
    )

class DepartmentResponse(BaseModel):
    id: int
    name: str
    location: OfficeLocationResponse
    model_config=ConfigDict(from_attributes=True)

class AddOfficeLocation(BaseModel):
    name: str
    street_address: str
    city: str
    state: str
    country: str

class OfficeLocationResponse(BaseModel):
    id: int
    name: str
    model_config=ConfigDict(from_attributes=True)