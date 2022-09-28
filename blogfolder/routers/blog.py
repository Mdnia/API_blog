from fastapi import APIRouter, Depends, status, HTTPException, Response
from typing import List

import schemas
import database
import models
#from repository import blog as bl
from .repository import blog

from sqlalchemy.orm import Session



router = APIRouter(
    prefix='/blog',
    tags=['Blogs']
)



@router.get("/", response_model=List[schemas.ShowBlog])
async def all(db: Session = Depends(database.get_db)):
    return blog.get_all(db)



@router.post("/", status_code=status.HTTP_201_CREATED)
async def create(blog: schemas.Blogs, db: Session = Depends(database.get_db)):
    new_blog = models.Blog(title=blog.title, body=blog.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog



@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def destroy(id, db: Session = Depends(database.get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")
    blog.delete(synchronize_session=False)
    db.commit()
    return {"done"}


@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
async def update(id, request: schemas.Blogs, db: Session = Depends(database.get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")
    blog.update(request, synchronize_session=False)
    db.commit()
    return "Updated title"




@router.get("/{id}", status_code=200, response_model=schemas.ShowBlog)
async def show(id, db: Session = Depends(database.get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with the id {id} is not available")

    return blog



'''
if __name__ == '__main__':

    import sys


    print(sys.path)
'''