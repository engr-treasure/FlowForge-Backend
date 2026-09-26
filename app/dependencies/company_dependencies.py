from fastapi import Depends, HTTPException
from app.models.company import Jobs, OfficeLocations, Departments
from app.schemas.company import CompanyLookup
from app.databases.database import get_db
from sqlalchemy.orm import Session

def get_job_by_id(
    job_id: int,
    db: Session = Depends(get_db)
):
    job = db.query(Jobs).filter_by(id==job_id).first()
    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job does not exist"
        )
    return job

def get_department_by_id(
    department_id: int,
    db: Session = Depends(get_db)
):
    department = db.query(Departments).filter_by(id==department_id).first()
    if not department:
        raise HTTPException(
            status_code=404,
            detail="Department does not exist"
        )
    return department

def get_location_by_id(
    location_id: int,
    db: Session = Depends(get_db)
):
    location = db.query(OfficeLocations).filter_by(id==location_id).first()
    if not location:
        raise HTTPException(
            status_code=404,
            detail="Location does not exist"
        )
    return location