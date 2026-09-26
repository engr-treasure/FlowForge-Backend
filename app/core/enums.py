from enum import Enum

class Roles(str, Enum):
    ADMIN = "admin"
    STAFF = "staff"
    TECHNICIAN = "technician"
    MANAGER = "manager"

class EmploymentStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"

class EquipmentCategories(str, Enum):
    COMPUTING = "computing"
    NETWORKING = "networking"
    POWER = "power"
    AUDIO_OR_VISUAL = "audio/visual"
    TESTING_AND_MEASUREMENT = "testing and measurement"
    TOOLS_AND_WORKSHOP = "tools and network"
    IOT_AND_EMBEDDED = "iot and embedded"
    OFFICE = "office"
    OTHER = "other"

class EquipmentOperationalStatus(str, Enum):
    AVAILABLE = "available"
    UNAVAILABLE = "unavailable"
    MAINTENANCE = "maintenance"
    RETIRED = "retired"

class ApprovalRequirements(str, Enum):
    REQUIRED = "required"
    NOT_REQUIRED = "not required"

class BookingStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    CANCELLED = "cancelled"
    COMPLETED = "completed"