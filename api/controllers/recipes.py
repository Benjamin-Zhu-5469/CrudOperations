from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from api.dependencies.database import get_db
from api.models import models, schemas

router = APIRouter(prefix="/recipes", tags=["Recipes"])


@router.post("", response_model=schemas.Recipe, status_code=status.HTTP_201_CREATED)
def create_recipe(payload: schemas.RecipeCreate, db: Session = Depends(get_db)):
    obj = models.Recipe(**payload.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.get("", response_model=list[schemas.Recipe])
def read_recipes(db: Session = Depends(get_db)):
    return db.query(models.Recipe).order_by(models.Recipe.id).all()


@router.get("/{recipe_id}", response_model=schemas.Recipe)
def read_one_recipe(recipe_id: int, db: Session = Depends(get_db)):
    obj = db.get(models.Recipe, recipe_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return obj


@router.put("/{recipe_id}", response_model=schemas.Recipe)
def update_one_recipe(recipe_id: int, payload: schemas.RecipeUpdate, db: Session = Depends(get_db)):
    obj = db.get(models.Recipe, recipe_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Recipe not found")

    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)

    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/{recipe_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_one_recipe(recipe_id: int, db: Session = Depends(get_db)):
    obj = db.get(models.Recipe, recipe_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Recipe not found")
    db.delete(obj)
    db.commit()
