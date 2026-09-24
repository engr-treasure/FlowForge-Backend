from app.models import company
from app.databases.database import SessionLocal
from app.models import user
from app.core.security import encrypt_password
from app.core.enums import Roles, EmploymentStatus
from app.core.config import settings
db = SessionLocal()
try:
    existing_admin = db.query(user.Users).filter(
        user.Users.role == Roles.ADMIN
    ).first()

    if existing_admin:
        raise RuntimeError("FlowForge has already been bootstrapped.")

    location = company.OfficeLocations(
        name = "FixForge Apatapoto",
        street_address = "30, Delta Savi Street",
        city = "Apatapotp",
        state = "Anambra",
        country = "Nigeria"
    )
    db.add(location)
    db.flush()

    department = company.Departments(
        name = "Infrastructure",
        description = "Oversees company processes",
        location_id = location.id
    )

    db.add(department)
    db.flush()

    job = company.Jobs(
        title = "Admin officer",
        description = "Grants perssions and oversees infrastructure",
        department_id = department.id
    )
    db.add(job)
    db.flush()

    admin = user.Users(
        first_name="Ayomide",
        last_name="Segun",
        phone_number="+2348000000000",
        password_hash=encrypt_password(settings.bootstrap_admin_password),
        role=Roles.ADMIN,
        street_address = "29 Gregory Street",
        city = "Apatapoto",
        state = "Anambra",
        country = "Nigeria",
        job_id = job.id,
        employment_status = EmploymentStatus.ACTIVE
    )
    db.add(admin)
    db.flush()
    admin.staff_id = f"STF{str(admin.join_date.year)[-2:]}{admin.id:03d}"
    db.commit()
    print(f"Admin created successfully: {admin.staff_id} - {job.title} - {department.name} - {location.name}")
except Exception:
    db.rollback()
    raise

finally:
    db.close()
