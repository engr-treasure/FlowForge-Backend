def test_registration_successful(admin_client, job):

    new_user = {
        "role": "admin",
        "first_name": "Ayomide",
        "last_name": "Segun",
        "phone_number": "08112660274",
        "street_address": "29 Jemtok Street",
        "city": "Okota",
        "state": "Lagos",
        "country": "Nigeria",
        "job_id": job.id,
        "employment_status": "active",
        "password": "pass123@Ayo",
        "repeat_password": "pass123@Ayo"
    }
    response = admin_client.post("users/register", json=new_user)
    assert response.status_code== 201
    data = response.json()
    assert data["staff_id"] == "STF26002"

def test_registration_failed_existing_user(admin_client, job):

    new_user = {
        "role": "admin",
        "first_name": "Ayo",
        "last_name": "Segun",
        "phone_number": "08112660274",
        "street_address": "29 Jemtok Street",
        "city": "Okota",
        "state": "Lagos",
        "country": "Nigeria",
        "job_id": job.id,
        "employment_status": "active",
        "password": "pass123@Ayo",
        "repeat_password": "pass123@Ayo"
    }
    response = admin_client.post("users/register", json=new_user)
    assert response.status_code== 400
    data = response.json()
    assert data["detail"] == "User already exists"

def test_registration_failed_unauthenticated(client, job):

    new_user = {
        "role": "admin",
        "first_name": "Ayomide",
        "last_name": "Segun",
        "phone_number": "08112660274",
        "street_address": "29 Jemtok Street",
        "city": "Okota",
        "state": "Lagos",
        "country": "Nigeria",
        "job_id": job.id,
        "employment_status": "active",
        "password": "pass123@Ayo",
        "repeat_password": "pass123@Ayo"
    }
    response = client.post("users/register", json=new_user)
    assert response.status_code== 401

def test_registration_failed_unauthorized(staff_client, job):

    new_user = {
        "role": "staff",
        "first_name": "Ayomide",
        "last_name": "Segun",
        "phone_number": "08112660274",
        "street_address": "29 Jemtok Street",
        "city": "Okota",
        "state": "Lagos",
        "country": "Nigeria",
        "job_id": job.id,
        "employment_status": "active",
        "password": "pass123@Ayo",
        "repeat_password": "pass123@Ayo"
    }
    response = staff_client.post("users/register", json=new_user)
    assert response.status_code== 403
    assert response.json()["detail"] == "Admin access required"

def test_get_users_successful_for_admin(admin_client):
    response = admin_client.get("/users")
    print(response.json())
    assert response.status_code == 200

def test_get_users_successful_for_manager(manager_client):
    response = manager_client.get("/users")
    print(response.json())
    assert response.status_code == 200

def test_get_users_failed_authorization(staff_client):
    response = staff_client.get("/users")
    assert response.status_code == 403
    assert response.json()["detail"] == "Admin or Manager access required"

def test_get_users_failed_unauthenticated(client):
    response = client.get("/users")
    assert response.status_code == 401

def test_update_user_successful(admin_client, job):
    update_user = {
        "email": "ayo@companyname.com"
    }
    response = admin_client.patch("users/STF26001", json=update_user)
    assert response.status_code== 200
    data = response.json()