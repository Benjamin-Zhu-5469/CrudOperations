from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from api.dependencies.database import get_db
from api.models import models, schemas

router = APIRouter(prefix="/sandwiches", tags=["Sandwiches"])


@router.post("", response_model=schemas.Sandwich, status_code=status.HTTP_201_CREATED)
def create_sandwich(payload: schemas.SandwichCreate, db: Session = Depends(get_db)):
    existing = db.query(models.Sandwich).filter(models.Sandwich.name == payload.name).first()
    if existing:
        raise HTTPException(status_code=409, detail="Sandwich name already exists")

    obj = models.Sandwich(**payload.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.get("", response_model=list[schemas.Sandwich])
def read_sandwiches(db: Session = Depends(get_db)):
    return db.query(models.Sandwich).order_by(models.Sandwich.id).all()


@router.get("/{sandwich_id}", response_model=schemas.Sandwich)
def read_one_sandwich(sandwich_id: int, db: Session = Depends(get_db)):
    obj = db.get(models.Sandwich, sandwich_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Sandwich not found")
    return obj


@router.put("/{sandwich_id}", response_model=schemas.Sandwich)
def update_one_sandwich(sandwich_id: int, payload: schemas.SandwichUpdate, db: Session = Depends(get_db)):
    obj = db.get(models.Sandwich, sandwich_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Sandwich not found")

    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)

    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/{sandwich_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_one_sandwich(sandwich_id: int, db: Session = Depends(get_db)):
    obj = db.get(models.Sandwich, sandwich_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Sandwich not found")
    db.delete(obj)
    db.commit()
