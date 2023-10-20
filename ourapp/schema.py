from pydantic import BaseModel

class UserCreate(BaseModel):
    email: str
    first_name: str
    last_name: str
    username: str
    password: str

class User(UserCreate):
    id: int

class BlogCreate(BaseModel):
    title: str
    body: str

class Blog(BlogCreate):
    id: int
    author_id: int
    created_at: str

class CommentCreate(BaseModel):
    id: int
    text: str
    blog_id: int
    author_id: int

class Comment(CommentCreate):
    id: int
    created_at: str