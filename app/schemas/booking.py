from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from app.core.enums import BookingStatus
from app.schemas import user, customer, equipment

class CreateBooking(BaseModel):
    staff_id: int = Field(
        ge=1
    )
    equipment_id: list[int]  = Field(
        min=1
    )
    customer_id: int | None = Field(
        default=None,
        ge=1
    )
    purpose_of_booking: str = Field(
        max_length=100
    )
    start_time: datetime
    end_time: datetime
    notes: str | None = Field(
        default=None,
        max_length=200
    )
    approved_or_rejected_by: int
    approved_or_rejected_date: datetime
    rejection_reason: str | None = Field(
        default=None,
        max_length=100
    )
    status: BookingStatus

class UpdateBooking(BaseModel):
    staff_id: int | None = Field(
        default=None,
        ge=1
    )
    equipment_ids: list[int] | None = Field(
        default=None,
        min_length=1
    )
    customer_id: int | None = Field(
        default=None,
        ge=1
    )
    purpose_of_booking: str | None = Field(
        default=None,
        max_length=100
    )
    start_time: datetime | None = None
    end_time: datetime | None = None
    notes: str | None = Field(
        default=None,
        max_length=200
    )
    approved_or_rejected_by: int | None = None
    approved_or_rejected_date: datetime | None = None
    rejection_reason: str | None = Field(
        default=None,
        max_length=100
    )
    status: BookingStatus | None = None

class BookingResponse(BaseModel):
    staff: user.UserResponse
    equipments: list[equipment.EquipmentResponse]
    customer: customer.CustomerResponse
    purpose_of_booking: str
    start_time: datetime
    end_time: datetime
    notes: str | None = None
    approved_or_rejected_by: int
    approved_or_rejected_date: datetime
    rejection_reason: str
    status: BookingStatus
    created_at: datetime
    updated_at: datetime
    model_config=ConfigDict(from_attributes=True)

class BookingListResponse(BaseModel):
    items: list[BookingResponse]
    page: int
    limit: int
    total: int
    pages: int