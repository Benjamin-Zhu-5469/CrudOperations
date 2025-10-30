# api/controllers/orders.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from api.dependencies.database import get_db
from api.models import models, schemas

router = APIRouter(prefix="/orders", tags=["Orders"])

# ---------- CRUD helpers (local to this module) ----------

def create(db: Session, order: schemas.OrderCreate) -> models.Order:
    obj = models.Order(**order.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def read_all(db: Session) -> list[models.Order]:
    return db.query(models.Order).all()

def read_one(db: Session, order_id: int) -> models.Order | None:
    return db.query(models.Order).filter(models.Order.id == order_id).first()

def update(db: Session, order_id: int, order: schemas.OrderUpdate) -> models.Order:
    obj = read_one(db, order_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="Order not found")
    for k, v in order.dict(exclude_unset=True).items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj

def delete(db: Session, order_id: int) -> None:
    obj = read_one(db, order_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="Order not found")
    db.delete(obj)
    db.commit()

# ---------- Endpoints ----------

@router.post(
    "", 
    response_model=schemas.Order, 
    status_code=status.HTTP_201_CREATED
)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    return create(db=db, order=order)

@router.get(
    "", 
    response_model=list[schemas.Order]
)
def read_orders(db: Session = Depends(get_db)):
    return read_all(db=db)

@router.get(
    "/{order_id}", 
    response_model=schemas.Order
)
def read_one_order(order_id: int, db: Session = Depends(get_db)):
    obj = read_one(db=db, order_id=order_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return obj

@router.put(
    "/{order_id}", 
    response_model=schemas.Order
)
def update_one_order(order_id: int, order: schemas.OrderUpdate, db: Session = Depends(get_db)):
    return update(db=db, order_id=order_id, order=order)

@router.delete(
    "/{order_id}", 
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_one_order(order_id: int, db: Session = Depends(get_db)):
    delete(db=db, order_id=order_id)
