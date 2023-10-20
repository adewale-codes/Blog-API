from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from ourapp.schema import UserCreate, User, Blog 
import csv
from datetime import datetime

router = APIRouter()

csv_file = "user_data.csv"


def load_from_csv():
    data = {}
    try:
        with open(csv_file, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                user = User(**row)  
                data[user.username] = user
    except FileNotFoundError:
        data = {}  
    return data

user_db = {}
blogs_db = []

def save_user_to_csv(user):
    with open(csv_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["User", user.id, user.email, user.first_name, user.last_name, user.username, user.password])

@router.post("/register", response_model=User)
def register_user(user: UserCreate):
    user_id = len(user_db) + 1
    new_user = User(id=user_id, email=user.email, first_name=user.first_name, last_name=user.last_name, username=user.username, password=user.password)
    user_db[user.username] = new_user
    save_user_to_csv(new_user)
    return new_user

@router.post("/login")
def login_user(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username not in user_db:
        raise HTTPException(status_code=400, detail="User not found")

    user = user_db[form_data.username]
    if form_data.password != user.password:
        raise HTTPException(status_code=400, detail="Incorrect password")

    return {"message": "Login successful", "user": user}

@router.get("/users", response_model=list[User])
def list_users():
    users = list(user_db.values())
    return users

@router.get("/users/{user_id}", response_model=User)
def get_user(user_id: int):
    if user_id in user_db:
        return user_db[user_id]
    else:
        raise HTTPException(status_code=404, detail="User not found")

@router.get("/users/{user_id}/blogs", response_model=list[Blog])
def get_user_blogs(user_id: int):
    user_blogs = [blog for blog in blogs_db if blog.author_id == user_id]
    return user_blogs
