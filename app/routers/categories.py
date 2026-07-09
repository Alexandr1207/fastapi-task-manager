from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException, Path, status

from sqlalchemy.orm import Session

from database.database import get_db
from services.category_service import get_categories_db, create_category_db, delete_category_db, get_category_by_id_db, update_category_db
from schemas.tasks import Category_schema




router = APIRouter(prefix='/categories', tags=['Categories'])


@router.get('/', 
            response_model=list[Category_schema], 
            status_code=status.HTTP_200_OK,
            summary='Get categories'
            )
async def get_categories(db: Session = Depends(get_db)):
    return get_categories_db(db=db)


@router.get('/{cat_id}',
            response_model=Category_schema, 
            status_code=status.HTTP_200_OK,
            summary='Get category by id')
async def get_category_by_id(cat_id: Annotated[int, Path(gt=0)], db: Session = Depends(get_db)):
    category = get_category_by_id_db(db=db, cat_id=cat_id)
    if category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    return category


@router.post('/', 
             response_model=Category_schema,
             status_code=status.HTTP_201_CREATED,
             summary="Create category"
             )
async def create_category(category: Annotated[Category_schema, Body()], db: Session = Depends(get_db)):
    category = category.model_dump()
    return create_category_db(db=db, category=category)


@router.delete('/{cat_id}', status_code=status.HTTP_200_OK, summary="Delete category")
async def delete_category(cat_id: Annotated[int, Path(gt=0)], db: Session = Depends(get_db)):
    cat = get_category_by_id_db(db=db, cat_id=cat_id)
    if cat is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    delete_category_db(db=db, cat_id=cat_id)
    return {'message': 'Category deleted successfully'}


@router.patch(
        '/{cat_id}', 
        response_model=Category_schema, 
        status_code=status.HTTP_200_OK,
        summary='Update task'
        )
async def update_category(cat_id: Annotated[int, Path(gt=0)], category: Annotated[Category_schema, Body()], db: Session = Depends(get_db)):
    cat_dict = category.model_dump(exclude_unset=True)
    category = update_category_db(db=db, cat_id=cat_id, cat_dict=cat_dict)
    if category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    return category