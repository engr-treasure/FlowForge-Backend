from pydantic import BaseModel, field_validator, Field, model_validator, ConfigDict, EmailStr
from datetime import date
from datetime import datetime
import re
from app.core import enums
from app.schemas.company import JobResponse, DepartmentResponse

class Register(BaseModel):
    role: enums.Roles
    first_name: str = Field(
        min_length=2,
        max_length=30
    )
    last_name: str = Field(
        min_length=2,
        max_length=30
    )
    email: EmailStr | None = None
    phone_number: str
    street_address: str = Field(
        max_length=200
    )
    city: str
    state: str
    country: str
    job_id: int = Field(
        ge=1
    )
    employment_status: enums.EmploymentStatus
    password: str
    repeat_password: str
    join_date: date = Field(
        default_factory=date.today,
        description="Date the staff member joined the company"
    )

    @field_validator("first_name", "last_name")
    @classmethod
    def clean_first_name(cls, value):
        return value.strip().title()

    @field_validator("email")
    @classmethod
    def clean_email(cls, value):
        if value is None:
            return value
        return value.lower().strip()

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, value) -> str:
        value = re.sub(r"[\s\-()]+", "", value) #value.replace(" ", "").replace("-", "")
        nigerian_phone_regex = r"^(\+234|234|0)[789][01]\d{8}$"
        if not re.match(nigerian_phone_regex, value):
            raise ValueError(
                "Invalid phone number"
            )       
        return value
        
    @field_validator("password")
    @classmethod
    def validate_password_format(cls, value) -> str:
        password_format = r"(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[^A-Za-z0-9]).{8,}"
        if " " in value:
            raise ValueError(
                "Password cannot contain spaces"
            )       
        if not re.fullmatch(password_format, value):
            raise ValueError(
                "Invalid password"
            )       
        return value 

    @model_validator(mode="after")
    def validate_password(self):
        if self.password != self.repeat_password:
            raise ValueError("Passwords do not match")
        return self  
    
class RegistrationResponse(BaseModel):
    staff_id: str
    id: int
    model_config=ConfigDict(from_attributes=True)

class Login(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str

class UserLookup(BaseModel):
    staff_id: str

    @field_validator("staff_id")
    @classmethod
    def validate_user_id(cls, value):
        id_format = r"^STF\d{2}\d{3}$"
        if not re.match(id_format, value):
            raise ValueError("Invalid staff id")
        return value

class UpdateUser(BaseModel):
    roles: enums.Roles
    first_name: str | None = Field(
        default=None,
        min_length=2,
        max_length=30
    )
    last_name: str | None = Field(
        default=None,
        min_length=2,
        max_length=30
    )
    email: str | None
    phone_number: str | None
    street_address: str  | None
    city: str | None
    state: str | None
    country: str | None
    job_id: int | None = Field(
        default=None,
        ge=1
    )
    employment_status: enums.EmploymentStatus | None

    @field_validator("first_name", "last_name")
    @classmethod
    def clean_first_name(cls, value):
        return value.strip().title()

    @field_validator("email")
    @classmethod
    def clean_email(cls, value):
        if value is None:
            return value
        return value.lower().strip()

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, value) -> str:
        value = re.sub(r"[\s\-()]+", "", value) #value.replace(" ", "").replace("-", "")
        nigerian_phone_regex = r"^(\+234|234|0)[789][01]\d{8}$"
        if not re.match(nigerian_phone_regex, value):
            raise ValueError(
                "Invalid phone number"
            )       
        return value

class UserResponse(BaseModel):
    id: int
    staff_id: str
    first_name: str 
    last_name: str 
    email: str | None = None
    phone_number: str
    join_date: date
    job: JobResponse
    last_login: datetime
    model_config=ConfigDict(from_attributes=True)

class UserListResponse(BaseModel):
    items: list[UserResponse]
    page: int
    limit: int
    total: int
    pages: int