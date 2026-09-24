from fastapi import APIRouter, Depends, HTTPException
from app.dependencies import auth, permissions
from app.databases.database import get_db
from sqlalchemy.orm import Session
from app.schemas import user
from app.models.user import Users
from app.models.company import Departments, Jobs
from app.core.security import encrypt_password, verify_password, create_access_token
from app.dependencies import user_dependencies
from app.core import enums
router = APIRouter(
    prefix="/users",
    tags=["user"]
)

@router.post("/register", response_model=user.RegistrationResponse, status_code=201)
def register(
    user: user.Register,
    db: Session = Depends(get_db),
    _: Users = Depends(permissions.require_admin),
    __: Users = Depends(permissions.allow_active_staff)
):
    if user.email:
        user_exists = db.query(Users).filter_by(email=user.email).first()
        if user_exists:
            raise HTTPException(
                status_code=400,
                detail="User already exists"
            )
    else:
        user_exists = db.query(Users).filter(Users.first_name == user.first_name, Users.last_name == user.last_name).first()
        if user_exists:
            raise HTTPException(
                status_code=400,
                detail="User already exists"
            )

    
    job_exists = db.query(Jobs).filter_by(id=user.job_id).first()
    if not job_exists:
        raise HTTPException(
            status_code=404,
            detail="Job does not exist"
        )
    
    hashed_password = encrypt_password(user.password)
    normalized_phone_number = f"+234{user.phone_number[-10:]}"
    join_year = str(user.join_date.year)[-2:]
    

    new_user = Users(
        role = user.role,
        first_name = user.first_name,
        last_name = user.last_name,
        email = user.email,
        phone_number = normalized_phone_number,
        street_address = user.street_address,
        city = user.city,
        state = user.state,
        country = user.country,
        job_id = user.job_id,
        employment_status = user.employment_status,
        password_hash = hashed_password,
        join_date = user.join_date
    )

    db.add(new_user)
    db.flush()
    staff_id = f"STF{join_year}{new_user.id:03d}"
    new_user.staff_id = staff_id
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login", response_model=user.LoginResponse, status_code=201)
def login(
    user: user.Login,
    db: Session = Depends(get_db)   
):
    db_user = db.query(Users).filter_by(email=user.username).first()
    if not db_user:
        db_user = db.query(Users).filter_by(staff_id=user.username).first()
    if not db_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid Email or Password"
        )       
    password_verified = verify_password(user.password, db_user.password_hash)
    if not password_verified:
        raise HTTPException(
            status_code=401,
            detail="Invalid Email or Password"
        )
    access_token = create_access_token(
        data={"sub": str(db_user.id)}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.get("/", response_model=list[user.UserResponse])
def get_users(
    db: Session = Depends(get_db),
    allowed_user: Users = Depends(permissions.require_admin_or_manager),
    __: Users = Depends(permissions.allow_active_staff)
):
    if allowed_user.role == enums.Roles.ADMIN:
        users = db.query(Users).all()
    else:
        users = db.query(Users).join(Users.job).join(Jobs.department).filter(Departments.id==allowed_user.job.department.id).all()
        # We use join() when constructing a database query that needs information from related tables. 
        # allowed_user is already a SQLAlchemy Users instance, so we can navigate its relationships directly.
    return users

@router.get("/profile", response_model=user.UserResponse)
def profile(
    user: Users = Depends(auth.get_authorized_user),
    __: Users = Depends(permissions.allow_active_staff)
):
    return user

@router.get("/{staff_id}", response_model=user.UserResponse)
def get_user(
    staff: Users = Depends(user_dependencies.get_user_by_staff_id),
    _: Users = Depends(permissions.require_admin_or_manager),
    __: Users = Depends(permissions.allow_active_staff)
):
    return staff

@router.patch("/{staff_id}", response_model=user.UserResponse)
def update_user(
    update_details: user.UpdateUser,
    verified_staff: Users = Depends(user_dependencies.get_user_by_staff_id),
    db: Session = Depends(get_db),
    _: Users = Depends(permissions.require_admin),
    __: Users = Depends(permissions.allow_active_staff)
):
    update_user = update_details.model_dump(exclude_unset=True)
    for key, value in update_user.items():
        setattr(verified_staff, key, value)

    db.commit()
    db.refresh(update_user)
    return update_user

    