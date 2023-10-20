from fastapi import APIRouter, Depends, HTTPException
from ourapp.schema import BlogCreate, Blog, User, UserCreate  
from datetime import datetime
import csv

router = APIRouter()

csv_file = "blog_data.csv"

def load_from_csv():
    data = []
    try:
        with open(csv_file, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append(Blog(**row))  
    except FileNotFoundError:
        data = []  
    return data

blogs_db = load_from_csv()

def save_to_csv(data):
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["id", "title", "body", "author_id", "created_at"])
        for item in data:
            writer.writerow([item.id, item.title, item.body, item.author_id, item.created_at])


@router.post("/blogs", response_model=Blog)
def create_blog(blog: BlogCreate, current_user: User = Depends()): 
    blog_id = len(blogs_db) + 1
    new_blog = Blog(id=blog_id, title=blog.title, body=blog.body, author_id=current_user.id, created_at=str(datetime.now()))
    
    blogs_db.append(new_blog)
    
    save_to_csv(blogs_db)
    
    return new_blog

@router.get("/blogs", response_model=list[Blog])
def list_blogs():
    blogs_db = load_from_csv()
    return blogs_db

@router.get("/blogs/{blog_id}", response_model=Blog)
def get_blog(blog_id: int):
    if 1 <= blog_id <= len(blogs_db):
        return blogs_db[blog_id - 1]
    else:
        raise HTTPException(status_code=404, detail="Blog not found")

@router.put("/blogs/{blog_id}", response_model=Blog)
def edit_blog(blog_id: int, blog: BlogCreate, current_user: User = Depends()):
    if 1 <= blog_id <= len(blogs_db):
        edited_blog = blogs_db[blog_id - 1]
        edited_blog.title = blog.title
        edited_blog.body = blog.body
        edited_blog.created_at = str(datetime.now())  

        save_to_csv(blogs_db)

        return edited_blog
    else:
        raise HTTPException(status_code=404, detail="Blog not found")

@router.delete("/blogs/{blog_id}")
def delete_blog(blog_id: int, current_user: User = Depends()):
    if 1 <= blog_id <= len(blogs_db):
        deleted_blog = blogs_db.pop(blog_id - 1)

        save_to_csv(blogs_db)

        return {"message": "Blog deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Blog not found")
