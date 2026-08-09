from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from datetime import datetime
from pydantic import BaseModel
from .. import models, utils
from ..database import get_db

router = APIRouter(prefix="/users", tags=['Users'])

class UserCreate(BaseModel):
    email: str
    password: str

class UserOut(BaseModel):
    id: int
    email: str
    created_at: datetime
    class Config:
        from_attributes = True

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user