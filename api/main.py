from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from api.dependencies.database import get_db
from api.models import models, schemas

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("", response_model=schemas.Order, status_code=status.HTTP_201_CREATED)
def create_order(payload: schemas.OrderCreate, db: Session = Depends(get_db)):
    obj = models.Order(**payload.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.get("", response_model=list[schemas.Order])
def read_orders(db: Session = Depends(get_db)):
    return db.query(models.Order).order_by(models.Order.id).all()


@router.get("/{order_id}", response_model=schemas.Order)
def read_one_order(order_id: int, db: Session = Depends(get_db)):
    obj = db.get(models.Order, order_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Order not found")
    return obj


@router.put("/{order_id}", response_model=schemas.Order)
def update_one_order(order_id: int, payload: schemas.OrderUpdate, db: Session = Depends(get_db)):
    obj = db.get(models.Order, order_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Order not found")

    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)

    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_one_order(order_id: int, db: Session = Depends(get_db)):
    obj = db.get(models.Order, order_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Order not found")
    db.delete(obj)
    db.commit()
