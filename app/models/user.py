from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Date
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import date, timezone
from app.databases.database import Base
from app.core import enums


class Users (Base):
    __tablename__="users"
    id = Column(Integer, primary_key=True, index=True)
    staff_id = Column(String, unique=True, nullable=True, index=True)
    role = Column(
        SQLEnum(enums.Roles),
        nullable=False
    )
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=True, unique=True)
    phone_number = Column(String, unique=True, nullable=False)
    street_address =  Column(String, nullable=False)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    country = Column(String, nullable=False)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)
    job = relationship(
        "Jobs",
        back_populates="staff"
    )
    employment_status = Column(SQLEnum(enums.EmploymentStatus), nullable=False)
    password_hash = Column(String, nullable=False)
    last_login = Column(DateTime(timezone=True), nullable=True)
    join_date = Column(Date, nullable=False, default=date.today)
    booking = relationship(
        "Bookings",
        back_populates="staff"
    )

