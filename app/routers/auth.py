from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from .. import database, schemas, models, utils, oauth2

router = APIRouter(tags=["Authentication"])

@router.post("/login", response_model = schemas.Token)
# def login(user_credentials: schemas.UserLogin,db: Session = Depends(database.get_db)):
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    
    # OAuth2PasswordRequestForm sends dict of {'username': 'ydjd', 'password': 'siiiei'} for user_credentials
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Username: Invalid Credential")
    
    
    if not utils.verify_password(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Password: Invalid Credential")
    
    # create a token
    access_token = oauth2.create_access_token(data = {"user_id": user.id}) # you can add some other details lie name, role etc
    # return the token
    return {"access_token": access_token, "token_type": "bearer"}