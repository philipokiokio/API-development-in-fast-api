from fastapi import FastAPI, Response,status
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange



app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool=True
    rating : Optional[int] = None



my_post = [{"title":"Title of a post 1", "content":"content of post 1", "id":1}, 
          {"title":"favorite foods", "content": "I like food", "id":2}
          ]


@app.get("/")
async def root():
    return {"Message": "Welcome to my API!"}




@app.post('/posts',status_code = status.HTTP_201_CREATED)
def create_post(post:Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(1,1000000)
    my_post.append(post_dict)
    print(post_dict)
    return {"data":"New Post","payload":post_dict}

@app.delete("/posts/{id}")
def delete_post(id:int, response:Response):
    for i, p in enumerate(my_post):
        if p["id"]== id:
            my_post.pop(i)
            response.status_code = status.HTTP_204_NO_CONTENT
            return { }
        else:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {
                "message": f"Post with id {id} does not exists"
            }


@app.get('/posts')
def get_posts():
    return {"data":my_post}

@app.get('/posts/{id}')
def get_post(id:int,response: Response):
    print(id)
    for p in my_post:
        if p["id"] == id:
            return {"data": p}
    response.status_code = status.HTTP_404_NOT_FOUND
    return {"data":f"{id} does not exist"}









@app.put('/posts/{id}')
def put_post(id:int):
    pass