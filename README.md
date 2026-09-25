FlowForge is an intelligent operations and resource management API built with FastAPI.
The system is designed for organizations that manage shared technical equipment, facilities, staff, bookings, maintenance, and approval workflows.

Features
• Staff and user management
• Role-based access control
• Office locations and departments
• Job and organizational structure
• Equipment management
• Equipment availability tracking
• Booking management
• Booking approval workflows
• Maintenance management
• JWT-based authentication
• Password hashing
• Input and response validation
• Database migrations with Alembic
• Automated API tests with Pytest

Tech Stack
• Python
• FastAPI
• SQLAlchemy
• Pydantic
• SQLite for local development
• Alembic for database migrations
• JWT for authentication
• Argon2 for password hashing
• Pytest for testing

Project Structure
FlowForge/
│
├── app/
│   ├── main.py
│   ├── core/
│   ├── db/
│   ├── models/
│   ├── schemas/
│   ├── api/
│   ├── dependencies/
│   └── services/
│
├── tests/
├── scripts/
│   └── bootstrap.py
├── alembic/
├── .env.example
├── .gitignore
├── alembic.ini
├── requirements.txt
└── README.md

Installation
1. Clone the repository
    git clone <repository-url>
    cd FlowForge
2. Create a virtual environment
    Windows:
    python -m venv .venv
    .venv\Scripts\activate
    macOS/Linux:
    python3 -m venv .venv
    source .venv/bin/activate
3. Install dependencies
    pip install -r requirements.txt
    Environment Variables
    Create a .env file in the project root based on .env.example.

Database Setup
FlowForge uses Alembic for database migrations.
Apply the migrations with:
alembic upgrade head

Initial Admin Setup
FlowForge uses a bootstrap script to create the initial organizational structure and administrator.
Run:
python scripts/bootstrap.py
The bootstrap process creates the initial:
• Office location
• Department
• Job
• Administrator account
The bootstrap script is protected against being run multiple times on the same database.

Running the Application
Start the development server with: python -m uvicorn app.main:app --reload

The API will be available at: http://127.0.0.1:8000
Interactive API documentation: http://127.0.0.1:8000/docs
Alternative API documentation: http://127.0.0.1:8000/redoc

Running Tests
Run the complete test suite with:python -m pytest
For verbose output:python -m pytest -v
Tests use a separate test database and override the application’s database dependency so that tests do not modify the development database.

Authentication
FlowForge uses JWT bearer authentication.
Users authenticate through the login endpoint and receive an access token that must be supplied in subsequent protected requests.
Example:
Authorization: Bearer <access_token>

Roles
FlowForge currently supports the following roles:
• Admin — system and organizational administration
• Manager — management and approval operations
• Staff — operational users
• Technician — equipment and maintenance operations
Access to protected endpoints is controlled through role-based authorization.

Development Status
FlowForge is currently under active development.
The architecture and feature set may evolve as additional business workflows are implemented.
Planned areas include:
• Advanced equipment availability queries
• Booking conflict detection
• Maintenance scheduling
• Approval workflows
• Notifications
• Escalation workflows
• Improved service-layer architecture
• Expanded automated test coverage

License
This project is currently intended as a personal software engineering project.