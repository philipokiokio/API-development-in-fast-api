
from ..schemas import UserResponse, UserCreate
from ..database import get_db
from ..utils import hash_pass
from sqlalchemy.orm import Session 
from fastapi import Depends, Response, status, APIRouter, HTTPException
from .. import models 



router = APIRouter(prefix= '/user', tags=['Users'])



@router.post('/', status_code = status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(user:UserCreate,db: Session = Depends(get_db)):

    # hash the password -userpassword
    hashed_password = hash_pass(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user



@router.get('/{id}', response_model=UserResponse)
def get_user(id:int, db: Session = Depends(get_db)):
    user_check = db.query(models.User).filter(models.User.id == id)  
    if user_check.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with the id: {id} was not found")

    return user_check.first()