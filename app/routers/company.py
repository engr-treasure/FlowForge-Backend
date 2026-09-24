from fastapi import APIRouter, Depends, HTTPException
from app.databases.database import get_db
from sqlalchemy.orm import Session
from app.schemas import company
from app.models.user import Users
from app.models.company import Jobs, OfficeLocations, Departments
from app.dependencies import permissions

router = APIRouter(
    prefix="/company",
    tags=["company"]
)

@router.post("/add-job", response_model=company.JobResponse, status_code=201)
def AddJob(
    job: company.AddJob,
    db: Session = Depends(get_db),
    _: Users = Depends(permissions.require_admin)
):
    job_exists = db.query(Jobs).filter_by(title=job.title).first()

    if job_exists:
        raise HTTPException(
            status_code=400,
            detail="Job already exists"
        )        
    department_exists = db.query(Departments).filter_by(id=job.department_id).first()
    if not department_exists:
        raise HTTPException(
            status_code=404,
            detail="Department doesnt exist"
        )
    new_job = Jobs(
        title = job.title,
        description = job.description,
        department_id = job.department_id
    )

    db.add(new_job)
    db.commit()
    db.refresh(new_job)
    return new_job

@router.post("/add-department", response_model=company.DepartmentResponse, status_code=201)
def AddDepartment(
    department: company.AddDepartment,
    db: Session = Depends(get_db),
    _: Users = Depends(permissions.require_admin)
):
    department_exists = db.query(Departments).filter_by(name=department.name).first()
    if department_exists:
        raise HTTPException(
            status_code=400,
            detail="Department already exists"
        )        
    location_exists = db.query(OfficeLocations).filter_by(id=department.location_id).first()
    if not location_exists:
        raise HTTPException(
            status_code=404,
            detail="Location doesnt exist"
        )
    new_department = Departments(
        name = department.name,
        description = department.description,
        location_id = department.location_id
    )

    db.add(new_department)
    db.commit()
    db.refresh(new_department)
    return new_department

@router.post("/add-location", response_model=company.OfficeLocationResponse, status_code=201)
def AddOfficeLocation(
    location: company.AddOfficeLocation,
    db: Session = Depends(get_db),
    _: Users = Depends(permissions.require_admin)
):
    location_exists = db.query(OfficeLocations).filter_by(name=location.name).first()
    if location_exists:
        raise HTTPException(
            status_code=400,
            detail="Location already exists"
        )
    new_location = OfficeLocations(
        name = location.name,
        street_address = location.street_address,
        city = location.city,
        state = location.state,
        country = location.country
    )

    db.add(new_location)
    db.commit()
    db.refresh(new_location)
    return new_location