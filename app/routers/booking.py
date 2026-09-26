from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.schemas.booking import BookingResponse, BookingListResponse, CreateBooking, UpdateBooking
from app.databases.database import get_db
from app.dependencies import permissions, user_dependencies
from app.dependencies.booking_dependencies import validate_booking,  validate_booking_id
from app.models.user import Users
from app.models.equipment import Equipments
from app.models.booking import Bookings, BookingEquipment
from datetime import datetime, timezone
import math

router = APIRouter(
    prefix="/bookings",
    tags=["booking"]
)

@router.post("/create-booking", response_model=BookingResponse, status_code=201)
def create_booking(
    db: Session = Depends(get_db),
    booking = CreateBooking,
     _: Users = Depends(permissions.require_admin),
    __: Users = Depends(permissions.allow_active_staff)
):
    staff = user_dependencies.get_user_by_staff_id(booking.staff_id)
    if not staff:
        raise HTTPException(
            status_code=404,
            detail="Staff not found"
        )
    validate_booking(booking.equipment_id, booking.start_time, booking.endtime)
    
    new_booking = Bookings(
        staff_id = booking.staff_id,
        customer_id = booking.customer_id,
        purpose_of_booking = booking.purpose_of_booking,
        start_time = booking.start_time,
        end_time = booking.end_time,
        notes = booking.notes,
        approved_or_rejected_by = booking.approved_or_rejected_by,
        approved_or_rejected_date = booking.approved_or_rejected_date,
        rejection_reason = booking.rejection_reason,
        status = booking.status
    )
    db.add(new_booking)
    db.flush()
    for equipment in booking.equipment_ids:
        new_booking_equipment = BookingEquipment(
            booking_id = new_booking.id,
            equipment_ids = equipment
        )
        db.add(new_booking_equipment)

    db.commit()
    db.refresh(new_booking)
    return new_booking

@router.get("/", response_model=BookingListResponse)
def get_bookings(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    __: Users = Depends(permissions.allow_active_staff)
):
    total = db.query(Bookings).count()
    pages = math.ceil(total/limit)
    offset = (page - 1) * limit
    bookings = db.query(Bookings).order_by(Bookings.created_at.desc()).offset(offset).limit(limit).all()
  
    return bookings


@router.get("/{id}", response_model=BookingResponse)
def get_booking_by_id(
    booking: Bookings = Depends(validate_booking_id),
    _: Users = Depends(permissions.require_admin_or_manager),
    __: Users = Depends(permissions.allow_active_staff)
):
    return booking

@router.patch("/{id}", response_model=BookingResponse)
def update_booking(
    update_details: UpdateBooking,
    verified_booking: Bookings = Depends(validate_booking_id),
    db: Session = Depends(get_db),
    _: Users = Depends(permissions.require_admin),
    __: Users = Depends(permissions.allow_active_staff)
):
    updated = update_details.model_dump(exclude_unset=True)
    updated["updated_at"] = datetime.now(timezone.utc)
    for key, value in updated.items():
        setattr(verified_booking, key, value)

     # Update booking equipment
    if update_details.equipment_ids is not None:

        equipment_ids = list(dict.fromkeys(update_details.equipment_ids))

        # Check that all equipment exist
        equipments = (
            db.query(Equipments)
            .filter(Equipments.id.in_(equipment_ids))
            .all()
        )

        if len(equipments) != len(equipment_ids):
            raise HTTPException(
                status_code=404,
                detail="One or more equipment were not found"
            )

        # Check equipment availability
        validate_booking(
            equipment_ids,
            verified_booking.start_time,
            verified_booking.end_time,
            db
        )

        # Remove existing equipment from this booking
        db.query(BookingEquipment).filter(
            BookingEquipment.booking_id == verified_booking.id
        ).delete(
            synchronize_session=False
        )

        # Add the new equipment
        for equipment_id in equipment_ids:
            db.add(
                BookingEquipment(
                    booking_id=verified_booking.id,
                    equipment_id=equipment_id
                )
            )
                
    db.commit()
    db.refresh(verified_booking)
    return verified_booking

@router.delete("/{id}", response_model=BookingResponse)
def delete_booking(
    booking: Bookings = Depends(validate_booking_id),
    db: Session = Depends(get_db),
    _: Users = Depends(permissions.require_admin),
    __: Users = Depends(permissions.allow_active_staff)
):
    db.delete(booking)
    db.commit()
    return booking