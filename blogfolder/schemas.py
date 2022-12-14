from pydantic import BaseModel
from typing import List, Union

class BlogBase(BaseModel):
    title: str
    body: str

class Blogs(BlogBase):
    class Config:
        orm_mode = True

class User(BaseModel):
    name: str
    email: str
    password: str


class ShowUser(BaseModel):
    name: str
    email: str
    blogs: List[Blogs] = []

    class Config:
        orm_mode = True


class ShowBlog(BaseModel):
    title: str
    body: str
    creator: ShowUser

    class Config:
        orm_mode = True


class Login(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


