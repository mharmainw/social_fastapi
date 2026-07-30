from fastapi import HTTPException, status, Response, Depends, APIRouter
from .. import models 
from ..schemas import PostCreate,Post,PostOut
from ..database import get_db
from sqlalchemy.orm import Session
from .. import oauth2
from typing import Optional, List
from sqlalchemy import func

router = APIRouter(
    prefix = '/posts',
    tags = ['Posts']
)

@router.get('/',response_model=List[PostOut])
async def get_posts(db:Session = Depends(get_db), curr_user : int = Depends(oauth2.get_current_user), limit : int = 10, skip : int = 0, search: Optional[str] = ""):
    results = (
        db.query(
            models.Post,
            func.count(models.Vote.post_id).label("votes"),
        )
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
        .filter(models.Post.title.contains(search))
        .group_by(models.Post.id)
        .limit(limit)
        .offset(skip)
        .all()
    )
    return [{"Post": post, "votes": votes} for post, votes in results]



@router.get('/{id}',response_model=PostOut)
async def get_post(id : int, db:Session = Depends(get_db), curr_user : int = Depends(oauth2.get_current_user )):
    

    # how to do it without ORM

    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (id,))
    # get_post_byid = cursor.fetchone()
    # if not get_post_byid:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail=f"post with id {id} was not found",
    #     )
    # conn.commit()
    

    by_id = (
        db.query(
            models.Post,
            func.count(models.Vote.post_id).label("votes"),
        )
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
        .filter(models.Post.id == id)
        .group_by(models.Post.id)
        .first()
    )
    
    if not by_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} was not found",
        )

    
    
    post, votes = by_id
    return {"Post": post, "votes": votes}


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=Post)
async def create_posts(post: PostCreate,db:Session = Depends(get_db),curr_user : int = Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT into posts(title,content,published) VALUES (%s,%s,%s) RETURNING * """, (post.title,post.content,post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    
    post_dict = post.model_dump()
    new_post = models.Post(owner_id = curr_user.id ,**post_dict)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.delete('/{id}')
async def delete_post(id : int, db:Session = Depends(get_db), curr_user : int = Depends(oauth2.get_current_user)):


    # cursor.execute('''DELETE FROM posts WHERE id = %s RETURNING *''', (id,))
    # deleted_post = cursor.fetchone()

    deleted_post = db.query(models.Post).filter(models.Post.id == id)

    deleted_post_query = deleted_post.first()

    if deleted_post_query == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = f'post with id: {id} does not exist')

    if deleted_post_query.owner_id != curr_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail = f'Not Authorized to perform requested action')
    

    deleted_post.delete(synchronize_session = False)
    db.commit()
    
    # conn.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/{id}',response_model=Post)
async def update_post(id:int, updated_post:PostCreate,db:Session = Depends(get_db), curr_user   : int = Depends(oauth2.get_current_user)):
    # cursor.execute('''UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *''', (post.title, post.content, post.published, id))
    # updated_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f'post with id: {id} was not found')

    if post.owner_id != curr_user.id:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail = f'Not Authorized to perform requested action')


    post_query.update(updated_post.model_dump(),synchronize_session = False)
    db.commit()

    return post_query.first()


