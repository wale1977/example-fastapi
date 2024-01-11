from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import  Session
from .. import schemas, models, utils
from ..database import get_db

router = APIRouter(
    prefix="/users",
    tags = ["Users"]  # This groups the routes under Users
    )

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.GetUsers)
def create_user(user: schemas.CreateUser, db: Session = Depends(get_db)):
       
    # harshing the password
    user.password = utils.hashing(user.password) # hashing function is from utils file
    
    new_user = models.User(**user.dict())    
    
    db.add(new_user) # add entry to database
    db.commit()      # commit entry
    db.refresh(new_user) # return entry and store in new_post

    return new_user

''' 
The following show how to use passlib package and bcrypt algorithm
        >>> from passlib.hash import bcrypt

        >>> # generate new salt, hash password
        >>> h = bcrypt.hash("password")
        >>> h
        '$2a$12$NT0I31Sa7ihGEWpka9ASYrEFkhuTNeBQ2xfZskIiiJeyFXhRgS.Sy'

        >>> # the same, but with an explicit number of rounds
        >>> bcrypt.using(rounds=13).hash("password")
        '$2b$13$HMQTprwhaUwmir.g.ZYoXuRJhtsbra4uj.qJPHrKsX5nGlhpts0jm'

        >>> # verify password
        >>> bcrypt.verify("password", h)
        True
        >>> bcrypt.verify("wrong", h)
        False

'''
@router.get("/{id}", response_model=schemas.GetUsers)
def get_user(id: int, db: Session = Depends(get_db)):
    
    user = db.query(models.User).filter(models.User.id == id).first()
    
    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="User with id: {id} does not exists")
    
    return user