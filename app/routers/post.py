
from .. import oauth2
from ..schemas import  PostCreate, Post, PostOut
from typing import List
from fastapi import Depends, status, HTTPException, Response, APIRouter
from .. import models
from fastapi.params import Body
from sqlalchemy.orm import Session
from  sqlalchemy import func
from ..database import get_db
from typing import Optional





router = APIRouter(prefix='/posts', tags=['Posts'])















@router.post('/',status_code = status.HTTP_201_CREATED, response_model = Post)
def create_post(post:PostCreate, db: Session = Depends(get_db), current_user: int= Depends(oauth2.get_current_user)):

    # cursor.execute("""insert into post (title,content,published) values (%s,%s,%s) returning * """,
    #      (post.title,post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
 
    print(current_user.email)
    new_post = models.Post(owner_id=current_user.id,**post.dict())
    

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return  new_post


@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db: Session= Depends(get_db), current_user: int= Depends(oauth2.get_current_user)):

    # cursor.execute(''' delete from post where id = %s returning * ''', (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"Post with id {id} does not exists")
    if post.owner_id != oauth2.get_current_user.id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= f"Request Unauthorized")

    post_query.delete(synchronize_session = False)
    db.commit()
    return Response(status_code = status.HTTP_204_NO_CONTENT)
    
  


@router.get('/', response_model = List[PostOut])
def get_posts(db: Session = Depends(get_db), limit:int=10, skip:int=0, search: Optional[str]=""):
    # cursor.execute("""select * from post """)
    # posts = cursor.fetchall()
    # posts =db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
        models.Post.title.contains(search)).limit(limit).offset(skip).all()
 
    return posts

@router.get('/{id}', response_model = PostOut)
def get_post(id:int, db: Session= Depends(get_db)):

    # cursor.execute('''select * from post where id = %s ''', (str(id),))
    # post= cursor.fetchone()

    # post = db.query(models.Post).filter(models.Post.id == id).first()
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(
            models.Post.id).filter(
            models.Post.id == id
        ).first()
    
    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, 
            detail=f"Post with Id: {id} was not found")
    return post



  





@router.put('/{id}', response_model = Post)
def update_post(id:int, post: PostCreate, db: Session= Depends(get_db), current_user: int= Depends(oauth2.get_current_user)):
    # cursor.execute(
    #     '''update post set title=%s, content=%s, published=%s where id= %s returning * ''',
    #  (post.title,post.content,post.published, str(id),)
    #  )
    # updated_post  = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id== id)
    post_q = post_query.first()
  
    


    if post_q == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
        detail=f"Post with id: {id} does not exist")
    


    if  post_q.owner_id != current_user.id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail='Request Unauthorized') 

    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return  post_query.first()

