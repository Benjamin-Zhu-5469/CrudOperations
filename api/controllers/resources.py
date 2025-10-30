from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from api.dependencies.database import get_db
from api.models import models, schemas

router = APIRouter(prefix="/resources", tags=["Resources"])


@router.post("", response_model=schemas.Resource, status_code=status.HTTP_201_CREATED)
def create_resource(payload: schemas.ResourceCreate, db: Session = Depends(get_db)):
    obj = models.Resource(**payload.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.get("", response_model=list[schemas.Resource])
def read_resources(db: Session = Depends(get_db)):
    return db.query(models.Resource).order_by(models.Resource.id).all()


@router.get("/{resource_id}", response_model=schemas.Resource)
def read_one_resource(resource_id: int, db: Session = Depends(get_db)):
    obj = db.get(models.Resource, resource_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Resource not found")
    return obj


@router.put("/{resource_id}", response_model=schemas.Resource)
def update_one_resource(resource_id: int, payload: schemas.ResourceUpdate, db: Session = Depends(get_db)):
    obj = db.get(models.Resource, resource_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Resource not found")

    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)

    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/{resource_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_one_resource(resource_id: int, db: Session = Depends(get_db)):
    obj = db.get(models.Resource, resource_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Resource not found")
    db.delete(obj)
    db.commit()
