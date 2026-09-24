from app.models.company import OfficeLocations
def test_location_creation_successful(test_db, admin_client):
    new_location = {
        "name": "FlowForge Okota",
        "street_address": "30 Ago Palace Way",
        "city": "Okota",
        "state": "Lagos",
        "country": "Nigeria"
    }
    locations = test_db.query(OfficeLocations).all()
    print("EXISTING LOCATIONS:", locations)
    response = admin_client.post("company/add-location", json=new_location)
    print("BODY:", response.json())
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    

def test_department_creation_successful(admin_client, location):
    new_department = {
        "name": "Marketing Department",
        "description": "Handles marketing company processes",
        "location_id": location.id
    }
    response = admin_client.post("company/add-department", json=new_department)
    print("BODY:", response.json())
    assert response.status_code == 201
    data = response.json()
    assert "id" in data

def test_job_creation_successful(admin_client, department):
    new_job = {
        "title": "IT Manager",
        "description": "Oversees all IT operations",
        "department_id": department.id
    }
    response = admin_client.post("company/add-job", json=new_job)
    print("BODY:", response.json())
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
