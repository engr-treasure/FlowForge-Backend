from fastapi import Depends, HTTPException
from app.models.user import Users
from app.schemas.user import UserLookup
from app.databases.database import get_db
from sqlalchemy.orm import Session

def get_user_by_staff_id(
    staff_id: str,
    db: Session = Depends(get_db)
):
    staff = db.query(Users).filter(Users.staff_id==staff_id).first()
    if not staff:
        raise HTTPException(
            status_code=404,
            detail="Staff does not exist"
        )
    return staff