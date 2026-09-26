from fastapi import Depends, HTTPException
from app.models.customer import Customers
from app.schemas.equipment import EquipmentLookup
from app.databases.database import get_db
from sqlalchemy.orm import Session

def get_customer_by_id(
    customer_id: int,
    db: Session = Depends(get_db)
):
    customer = db.query(Customers).filter_by(id==customer_id).first()
    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer does not exist"
        )
    return customer
