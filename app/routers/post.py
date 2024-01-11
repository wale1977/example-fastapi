from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import  Session
from typing import Optional, List
from sqlalchemy import func
from sqlalchemy.sql import text

from .. import schemas, models
from ..database import get_db
from .. import models,schemas, utils, oauth2


router = APIRouter(
    prefix="/posts",
    tags = ["Posts"]
    )

# @router.get("/") # List from the typing package
# @router.get("/", response_model=List[schemas.Post]) # List from the typing package
@router.get("/", response_model=List[schemas.PostOut]) # List from the typing package
# def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit:int=10, skip:int=0, search:Optional[str]=""):
       
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("post_likes")).join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    # results = list ( map (lambda x : x._mapping, results) )
    
    # print(results)
    
    # posts = db.query(models.Post).limit(limit).offset(skip).all()
    # posts = db.query(models.Post).limit(limit).all()
    # posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all() # This gets all posts by the current user.
    
    # print(current_user.email)

# def get_posts():

    # posts = db.execute(text(
    #     'select posts.*, COUNT(votes.post_id) as vote_likes from posts LEFT JOIN votes ON posts.id=votes.post_id GROUP BY posts.id'
    # ))
    
    # results = []
    
    # for post in posts:
    #     results.append(dict(post))
    
    # print(results)
    # -----------------------------------------------------------------------
    
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
# def create_posts(n_post: schemas.CreatePost, db: Session = Depends(get_db)):
def create_posts(n_post: schemas.CreatePost, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # new_post = models.Post(title=n_post.title, content=n_post.content, published=n_post.published) # creates new entry
    
    # print(n_post.dict())
    # print(current_user.email)
    
    new_post = models.Post(**n_post.dict(), owner_id=current_user.id) #this converts n_post to dictionary and unpacked it key-value pairs
    
    db.add(new_post) # add entry to database
    db.commit()      # commit entry
    db.refresh(new_post) # return entry and store in new_post

# def create_posts(n_post: Post ):
#     cursor.execute("""INSERT INTO posts(title, content, published) VALUES(%s, %s, %s) RETURNING * """, (n_post.title, n_post.content, n_post.published))
    
#     new_post = cursor.fetchone()
#     conn.commit()  # write data into database
    
    # post_dict = n_post.dict()
    # post_dict['id'] = randrange(0, 1000000)
    
    # my_posts.append(post_dict)
    return new_post
    
@router.get("/{id}", response_model=schemas.PostOut)
# def get_post(id: int, response: Response):
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # post = find_post(id)
    
    # cursor.execute("SELECT * FROM posts WHERE id= %s", (str(id)))
    # post = cursor.fetchone()
    
    # post = db.query(models.Post).filter(models.Post.id == id).first()
    
    post = db.query(models.Post, func.count(models.Vote.post_id).label("post_likes")).join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id}, was not found")
        response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id: {id}, was not found"}
        
    # if post.owner_id != current_user.id:
    #     raise  HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action.")
    
    return post
    

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # find the index in the array that has the required Id
    # index = find_post_index(id)
    
    # cursor.execute("""DELETE FROM posts WHERE id= %s RETURNING *""",(str(id)))
    # deleted_post = cursor.fetchone()
    
    # conn.commit()
    
    post = db.query(models.Post).filter(models.Post.id == id)
    
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    
   
    if post.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
        
    post.delete()
    db.commit()
    # delete the post
    # my_posts.pop(index)
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    

@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, update_post: schemas.UpdatePost, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # index = find_post_index(id)
    # cursor.execute("UPDATE posts SET title = %s, content = %s, published = %s WHERE id=%s RETURNING *", (post.title, post.content, post.published, str(id)))
    
    # updated_post = cursor.fetchone()
    # conn.commit()
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    # print(post_query)
    post = post_query.first()
    # print(update_post.dict())
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requed action")
        
    post_query.update(update_post.dict(), synchronize_session=False)
    
    db.commit()
    
    # post_dict = post.dict()
    # post_dict['id'] = id
    # my_posts[index] = post_dict
    
    return post_query.first()
