from enum import Enum

class Roles(str, Enum):
    ADMIN = "admin"
    STAFF = "staff"
    TECHNICIAN = "technician"
    MANAGER = "manager"

class EmploymentStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"