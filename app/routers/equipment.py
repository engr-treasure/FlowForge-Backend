from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.schemas.equipment import EquipmentResponse, EquipmentListResponse, AddEquipment, UpdateEquipment
from app.databases.database import get_db
from app.dependencies import permissions
from app.dependencies.equipment_dependencies import get_equipment_by_id
from app.models.user import Users
from app.models.company import OfficeLocations
from app.models.equipment import Equipments
from datetime import datetime, timezone
import math

router = APIRouter(
    prefix="/equipments",
    tags=["equipment"]
)

@router.post("/add-equipment", response_model=EquipmentResponse)
def add_equipment(
    db: Session = Depends(get_db),
    equipment = AddEquipment,
     _: Users = Depends(permissions.require_admin),
    __: Users = Depends(permissions.allow_active_staff)
):
    equipment_exists = db.query(Users).filter_by(name=equipment.name).first()

    if equipment_exists:
        raise HTTPException(
            status_code=400,
            detail="Equipment already exists"
        )        
    location_exists = db.query(OfficeLocations).filter_by(id=equipment.location_id).first()
    if not location_exists:
        raise HTTPException(
            status_code=404,
            detail="Location doesnt exist"
        )
    new_equipment = Equipments(
        name = equipment.name,
        description = equipment.description,
        category = equipment.category,
        location_id = equipment.location_id,
        serial_number = equipment.serial_number,
        manufacturer = equipment.manufacturer,
        model = equipment.model,
        quantity = equipment.quantity,
        approval = equipment.approval,
        date_acquired = equipment.date_acquired,
        rest_duration = equipment.rest_duration,
        status = equipment.status
    )

    db.add(new_equipment)
    db.commit()
    db.refresh(new_equipment)
    return new_equipment

@router.get("/", response_model=EquipmentListResponse,)
def get_equipments(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    _: Users = Depends(permissions.require_admin_or_manager),
    __: Users = Depends(permissions.allow_active_staff)
):
    total = db.query(Equipments).count()
    pages = math.ceil(total / limit)
    offset = (page - 1) * limit
    equipments = db.query(Equipments).order_by(Equipments.created_at.desc()).offset(offset).limit(limit).all()
  
    return equipments


@router.get("/{id}", response_model=EquipmentResponse)
def get_job_by_id(
    equipment: Equipments = Depends(get_equipment_by_id),
    _: Users = Depends(permissions.require_admin_or_manager),
    __: Users = Depends(permissions.allow_active_staff)
):
    return equipment

@router.patch("/{id}", response_model=EquipmentResponse)
def update_equipment(
    update_details: UpdateEquipment,
    verified_equipment: Equipments = Depends(get_equipment_by_id),
    db: Session = Depends(get_db),
    _: Users = Depends(permissions.require_admin),
    __: Users = Depends(permissions.allow_active_staff)
):
    updated = update_details.model_dump(exclude_unset=True)
    updated["updated_at"] = datetime.now(timezone.utc)
    for key, value in updated.items():
        setattr(verified_equipment, key, value)
    
    db.commit()
    db.refresh(verified_equipment)
    return verified_equipment

@router.delete("/{id}", response_model=EquipmentResponse)
def delete_equipment(
    equipment: Equipments = Depends(get_equipment_by_id),
    db: Session = Depends(get_db),
    _: Users = Depends(permissions.require_admin),
    __: Users = Depends(permissions.allow_active_staff)
):
    db.delete(equipment)
    db.commit()
    return equipment