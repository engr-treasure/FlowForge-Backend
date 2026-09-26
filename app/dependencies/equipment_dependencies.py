from fastapi import Depends, HTTPException
from app.models.equipment import Equipments
from app.schemas.equipment import EquipmentLookup
from app.databases.database import get_db
from sqlalchemy.orm import Session

def get_equipment_by_id(
    equipment_id: int,
    db: Session = Depends(get_db)
):
    equipment = db.query(Equipments).filter_by(id==equipment_id).first()
    if not equipment:
        raise HTTPException(
            status_code=404,
            detail="Equipment does not exist"
        )
    return equipment
