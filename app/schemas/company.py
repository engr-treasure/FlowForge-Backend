from pydantic import BaseModel, Field, ConfigDict, field_validator
import re
from datetime import date
from app.core import enums

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

    @field_validator("title")
    @classmethod
    def clean_job_title(cls, value):
        return value.strip().title()

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

    @field_validator("title")
    @classmethod
    def clean_job_title(cls, value):
        return value.strip().title()

class JobResponse(BaseModel):
    id: int
    title: str
    department: DepartmentResponse
    model_config=ConfigDict(from_attributes=True)

class JobListResponse(BaseModel):
    items: list[JobResponse]
    page: int
    limit: int
    total: int
    pages: int

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

    @field_validator("name")
    @classmethod
    def clean_department_name(cls, value):
        return value.strip().title()

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

    @field_validator("name")
    @classmethod
    def clean_department_name(cls, value):
        return value.strip().title()

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

    @field_validator("name")
    @classmethod
    def clean_office_location_name(cls, value):
        return value.strip().title()

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
    
    @field_validator("name")
    @classmethod
    def clean_office_location_name(cls, value):
        return value.strip().title()

class OfficeLocationResponse(BaseModel):
    id: int
    name: str
    model_config=ConfigDict(from_attributes=True)

class CompanyLookup(BaseModel):
    id: int = Field(
        ge=1
    )