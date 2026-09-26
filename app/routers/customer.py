from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.schemas.customer import CustomerResponse, CustomerListResponse, AddCustomer, UpdateCustomer
from app.databases.database import get_db
from app.dependencies import permissions
from app.dependencies.customer_dependencies import get_customer_by_id
from app.models.user import Users
from app.models.customer import Customers
from datetime import datetime, timezone
import math

router = APIRouter(
    prefix="/customers",
    tags=["customer"]
)

@router.post("/add-customer", response_model=CustomerResponse)
def add_customer(
    db: Session = Depends(get_db),
    customer = AddCustomer,
     _: Users = Depends(permissions.require_admin),
    __: Users = Depends(permissions.allow_active_staff)
):
    customer_exists = db.query(Users).filter_by(name=customer.email).first()
    if customer_exists:
        raise HTTPException(
            status_code=400,
            detail="customer already exists"
        )        
    customer_exists = db.query(Users).filter_by(name=customer.phone_number).first()
    if customer_exists:
        raise HTTPException(
            status_code=400,
            detail="customer already exists"
        )        

    new_customer = Customers(
        first_name = customer.first_name,
        last_name = customer.last_name,
        email = customer.email,
        phone_number = customer.phone_number,
        bookings = customer.bookings
    )

    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    return new_customer

@router.get("/", response_model=CustomerListResponse)
def get_customers(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    _: Users = Depends(permissions.require_admin_or_manager),
    __: Users = Depends(permissions.allow_active_staff)
):
    total = db.query(Customers).count()
    pages = math.ceil(total / limit)
    offset = (page - 1) * limit
    customers = db.query(Customers).order_by(Customers.created_at.desc()).offset(offset).limit(limit).all()
  
    return customers


@router.get("/{id}", response_model=CustomerResponse)
def get_customer_by_id(
    customer: Customers = Depends(get_customer_by_id),
    _: Users = Depends(permissions.require_admin_or_manager),
    __: Users = Depends(permissions.allow_active_staff)
):
    return customer

@router.patch("/{id}", response_model=CustomerResponse)
def update_customer(
    update_details: UpdateCustomer,
    verified_customer: Customers = Depends(get_customer_by_id),
    db: Session = Depends(get_db),
    _: Users = Depends(permissions.require_admin),
    __: Users = Depends(permissions.allow_active_staff)
):
    updated = update_details.model_dump(exclude_unset=True)
    updated["updated_at"] = datetime.now(timezone.utc)
    for key, value in updated.items():
        setattr(verified_customer, key, value)
    
    db.commit()
    db.refresh(verified_customer)
    return verified_customer

@router.delete("/{id}", response_model=CustomerResponse)
def delete_customer(
    customer: Customers = Depends(get_customer_by_id),
    db: Session = Depends(get_db),
    _: Users = Depends(permissions.require_admin),
    __: Users = Depends(permissions.allow_active_staff)
):
    db.delete(customer)
    db.commit()
    return customer