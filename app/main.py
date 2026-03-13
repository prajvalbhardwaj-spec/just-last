from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import auth, users, blogs


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("App started")
    yield
    print("App shutting down")


app = FastAPI(
    title="Blog API",
    description="A FastAPI blog application with user auth and CRUD for blogs",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(blogs.router)


@app.get("/", tags=["Health"])
def root():
    return {"message": "API is running"}
