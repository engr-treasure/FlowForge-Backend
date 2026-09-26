# FlowForge

FlowForge is an intelligent operations and resource management API built with **FastAPI**.

The system is designed for organizations that manage shared technical equipment, staff, customers, bookings, resource availability, and approval workflows.

FlowForge focuses on applying software engineering principles to real-world operational workflows, including authentication, role-based authorization, relational data modelling, booking validation, resource conflict detection, database migrations, automated testing, and containerized deployment.

## Features

* Staff and user management
* Role-based access control
* Office locations and departments
* Job and organizational structure
* Customer management
* Equipment management
* Equipment operational status management
* Multi-equipment bookings
* Booking approval workflows
* Booking conflict and availability validation
* Equipment-specific rest periods between bookings
* JWT-based authentication
* Argon2 password hashing
* Input and response validation with Pydantic
* Database migrations with Alembic
* Paginated API responses
* Automated API tests with Pytest
* Docker containerization

## Tech Stack

* **Python**
* **FastAPI**
* **SQLAlchemy**
* **Pydantic**
* **SQLite** for local development
* **Alembic** for database migrations
* **JWT** for authentication
* **Argon2** for password hashing
* **Pytest** for automated testing
* **Docker** for containerization

## Architecture

FlowForge is structured to separate application responsibilities across models, schemas, dependencies, routers, and core configuration.

The project is designed to evolve toward a service-oriented backend architecture as business logic becomes more complex.

## Project Structure

```text
FlowForge/
│
├── app/
│   ├── main.py
│   ├── core/
│   │   ├── config.py
│   │   ├── enums.py
│   │   └── security.py
│   │
│   ├── databases/
│   │   └── database.py
│   │
│   ├── models/
│   │   ├── booking.py
│   │   ├── company.py
│   │   ├── customer.py
│   │   ├── equipment.py
│   │   └── user.py
│   │
│   ├── schemas/
│   │   ├── booking.py
│   │   ├── company.py
│   │   ├── customer.py
│   │   ├── equipment.py
│   │   └── user.py
│   │
│   ├── dependencies/
│   │   ├── auth.py
│   │   ├── booking_dependencies.py
│   │   ├── company_dependencies.py
│   │   ├── customer_dependencies.py
│   │   ├── equipment_dependencies.py
│   │   ├── permissions.py
│   │   └── user_dependencies.py
│   │
│   └── routers/
│       ├── booking.py
│       ├── company.py
│       ├── customer.py
│       ├── equipment.py
│       └── user.py
│
├── tests/
├── scripts/
│   └── bootstrap.py
├── alembic/
├── .env.example
├── .gitignore
├── alembic.ini
├── Dockerfile
├── requirements.txt
└── README.md
```

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd FlowForge
```

### 2. Create a virtual environment

#### Windows

```powershell
python -m venv .venv
.venv\Scripts\activate
```

#### macOS/Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file in the project root based on `.env.example`.

Do not commit `.env` or other files containing secrets to version control.

## Database Setup

FlowForge uses **Alembic** to manage database schema changes.

Apply the latest migrations with:

```bash
alembic upgrade head
```

## Initial Admin Setup

FlowForge includes a bootstrap script for creating the initial organizational structure and administrator account.

Run:

```bash
python scripts/bootstrap.py
```

The bootstrap process creates the initial:

* Office location
* Department
* Job
* Administrator account

The bootstrap script is protected against being run multiple times on the same database.

## Running the Application

Start the development server with:

```bash
python -m uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

Alternative API documentation:

```text
http://127.0.0.1:8000/redoc
```

## Running with Docker

Build the Docker image:

```bash
docker build -t flowforge-backend .
```

Run the container:

```bash
docker run -d -p 8000:8000 --name flowforge-api flowforge-backend
```

The API can then be accessed at:

```text
http://localhost:8000
```

Swagger documentation:

```text
http://localhost:8000/docs
```

To view container logs:

```bash
docker logs flowforge-api
```

## Running Tests

Run the complete test suite with:

```bash
python -m pytest
```

For verbose output:

```bash
python -m pytest -v
```

Tests use a separate test database and override the application's database dependency so that tests do not modify the development database.

## Authentication

FlowForge uses **JWT Bearer authentication**.

Users authenticate through the login endpoint and receive an access token that must be supplied when accessing protected endpoints.

Example:

```http
Authorization: Bearer <access_token>
```

Passwords are securely hashed using **Argon2** rather than being stored in plaintext.

## Roles

FlowForge currently supports four roles:

| Role           | Responsibility                                      |
| -------------- | --------------------------------------------------- |
| **Admin**      | System and organizational administration            |
| **Manager**    | Management and approval operations                  |
| **Staff**      | Operational users who manage bookings and customers |
| **Technician** | Equipment-related operational responsibilities      |

Access to protected endpoints is controlled through role-based authorization and active-user checks.

## Booking and Resource Management

A booking can contain multiple pieces of equipment.

Before a booking is created, FlowForge validates:

* Whether the requested equipment exists
* Whether equipment is operationally available
* Whether the requested time range is valid
* Whether the equipment already has a conflicting booking
* Whether the equipment's configured rest period has elapsed
* Whether all requested equipment can be booked for the requested period

If any requested resource cannot satisfy the booking requirements, the booking is rejected rather than partially created.

This ensures that multi-resource bookings remain consistent.

## Booking Approval

Equipment can be configured with approval requirements.

Depending on the equipment and organizational rules, a booking can enter an approval workflow before becoming confirmed.

The booking lifecycle currently supports statuses including:

* `pending`
* `confirmed`
* `rejected`
* `cancelled`
* `completed`

Approval and rejection information is recorded against the booking.

## Pagination

List endpoints support pagination to avoid returning unrestricted result sets.

Paginated responses include:

* Items
* Current page
* Page size
* Total records
* Total pages

Example:

```text
GET /bookings?page=1&limit=20
```

## Development Status

FlowForge is currently under active development.

The current version focuses on the core operational workflow:

* Authentication
* User and organizational management
* Customers
* Equipment
* Resource availability
* Bookings
* Booking conflicts
* Approval workflows
* Pagination
* Automated testing
* Docker-based execution

### Future Improvements

Planned areas for future development include:

* Advanced availability search
* Notifications
* Approval escalation workflows
* Background task processing
* Expanded service-layer architecture
* Improved repository/data-access patterns
* Expanded automated test coverage
* Production database support such as PostgreSQL
* Docker Compose for multi-service development

Maintenance management has been intentionally left outside the current v1 scope so that the core resource-management workflow can be developed and validated first.

## License

This project is currently intended as a personal software engineering and portfolio project.
