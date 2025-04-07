
from .. import models, schemas, utils
from fastapi import FastAPI, Response, status, HTTPException, APIRouter
from fastapi import Body, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import SessionLocal, get_db
from ..schemas import UserCreate, UserOut, PostCreate, Post, PostOut
from .. import oauth2
from typing import List, Optional
##DEPENDS expects a callable function not the result of the function 
##DEPPENDS works as a injection dependency routing the operations which have to be executed before we actually execute the test_post function
router = APIRouter(
    prefix="/posts", 
    tags=['Posts']
)

@router.get("/sqlalchemy")
def test_post(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    print(posts)
    return posts
    
#{{URL}}posts?limit=2&skip=2&search=again => query parameters
#@router.get("/", response_model=List[Post])
@router.get("/", response_model=List[PostOut])
def get_posts(db: Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    print(limit)
    #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    results = db.query(models.Post, func.count(models.Votes.post_id).label("votes")).join(models.Votes, models.Votes.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    print(results)
    
    return results

##this is how we change the default status code for a operation
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Post)
def create_posts(post: PostCreate, db: Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_user)):
    #cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    ##getting the returning * values  
    #new_post = cursor.fetchone() 
    #conn.commit()
    print(post.dict())
    ##**post.dict() is the same as post.title, post.content, post.published (it automatically unpacks the dictionary)
    print(current_user.id)
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

##getting a single post 
##A path parameter is always a string, so we need to convert it to an int.
@router.get("/{id}", response_model=PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_user)):
    print(current_user)
    #post = db.query(models.Post).filter(models.Post.id == id).first() 
    post = db.query(models.Post, func.count(models.Votes.post_id).label("votes")).join(models.Votes, models.Votes.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first() 
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    return post

##Deleting the post 
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db: Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_user)):
    ##remember %s is the placeholder for the value in the sql statement
    #cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", str(id))
    #deleted = cursor.fetchone()
    #conn.commit()
    #if deleted == None:
    #    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    #return Response(status_code=status.HTTP_204_NO_CONTENT)
    print(current_user)
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    

    ##this is going to check if the post owner id is the same as the current user id
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    

    post_query.delete(synchronize_session=False)
    db.commit()

@router.put("/{id}", response_model=Post)
def update_post(id:int, updated_post:PostCreate, db: Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_user)):
    #cursor.execute("""UPDATE posts SET title= %s, content = %s, published= %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id)))
    #updated_post = cursor.fetchone()
    #conn.commit()
    #if updated_post == None:
    #    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    #return {"data": updated_post}
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    ##post_query takes in the updated fields as a dictionary
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()
