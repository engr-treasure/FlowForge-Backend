from app.core.security import decode_access_token
from fastapi import HTTPException, Depends, security
from app.databases.database import get_db
from sqlalchemy.orm import Session
from app.models import user

auth2_scheme = security.OAuth2PasswordBearer(tokenUrl="users/login")
def get_authenticated_user(
    token: str = Depends(auth2_scheme),
    db: Session = Depends(get_db)
):
    payload = decode_access_token(token)
    user_id = int(payload["sub"])

    current_user = db.query(user.Users).filter_by(id=user_id).first()
    if not current_user:
        raise HTTPException(
            status_code=401,
            detail="Login to continue"
        )
    return current_user