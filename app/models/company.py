from sqlalchemy import Column, String, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.databases.database import Base
from app.core import enums
from enum import Enum
from datetime import date

class Jobs(Base):
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    department_id = Column(ForeignKey("departments.id"))
    department = relationship(
        "Departments",
        back_populates="jobs"
    )
    staff = relationship(
        "Users",
        back_populates="job"
    )


class Departments(Base):
    __tablename__ = "departments"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    jobs = relationship(
        "Jobs",
        back_populates="department"
    )
    location_id = Column(
        Integer,
        ForeignKey("office_locations.id"),
        nullable=False
    )
    location = relationship(
        "OfficeLocations",
        back_populates="departments"
    )

class OfficeLocations(Base):
    __tablename__ = "office_locations"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    street_address = Column(String, nullable=False)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    country = Column(String, nullable=False)
    departments = relationship(
        "Departments",
        back_populates="location"
    )