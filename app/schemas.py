from  pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

from pydantic.types import conint


#---------- Post Schema ------------------------------
# We're going to define a class, Post, which will extends BaseModel
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
   
    # rating: Optional[float] = None

# These next three classes inherit from the PostBase class
class CreatePost(PostBase):
    pass

class UpdatePost(PostBase):
    pass


class GetUsers(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    
    class Config:
        orm_mode: True


class  Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: GetUsers
    
    class Config:
        orm_mode: True

class PostOut(BaseModel):
    Post: Post
    post_likes: int
    
    # class Config:
    #     orm_mode: True
        
#------------- User Schema ------------------------

class CreateUser(BaseModel):
    email: EmailStr
    # using str, password will be stored in plain text. Therefore, we need to install password library and harshing algorith
    # used the command: pip install passlib[bcrypt]  - bcrypt is the one of the popular algorithm
    password: str 

        
class UserLogin(BaseModel):
    email: EmailStr
    password: str
    

class TokenData(BaseModel):
    id: Optional[int] = None
    
class Token(BaseModel):
    access_token: str
    token_type: str
    

class Vote(BaseModel):
    post_id: int
    direction: conint(le=1)
    