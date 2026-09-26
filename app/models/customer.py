from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.databases.database import Base


class Customers (Base):
    __tablename__="customers"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=True, unique=True)
    phone_number = Column(String, unique=True, nullable=False)
    bookings = relationship(
        "Bookings",
        back_populates="customer"
    )
    created_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc), nullable=False)

