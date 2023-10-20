from fastapi import APIRouter, Depends, HTTPException
from ourapp.schema import CommentCreate, Comment, User, Blog
import csv
from datetime import datetime

router = APIRouter()

csv_file = "comment_data.csv"

def load_from_csv():
    data = []
    try:
        with open(csv_file, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append(Comment(**row))  
    except FileNotFoundError:
        data = []  
    return data

comments_db = load_from_csv()

def save_to_csv(data):
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["id", "text", "blog_id", "author_id", "created_at"])
        for item in data:
            writer.writerow([item.id, item.text, item.blog_id, item.author_id, item.created_at])

@router.post("/comments", response_model=Comment)
def create_comment(comment: CommentCreate, current_user: User = Depends()):
    comment_id = len(comments_db) + 1
    new_comment = Comment(
        id=comment_id,
        text=comment.text,
        blog_id=comment.blog_id,
        author_id=comment.author_id,
        created_at=str(datetime.now())
    )
    
    comments_db.append(new_comment)
    
    save_to_csv(comments_db)
    
    return new_comment

@router.get("/comments/{comment_id}", response_model=Comment)
def get_comment(comment_id: int):
    if 1 <= comment_id <= len(comments_db):
        return comments_db[comment_id - 1]
    else:
        raise HTTPException(status_code=404, detail="Comment not found")

@router.put("/comments/{comment_id}", response_model=Comment)
def edit_comment(comment_id: int, comment: CommentCreate, current_user: User = Depends()):
    if 1 <= comment_id <= len(comments_db):
        edited_comment = comments_db[comment_id - 1]
        if edited_comment.author_id != current_user.id:
            raise HTTPException(status_code=403, detail="Permission denied")
        
        edited_comment.text = comment.text

        save_to_csv(comments_db)

        return edited_comment
    else:
        raise HTTPException(status_code=404, detail="Comment not found")

@router.delete("/comments/{comment_id}")
def delete_comment(comment_id: int, current_user: User = Depends()):
    if 1 <= comment_id <= len(comments_db):
        deleted_comment = comments_db.pop(comment_id - 1)
        
        if deleted_comment.author_id != current_user.id:
            raise HTTPException(status_code=403, detail="Permission denied")

        save_to_csv(comments_db)

        return {"message": "Comment deleted successfully"}

@router.get("/comments", response_model=list[Comment])
def list_comments():
    return comments_db

@router.get("/comments/user/{user_id}", response_model=list[Comment])
def get_user_comments(user_id: int):
    user_comments = [comment for comment in comments_db if comment.author_id == user_id]
    return user_comments

@router.get("/comments/blog/{blog_id}", response_model=list[Comment])
def get_blog_comments(blog_id: int):
    blog_comments = [comment for comment in comments_db if comment.blog_id == blog_id]
    return blog_comments

@router.get("/comments/user/{user_id}", response_model=list[Comment])
def get_user_comments(user_id: int):
    user_comments = [comment for comment in comments_db if comment.author_id == user_id]
    return user_comments

@router.get("/comments/blog/{blog_id}", response_model=list[Comment])
def get_blog_comments(blog_id: int):
    blog_comments = [comment for comment in comments_db if comment.blog_id == blog_id]
    return blog_comments

@router.get("/comments/blog/{blog_id}", response_model=list[Comment])
def get_blog_comments(blog_id: int):
    blog_comments = [comment for comment in comments_db if comment.blog_id == blog_id]
    return blog_comments

@router.get("/comments/user/{user_id}/blog/{blog_id}", response_model=list[Comment])
def get_user_blog_comments(user_id: int, blog_id: int):
    user_blog_comments = [comment for comment in comments_db if comment.author_id == user_id and comment.blog_id == blog_id]
    return user_blog_comments
