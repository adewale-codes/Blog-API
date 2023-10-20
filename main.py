from fastapi import FastAPI
from ourapp.routes import user, blog, comment  


app = FastAPI()

app.include_router(user.router, prefix="/users", tags=["users"])
app.include_router(blog.router, prefix="/blogs", tags=["blogs"])
app.include_router(comment.router, prefix="/comments", tags=["comments"])

@app.get("/")
async def read_root():
    return {"message": "Welcome to Adewale Sulaiman FastAPI Blog App"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
