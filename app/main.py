import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.logging_config import setup_logging
from app.middleware import RequestLoggerMiddleware
from app.routers import auth, users, blogs
from app.seeder import create_tables, seed_database

# Boot logging before anything else
setup_logging()
logger = logging.getLogger("app.main")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("App started")
    yield
    logger.info("App shutting down")


app = FastAPI(
    title="Blog API",
    description="A FastAPI blog application with user auth and CRUD for blogs",
    version="1.0.0",
    lifespan=lifespan,
)

# Request logger must be added BEFORE CORSMiddleware so every request is captured
app.add_middleware(RequestLoggerMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.critical(
        "Unhandled exception on %s %s: %s",
        request.method,
        request.url.path,
        exc,
        exc_info=True,
    )
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )


app.include_router(auth.router)
app.include_router(users.router)
app.include_router(blogs.router)


@app.get("/", tags=["Health"])
def root():
    return {"message": "API is running"}


@app.post("/seed", tags=["Health"])
def seed():
    from app.database import SessionLocal
    from app import models

    create_tables()
    db = SessionLocal()
    try:
        if db.query(models.User).first():
            logger.info("POST /seed called — data already exists, skipping")
            return {"message": "Already seeded, skipping"}
    finally:
        db.close()

    seed_database()
    logger.info("POST /seed called — database seeded successfully")
    return {"message": "Database seeded!"}
