from sqlalchemy import Column, String, Integer, Enum as SQLEnum, ForeignKey, Date, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import date, timezone, datetime
from app.core.enums import EquipmentCategories, EquipmentOperationalStatus, ApprovalRequirements
from app.databases.database import Base

class Equipments(Base):
    __tablename__="equipments"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    description = Column(Text, nullable=True)
    category = Column(SQLEnum(EquipmentCategories), nullable=False)
    location_id = Column(Integer, ForeignKey("office_locations.id"), nullable=False)
    location = relationship(
        "OfficeLocations",
        back_populates="equipments"
    )
    serial_number = Column(String, nullable=False)
    manufacturer = Column(String, nullable=False, index=True)
    Model = Column(String, nullable=True)
    quantity = Column(Integer, nullable=False)
    approval = Column(SQLEnum(ApprovalRequirements), nullable=False)
    date_acquired = Column(Date, nullable=False, default=date.today)
    created_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc), nullable=False)
    rest_duration = Column(Integer, nullable=False) #minutes
    status = Column(SQLEnum(EquipmentOperationalStatus), nullable=False)
    booking = relationship(
        "BookingEquipments",
        back_populates="equipment"
    )
