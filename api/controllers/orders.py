from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from api.dependencies.database import get_db
from api.models import models, schemas

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("", response_model=schemas.Order, status_code=status.HTTP_201_CREATED)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    return orders.create(db=db, order=order)  # if you have service/helpers; or do inline DB ops

@router.get("", response_model=list[schemas.Order])
def read_orders(db: Session = Depends(get_db)):
    return orders.read_all(db)  # or inline

@router.get("/{order_id}", response_model=schemas.Order)
def read_one_order(order_id: int, db: Session = Depends(get_db)):
    obj = orders.read_one(db, order_id=order_id)  # or inline
    if obj is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return obj

@router.put("/{order_id}", response_model=schemas.Order)
def update_one_order(order_id: int, order: schemas.OrderUpdate, db: Session = Depends(get_db)):
    obj = orders.read_one(db, order_id=order_id)  # or inline
    if obj is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return orders.update(db=db, order=order, order_id=order_id)

@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_one_order(order_id: int, db: Session = Depends(get_db)):
    obj = orders.read_one(db, order_id=order_id)  # or inline
    if obj is None:
        raise HTTPException(status_code=404, detail="Order not found")
    orders.delete(db=db, order_id=order_id)