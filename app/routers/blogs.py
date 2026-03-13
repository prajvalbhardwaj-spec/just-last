import logging
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app import models
from app.schemas import BlogCreate, BlogUpdate, BlogOut
from app.auth import get_current_user

router = APIRouter(prefix="/blogs", tags=["Blogs"])
logger = logging.getLogger("app.blogs")


@router.post("/", response_model=BlogOut, status_code=status.HTTP_201_CREATED)
def create_blog(
    payload: BlogCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    blog = models.Blog(
        title=payload.title,
        content=payload.content,
        owner_id=current_user.id,
    )
    db.add(blog)
    db.commit()
    db.refresh(blog)
    return blog


@router.get("/", response_model=List[BlogOut])
def list_blogs(db: Session = Depends(get_db)):
    return db.query(models.Blog).all()


@router.get("/{blog_id}", response_model=BlogOut)
def get_blog(blog_id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if not blog:
        logger.warning("Blog not found: id=%d", blog_id)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")
    return blog


@router.put("/{blog_id}", response_model=BlogOut)
def update_blog(
    blog_id: int,
    payload: BlogUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if not blog:
        logger.warning("Blog not found for update: id=%d", blog_id)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")
    if blog.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this blog",
        )
    if payload.title is not None:
        blog.title = payload.title
    if payload.content is not None:
        blog.content = payload.content
    db.commit()
    db.refresh(blog)
    return blog


@router.delete("/{blog_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(
    blog_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if not blog:
        logger.warning("Blog not found for delete: id=%d", blog_id)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")
    if blog.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this blog",
        )
    db.delete(blog)
    db.commit()
