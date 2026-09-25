from fastapi import APIRouter, Depends, HTTPException
from app.databases.database import get_db
from sqlalchemy.orm import Session
from app.schemas import company
from app.models.user import Users
from app.models.company import Jobs, OfficeLocations, Departments
from app.dependencies import permissions, company_dependencies
from app.core import enums

router = APIRouter(
    prefix="/company",
    tags=["company"]
)

@router.post("/jobs/add-job", response_model=company.JobResponse, status_code=201)
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

@router.get("/jobs", response_model=list[company.JobResponse])
def get_jobs(
    db: Session = Depends(get_db),
    allowed_user: Users = Depends(permissions.require_admin_or_manager),
    __: Users = Depends(permissions.allow_active_staff)
):
    if allowed_user.role == enums.Roles.ADMIN:
        jobs = db.query(Jobs).all()
    else:
        jobs = db.query(Jobs).filter(Jobs.department_id==allowed_user.job.department_id).all()
        # We use join() when constructing a database query that needs information from related tables. 
        # allowed_job is already a SQLAlchemy jobs instance, so we can navigate its relationships directly.
    return jobs


@router.get("/jobs/{id}", response_model=company.JobResponse)
def get_job_by_id(
    job: Users = Depends(company_dependencies.get_job_by_id),
    _: Users = Depends(permissions.require_admin_or_manager),
    __: Users = Depends(permissions.allow_active_staff)
):
    return job

@router.patch("/jobs/{id}", response_model=company.JobResponse)
def update_job(
    update_details: company.UpdateJob,
    verified_job: Users = Depends(company_dependencies.get_job_by_id),
    db: Session = Depends(get_db),
    _: Users = Depends(permissions.require_admin),
    __: Users = Depends(permissions.allow_active_staff)
):
    update_job = update_details.model_dump(exclude_unset=True)
    for key, value in update_job.items():
        setattr(verified_job, key, value)

    db.commit()
    db.refresh(update_job)
    return update_job

@router.delete("/jobs/{id}", response_model=company.JobResponse)
def get_job(
    job: Users = Depends(company_dependencies.get_job_by_id),
    db: Session = Depends(get_db),
    _: Users = Depends(permissions.require_admin),
    __: Users = Depends(permissions.allow_active_staff)
):
    db.delete(job)
    db.commit()
    return job

@router.post("/departments/add-department", response_model=company.DepartmentResponse, status_code=201)
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

@router.get("/departments", response_model=list[company.DepartmentResponse])
def get_departments(
    db: Session = Depends(get_db),
    _: Users = Depends(permissions.require_admin),
    __: Users = Depends(permissions.allow_active_staff)
):
    jobs = db.query(Departments).all()
    return jobs


@router.get("/departments/{id}", response_model=company.DepartmentResponse)
def get_department_by_id(
    department: Departments = Depends(company_dependencies.get_department_by_id),
    _: Users = Depends(permissions.require_admin_or_manager),
    __: Users = Depends(permissions.allow_active_staff)
):
    return department

@router.patch("/departments/{id}", response_model=company.DepartmentResponse)
def update_department(
    update_details: company.UpdateDepartment,
    verified_department: Departments = Depends(company_dependencies.get_job_by_id),
    db: Session = Depends(get_db),
    _: Users = Depends(permissions.require_admin),
    __: Users = Depends(permissions.allow_active_staff)
):
    update_department = update_details.model_dump(exclude_unset=True)
    for key, value in update_department.items():
        setattr(verified_department, key, value)

    db.commit()
    db.refresh(update_department)
    return update_department

@router.delete("/departments/{id}", response_model=company.DepartmentResponse)
def delete_department(
    department: Departments = Depends(company_dependencies.get_department_by_id),
    db: Session = Depends(get_db),
    _: Users = Depends(permissions.require_admin),
    __: Users = Depends(permissions.allow_active_staff)
):
    db.delete(department)
    db.commit()
    return department

@router.post("/locations/add-location", response_model=company.OfficeLocationResponse, status_code=201)
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

@router.get("/locations", response_model=list[company.OfficeLocationResponse])
def get_office_locations(
    db: Session = Depends(get_db),
    _: Users = Depends(permissions.require_admin),
    __: Users = Depends(permissions.allow_active_staff)
):
    jobs = db.query(OfficeLocations).all()
    return jobs


@router.get("/locations/{id}", response_model=company.OfficeLocationResponse)
def get_office_location_by_id(
    location: OfficeLocations = Depends(company_dependencies.get_location_by_id),
    _: Users = Depends(permissions.require_admin_or_manager),
    __: Users = Depends(permissions.allow_active_staff)
):
    return location

@router.patch("/locations/{id}", response_model=company.OfficeLocationResponse)
def update_office_location(
    update_details: company.UpdateOfficeLocation,
    verified_location: OfficeLocations = Depends(company_dependencies.get_location_by_id),
    db: Session = Depends(get_db),
    _: Users = Depends(permissions.require_admin),
    __: Users = Depends(permissions.allow_active_staff)
):
    update_location = update_details.model_dump(exclude_unset=True)
    for key, value in update_location.items():
        setattr(verified_location, key, value)

    db.commit()
    db.refresh(update_location)
    return update_location

@router.delete("/locations/{id}", response_model=company.OfficeLocationResponse)
def delete_office_location(
    location: OfficeLocations = Depends(company_dependencies.get_location_by_id),
    db: Session = Depends(get_db),
    _: Users = Depends(permissions.require_admin),
    __: Users = Depends(permissions.allow_active_staff)
):
    db.delete(location)
    db.commit()
    return location