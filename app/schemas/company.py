from pydantic import BaseModel, Field, ConfigDict, field_validator
import re
from app.core import enums
from datetime import date

class AddJob(BaseModel):
    title: str = Field(
        max_length=50
    )
    description: str | None = Field(
        default=None,
        max_length=500
    )
    department_id: int = Field(
        ge=1
    )

class UpdateJob(BaseModel):
    title: str | None = Field(
        default=None,
        max_length=50
    )
    description: str | None = Field(
        default=None,
        max_length=500
    )
    department_id: int | None = Field(
        default=None,
        ge=1
    )

class JobResponse(BaseModel):
    id: int
    title: str
    department: DepartmentResponse
    model_config=ConfigDict(from_attributes=True)

class AddDepartment(BaseModel):
    name: str = Field(
        max_length=50
    )
    description: str | None = Field(
        default=None,
        max_length=500
    )
    location_id: int = Field(
        ge=1
    )

class UpdateDepartment(BaseModel):
    name: str | None = Field(
        default=None,
        max_length=50
    )
    description: str | None = Field(
        default=None,
        max_length=500
    )
    location_id: int | None = Field(
        default=None,
        ge=1
    )

class DepartmentResponse(BaseModel):
    id: int
    name: str
    location: OfficeLocationResponse
    model_config=ConfigDict(from_attributes=True)

class AddOfficeLocation(BaseModel):
    name: str = Field(
        max_length=50
    )
    street_address: str = Field(
        max_length=200
    )
    city: str
    state: str
    country: str

class UpdateOfficeLocation(BaseModel):
    name: str | None = Field(
        default=None,
        max_length=50
    )
    street_address: str | None = Field(
        default=None,
        max_length=200
    )
    city: str | None = None
    state: str | None = None
    country: str | None = None

class OfficeLocationResponse(BaseModel):
    id: int
    name: str
    model_config=ConfigDict(from_attributes=True)

class CompanyLookup(BaseModel):
    id: int = Field(
        ge=1
    )