from pydantic import BaseModel, ConfigDict, Field, field_validator, EmailStr
from datetime import datetime
import re

class AddCustomer(BaseModel):
    first_name: str = Field(
        max_length=50
    )
    last_name: str = Field(
        max_length=50
    )
    email: EmailStr
    phone_number: str

    @field_validator("email")
    @classmethod
    def validate_email(cls, value):
        return value.strip().lower()

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, value):
        value = re.sub(r"[\s-()]+", "", value)
        phone_number_format = r"^(\+234|234|0)[789][01]\d{8}$"
        if not re.match(phone_number_format, value):
            raise ValueError("Invalid phone number")
        return value
    
class UpdateCustomer(BaseModel):
    id: int | None = Field(
        default=None,
        ge=1
    )
    first_name: str | None = Field(
        default=None,
        max_length=50
    )
    last_name: str | None = Field(
        default=None,
        max_length=50
    )
    email: EmailStr | None = None
    phone_number: str | None = None

    @field_validator("email")
    @classmethod
    def validate_email(cls, value):
        return value.strip().lower()

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, value):
        value = re.sub(r"[\s-()]+", "", value)
        phone_number_format = r"^(\+234|234|0)[789][01]\d{8}$"
        if not re.match(phone_number_format, value):
            raise ValueError("Invalid phone number")
        return value

class CustomerResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    phone_number: str
    created_at: datetime
    updated_at: datetime
    model_config=ConfigDict(from_attributes=True)

class CustomerListResponse(BaseModel):
    items: list[CustomerResponse]
    page: int
    limit: int
    total: int
    pages: int