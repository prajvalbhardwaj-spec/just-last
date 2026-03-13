import bcrypt
from sqlalchemy.orm import Session
from app.database import engine, SessionLocal
from app.models import Base, User, Blog


def create_tables():
    Base.metadata.create_all(bind=engine)
    print("Tables created")


def seed_database():
    db: Session = SessionLocal()
    try:
        if db.query(User).first():
            print("Database already has data, skipping seed")
            return

        users_data = [
            {"username": "alice", "email": "alice@example.com", "password": "password123"},
            {"username": "bob", "email": "bob@example.com", "password": "password123"},
            {"username": "charlie", "email": "charlie@example.com", "password": "password123"},
        ]

        users = []
        for ud in users_data:
            hashed = bcrypt.hashpw(
                ud["password"].encode("utf-8")[:72], bcrypt.gensalt()
            ).decode("utf-8")
            user = User(
                username=ud["username"],
                email=ud["email"],
                hashed_password=hashed,
            )
            db.add(user)
            users.append(user)

        db.flush()

        blogs_data = [
            {
                "title": "Welcome to My Blog",
                "content": "This is my first blog post. Hello world!",
                "owner": users[0],
            },
            {
                "title": "FastAPI is Amazing",
                "content": "FastAPI makes building APIs incredibly fast and easy to use.",
                "owner": users[0],
            },
            {
                "title": "Python Tips and Tricks",
                "content": "Here are some Python tips I have learned over the years.",
                "owner": users[1],
            },
            {
                "title": "Why I Love PostgreSQL",
                "content": "PostgreSQL is a powerful open-source relational database system.",
                "owner": users[1],
            },
            {
                "title": "Getting Started with Docker",
                "content": "Docker makes deploying applications straightforward and reproducible.",
                "owner": users[2],
            },
        ]

        for bd in blogs_data:
            blog = Blog(
                title=bd["title"],
                content=bd["content"],
                owner=bd["owner"],
            )
            db.add(blog)

        db.commit()
        print("Database seeded with dummy data")

    except Exception as e:
        db.rollback()
        print(f"Seeding failed: {e}")
        raise
    finally:
        db.close()
