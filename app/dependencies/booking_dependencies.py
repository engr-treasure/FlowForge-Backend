from fastapi import Depends, HTTPException
from app.models.booking import Bookings, BookingEquipment
from app.models.user import Users
from app.models.equipment import Equipments
from app.databases.database import get_db
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.core.enums import BookingStatus, EquipmentOperationalStatus

def validate_booking(
    equipment_ids: list[int],
    new_start_time: datetime,
    new_end_time: datetime,
    db: Session = Depends(get_db)
):
    if new_start_time >= new_end_time:
        raise HTTPException(
            status_code=400,
            detail="End time must be after start time"
        )

    equipment_ids = list(set(equipment_ids))

    equipment_list = (
        db.query(Equipments)
        .filter(
            Equipments.id.in_(equipment_ids)
        )
        .all()
    )

    if len(equipment_list) != len(equipment_ids):
        raise HTTPException(
            status_code=404,
            detail="One or more equipment were not found"
        )

    for equipment in equipment_list:
        if equipment.status in {
            EquipmentOperationalStatus.UNAVAILABLE,
            EquipmentOperationalStatus.MAINTENANCE,
            EquipmentOperationalStatus.RETIRED
        }:
            raise HTTPException(
                status_code=400,
                detail=(
                    f"Equipment '{equipment.name}' "
                    f"is not available"
                )
            )
    
    existing_booking = (
        db.query(Bookings)
        .join(
            BookingEquipment,
            BookingEquipment.booking_id == Bookings.id
        )
        .filter(
            BookingEquipment.equipment_ids == equipment.id,
            # Existing booking starts before the new booking ends
            Bookings.start_time < new_end_time,
            # Existing booking + rest period extends beyond the new start
            (
                Bookings.end_time
                + timedelta(minutes=equipment.rest_duration)
            ) > new_start_time,
            Bookings.status.in_([
                BookingStatus.PENDING,
                BookingStatus.CONFIRMED
            ])
        )
        .first()
    )

    if existing_booking:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Equipment '{equipment.name}' "
                f"is already booked for this period"
            )
        )

    return True

def validate_booking_id(
    booking_id: int,
    db: Session = Depends(get_db)
):
    valid = db.query(Bookings).filter_by(id==booking_id).first()
    if not valid:
        raise HTTPException(
            status_code=404,
            detail="Equipment does not exist"
        )
    return valid