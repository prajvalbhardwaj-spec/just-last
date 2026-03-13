import os
from dotenv import load_dotenv
from sqlalchemy_utils import database_exists, create_database

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set in .env")

# Auto-create the database if it doesn't exist
if not database_exists(DATABASE_URL):
    create_database(DATABASE_URL)
    print(f"Database created: {DATABASE_URL}")
else:
    print("Database already exists")

# Now create tables and seed
from app.seeder import create_tables, seed_database

create_tables()
seed_database()

print("Database seeded successfully!")
