from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()


# define what i want from a post request from a user
# title:str, content:str, id:int
class Post(BaseModel):
    title: str
    content: str
    # id: int
    published: bool = True
    rating: Optional[int] = None


my_posts = [
    {"title": "title of first post", "content": "content of first post", "id": 1},
    {"title": "favorite food", "content": "I love pounded yam", "id": 2},
    {"title": "Football", "content": "My favourite club is Manchester united", "id": 3}
]


# function to find post by id
def find_post(id):
    post_id = id
    for post in my_posts:
        if post["id"] == post_id:
            return post
        # return {"postDetail": f"here is your post:c{post} with id of {id}"}


# function to delete a post by id using enumerate
def find_index_post(id):
    for index, value in enumerate(my_posts):
        if value["id"] == id:
            return index


# function to get latest post
def get_latest():
    post = my_posts[len(my_posts) - 1]
    return post


@app.get("/")
def root():
    return {"message": "Welcome to my api"}


# retrieves all post from datastore


@app.get("/posts")
def get_post():
    return {"data": my_posts}


# adds new post to the datastore
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    # print(post.model_dump())
    post_dict = post.model_dump()
    post_dict["id"] = randrange(0, 1000000)
    my_posts.append(post_dict)
    return {"data": post_dict}


# gets latest post
@app.get("/posts/latest")
def get_latest_posts():
    post = get_latest()
    return {"LatestPost": post}


# gets a singular post by id from the database
@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    post = find_post(id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id of {id} not found"
        )
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return{"postDetail": f"Post with id of {id} not found"}
    return {"postDetail": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):

    index = find_index_post(id)

    if index == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} not found, please enter a valid id"
        )

    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):

    index = find_index_post(id)

    if index == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} not found, please enter a valid id"
        )
    # convert post data input to a python dictionary
    post_dict = post.model_dump()

    # adding id field, by setting id of the above post to the id used to find the post
    post_dict["id"] = id

    # replace old content with new content using the index
    my_posts[index] = post_dict

    return {"data": post_dict}
