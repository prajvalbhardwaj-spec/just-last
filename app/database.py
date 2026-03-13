import os
import logging
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy.exc import OperationalError

load_dotenv()

logger = logging.getLogger("app.database")

DATABASE_URL = os.getenv("DATABASE_URL")

try:
    engine = create_engine(DATABASE_URL)
    # Test the connection eagerly so misconfiguration surfaces at startup
    with engine.connect() as conn:
        pass
    logger.info("Database connection established")
except OperationalError as e:
    logger.error("Database connection failed: %s", e, exc_info=True)
    raise

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    except OperationalError as e:
        logger.error("Database session error: %s", e, exc_info=True)
        raise
    finally:
        db.close()
