from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app.databases.database import get_db
from app.models import user
from app.dependencies import auth
from app.core import enums

def allow_active_staff(
    user : user.Users = Depends(auth.get_authenticated_user),
    db: Session = Depends(get_db)
):
    if user.role != enums.EmploymentStatus.ACTIVE:
        raise HTTPException(
            status_code=403,
            detail="Staff access required"
        )
    return user

def require_admin(
    user : user.Users = Depends(auth.get_authenticated_user),
    db: Session = Depends(get_db)
):
    if user.role != enums.Roles.ADMIN:
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )
    return user

def require_admin_or_manager(
    user : user.Users = Depends(auth.get_authenticated_user),
    db: Session = Depends(get_db)
):
    if user.role != enums.Roles.ADMIN and user.role != enums.Roles.MANAGER:
        raise HTTPException(
            status_code=403,
            detail="Admin or Manager access required"
        )
    return user
    