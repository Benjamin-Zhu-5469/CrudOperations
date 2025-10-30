from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from api.dependencies.database import get_db
from api.models import models
from api.models.schemas import SandwichCreate, SandwichUpdate, SandwichOut

router = APIRouter(prefix="/sandwiches", tags=["sandwiches"])

@router.post("", response_model=SandwichOut, status_code=status.HTTP_201_CREATED)
def create(data: SandwichCreate, db: Session = Depends(get_db)):
    exists = db.query(models.Sandwich).filter(models.Sandwich.name == data.name).first()
    if exists:
        raise HTTPException(status_code=409, detail="Sandwich name already exists")
    obj = models.Sandwich(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@router.get("", response_model=list[SandwichOut])
def read_all(db: Session = Depends(get_db)):
    return db.query(models.Sandwich).order_by(models.Sandwich.id).all()

@router.get("/{sandwich_id}", response_model=SandwichOut)
def read_one(sandwich_id: int, db: Session = Depends(get_db)):
    obj = db.get(models.Sandwich, sandwich_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Sandwich not found")
    return obj

@router.put("/{sandwich_id}", response_model=SandwichOut)
def update(sandwich_id: int, data: SandwichUpdate, db: Session = Depends(get_db)):
    obj = db.get(models.Sandwich, sandwich_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Sandwich not found")
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj

@router.delete("/{sandwich_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(sandwich_id: int, db: Session = Depends(get_db)):
    obj = db.get(models.Sandwich, sandwich_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Sandwich not found")
    db.delete(obj)
    db.commit()