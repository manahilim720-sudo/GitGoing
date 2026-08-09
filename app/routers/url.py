from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
import random
import string
from .. import models, oauth2
from ..database import get_db

router = APIRouter(tags=['URLs'])

class URLCreate(BaseModel):
    original_url: str
    custom_alias: Optional[str] = None

class URLResponse(BaseModel):
    id: int
    original_url: str
    short_code: str
    click_count: int
    created_at: datetime
    class Config:
        from_attributes = True

def generate_short_code(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

@router.post("/urls", status_code=status.HTTP_201_CREATED, response_model=URLResponse)
def create_url(url: URLCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    if url.custom_alias:
        existing = db.query(models.URL).filter(models.URL.short_code == url.custom_alias).first()
        if existing:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This alias is already taken")
        code = url.custom_alias
    else:
        code = generate_short_code()
        while db.query(models.URL).filter(models.URL.short_code == code).first():
            code = generate_short_code()

    new_url = models.URL(original_url=url.original_url, short_code=code, owner_id=current_user)
    db.add(new_url)
    db.commit()
    db.refresh(new_url)
    return new_url

@router.get("/urls", response_model=List[URLResponse])
def get_my_urls(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    urls = db.query(models.URL).filter(models.URL.owner_id == current_user).all()
    return urls

@router.delete("/urls/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_url(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    url_query = db.query(models.URL).filter(models.URL.id == id)
    url = url_query.first()
    if url is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="URL not found")
    if url.owner_id != current_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    url_query.delete(synchronize_session=False)
    db.commit()

@router.put("/urls/{id}", response_model=URLResponse)
def update_url(id: int, url_update: URLCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    url_query = db.query(models.URL).filter(models.URL.id == id)
    url = url_query.first()
    if url is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="URL not found")
    if url.owner_id != current_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    url_query.update({"original_url": url_update.original_url}, synchronize_session=False)
    db.commit()
    return url_query.first()

@router.get("/{short_code}")
def redirect_url(short_code: str, db: Session = Depends(get_db)):
    url = db.query(models.URL).filter(models.URL.short_code == short_code).first()
    if url is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Short URL not found")
    url.click_count += 1
    db.commit()
    return RedirectResponse(url=url.original_url)