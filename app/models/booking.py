from datetime import datetime, timezone
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy import Column, String, Integer, ForeignKey, Time, Enum as SQLEnum, Date, DateTime, Text
from sqlalchemy.orm import relationship
from app.databases.database import Base
from app.core.enums import BookingStatus

class Bookings(Base):
    __tablename__ = "bookings"
    id = Column(Integer, index=True, primary_key=True)
    staff_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    staff = relationship(
        "Users",
        back_populates="booking"
    )
    booking_equipments = relationship(
        "BookingEquipments",
        back_populates="booking",
        cascade="all, delete-orphan"
    )
    equipments = association_proxy(
        "BookingEquipments",
        "equipment"
    )
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=True)
    customer = relationship(
        "Customers",
        back_populates="bookings"
    )
    purpose_of_booking = Column(Text, nullable=False)
    start_time = Column(DateTime(timezone=True), nullable=False)
    end_time = Column(DateTime(timezone=True), nullable=False)
    notes = Column(Text, nullable=True)
    approved_or_rejected_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    approved_or_rejected_date = Column(DateTime(timezone=True), nullable=True)
    rejection_reason = Column(Text, nullable=True)
    status = Column(
        SQLEnum(BookingStatus),
        nullable=False
    )
    created_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc), nullable=False)

class BookingEquipment(Base):
    __tablename__ = "booking_equipment"

    id = Column(Integer, primary_key=True)

    booking_id = Column(
        Integer,
        ForeignKey("bookings.id"),
        nullable=False
    )
    booking = relationship(
            "Bookings",
            back_populates="booking_equipment"
        )
    equipment_ids = Column(
        Integer,
        ForeignKey("equipments.id"),
        nullable=False
    )
    equipment = relationship(
        "Equipments",
        back_populates="booking"
    )