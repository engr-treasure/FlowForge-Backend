from app.databases.database import SessionLocal
from app.models.user import Users
from app.core.security import encrypt_password
from app.core.enums import Roles, EmploymentStatus
db = SessionLocal()

admin = Users(
    first_name="Ayomide",
    last_name="Segun",
    password_hash=encrypt_password("pass123"),
    role=Roles.ADMIN,
    street_address = "29 Gregory Street",
    city = "Apatapoto",
    state = "Anambra",
    country = "Kenya",
    job_id = 1,
    employment_status = EmploymentStatus.ACTIVE
)
db.add(admin)
db.flush()
admin.staff_id = f"STF{str(admin.join_date.year)[-2:]}{admin.id:03d}"
db.commit()
print(f"Admin created successfully: {admin.staff_id}")
db.close()