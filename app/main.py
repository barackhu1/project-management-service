from fastapi import FastAPI
from app.routers import auth, projects, documents

app = FastAPI()

app.include_router(auth.router)
app.include_router(projects.router)
app.include_router(documents.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
