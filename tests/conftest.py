from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.models import company
from app.core.config import settings
from app.core.security import encrypt_password
from app.core.enums import EmploymentStatus, Roles
from app.databases.database import get_db, Base
from fastapi.testclient import TestClient
from app.models import user
import pytest
from main import app

engine = create_engine(
    settings.test_database_url,
    connect_args={"check_same_thread":False}
)

TestSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

@pytest.fixture
def test_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def location(test_db):
    location = company.OfficeLocations(
        name="Test Location",
        street_address="30 Umaru Street",
        city="Abakaleke",
        state="Abia",
        country="Nigeria"
    )

    test_db.add(location)
    test_db.commit()
    test_db.refresh(location)

    return location

@pytest.fixture
def department(test_db, location):
    department = company.Departments(
        name="IT Department",
        description="Software engineering, data analysis, AI automations",
        location_id=location.id
    )

    test_db.add(department)
    test_db.commit()
    test_db.refresh(department)

    return department

@pytest.fixture
def job(test_db, department):
    job = company.Jobs(
        title="Software Developer",
        description="Develop web and mobile apps",
        department_id=department.id
    )

    test_db.add(job)
    test_db.commit()
    test_db.refresh(job)

    return job

@pytest.fixture
def admin(test_db, job):
    admin = user.Users(
        first_name="Ayo",
        last_name="Segun",
        email="admin@test.com",
        password_hash=encrypt_password("TestPass123!"),
        role=Roles.ADMIN,
        phone_number="08123456789",
        street_address="Test Street",
        city="Lagos",
        state="Lagos",
        country="Nigeria",
        job_id=job.id,
        employment_status=EmploymentStatus.ACTIVE
    )

    test_db.add(admin)
    test_db.flush()

    admin.staff_id = (
        f"STF{str(admin.join_date.year)[-2:]}"
        f"{admin.id:03d}"
    )

    test_db.commit()
    test_db.refresh(admin)

    return admin

@pytest.fixture
def staff(test_db, job):
    staff = user.Users(
        first_name="Mo",
        last_name="Segun",
        email="staff@test.com",
        password_hash=encrypt_password("TestPass123!"),
        role=Roles.STAFF,
        phone_number="08123456780",
        street_address="Test Street",
        city="Lagos",
        state="Lagos",
        country="Nigeria",
        job_id=job.id,
        employment_status=EmploymentStatus.ACTIVE
    )

    test_db.add(staff)
    test_db.flush()

    staff.staff_id = (
        f"STF{str(staff.join_date.year)[-2:]}"
        f"{staff.id:03d}"
    )

    test_db.commit()
    test_db.refresh(staff)

    return staff

@pytest.fixture
def manager(test_db, job):
    manager = user.Users(
        first_name="Mo",
        last_name="Segun",
        password_hash=encrypt_password("TestPass123!"),
        role=Roles.MANAGER,
        phone_number="08123456780",
        street_address="Test Street",
        city="Lagos",
        state="Lagos",
        country="Nigeria",
        job_id=job.id,
        employment_status=EmploymentStatus.ACTIVE
    )

    test_db.add(manager)
    test_db.flush()

    manager.staff_id = (
        f"STF{str(manager.join_date.year)[-2:]}"
        f"{manager.id:03d}"
    )

    test_db.commit()
    test_db.refresh(manager)

    return manager

@pytest.fixture
def admin_client(admin, client):
    login_data = {
        "username": admin.staff_id,
        "password": "TestPass123!"
    }
    response = client.post("users/login", json=login_data)
    print(response.json())
    assert response.status_code == 201
    token = response.json()["access_token"]
    client.headers.update({
        "Authorization": f"Bearer {token}"
    })
    return client

@pytest.fixture
def staff_client(staff, client):
    login_data = {
        "username": staff.staff_id,
        "password": "TestPass123!"
    }
    response = client.post("users/login", json=login_data)
    print(response.json())
    assert response.status_code == 201
    token = response.json()["access_token"]
    client.headers.update({
        "Authorization": f"Bearer {token}"
    })
    return client

@pytest.fixture
def manager_client(manager, client):
    login_data = {
        "username": manager.staff_id,
        "password": "TestPass123!"
    }
    response = client.post("users/login", json=login_data)
    print(response.json())
    assert response.status_code == 201
    token = response.json()["access_token"]
    client.headers.update({
        "Authorization": f"Bearer {token}"
    })
    return client

@pytest.fixture
def client(test_db):
    app.dependency_overrides[get_db] = lambda: test_db
    yield TestClient(app)

    app.dependency_overrides.clear()