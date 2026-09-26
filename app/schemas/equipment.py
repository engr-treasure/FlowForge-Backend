from pydantic import BaseModel, Field, field_validator, ConfigDict
from datetime import date, datetime
from app.core.enums import EquipmentCategories, EquipmentOperationalStatus, ApprovalRequirements
from app.schemas.company import OfficeLocationResponse

class AddEquipment(BaseModel):
    name: str = Field(
        max_length=50
    )
    description: str = Field(
        max_length=200
    )
    category: EquipmentCategories
    location_id: int = Field(
        ge=1
    )
    serial_number: str
    manufacturer: str = Field(
        max_length=50
    )
    model: str = Field(
        max_length=50
    )
    quantity: int = Field(
        ge=1
    )
    approval: ApprovalRequirements
    date_acquired: date = Field(
        default_factory=date.today
    )
    rest_duration: int = Field(
        ge=10
    ) #minutes
    status: EquipmentOperationalStatus

    @field_validator("name", "manufacturer", "model")
    @classmethod
    def clean_equipment_name(cls, value: str) -> str :
        return value.strip().title()
    
    @field_validator("serial_number")
    @classmethod
    def clean_equipment_serial_number(cls, value: str) -> str :
        return value.strip().upper()
    
class UpdateEquipment(BaseModel):
    name: str | None = Field(
        default=None,
        max_length=50
    )
    description: str | None = Field(
        default=None,
        max_length=200
    )
    category: EquipmentCategories | None = None
    location_id: int | None = Field(
        default=None,
        ge=1
    )
    serial_number: str | None = None
    manufacturer: str | None = Field(
        default=None,
        max_length=50
    )
    model: str | None = Field(
        default=None,
        max_length=50
    )
    quantity: int | None = Field(
        default=None,
        ge=1
    )
    approval: ApprovalRequirements | None = None
    rest_duration: int | None = Field(
        default=None,
        ge=10
    ) #minutes
    status: EquipmentOperationalStatus | None = None

    @field_validator("name", "manufacturer", "model")
    @classmethod
    def clean_equipment_name(cls, value: str) -> str :
        return value.strip().title()
    
    @field_validator("serial_number")
    @classmethod
    def clean_equipment_serial_number(cls, value: str) -> str :
        return value.strip().upper()

class EquipmentResponse(BaseModel):
    id: int
    name: str
    description: str
    category: EquipmentCategories
    location: OfficeLocationResponse
    serial_number: str
    manufacturer: str
    model: str
    quantity: int
    approval: ApprovalRequirements
    rest_duration: int
    date_aquired: int
    model_config=ConfigDict(from_attributes=True)
    created_at: datetime
    updated_at: datetime

class EquipmentListResponse(BaseModel):
    items: list[EquipmentResponse]
    page: int
    limit: int
    total: int
    pages: int

class EquipmentLookup(BaseModel):
    id: int = Field(
        ge=1
    )