# Blog API

A production-ready FastAPI blog application with PostgreSQL, JWT authentication, and full CRUD.

## Requirements

- Python 3.9+
- PostgreSQL running locally (or a cloud DB URL)

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/prajvalbhardwaj-spec/just-last.git
cd just-last
```

### 2. Configure environment

Create a `.env` file in the root folder:

```
DATABASE_URL=postgresql://user:password@localhost:5432/yourdb
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
```

### 3. Run locally (macOS/Linux)

```bash
./start.sh
```

### 3. Run locally (Windows)

```bat
start.bat
```

These scripts will:
1. Install all dependencies
2. Auto-create the database and seed dummy data
3. Start the development server at http://localhost:8000

## API Docs

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Endpoints

| Method | Route | Auth | Description |
|--------|-------|------|-------------|
| GET | `/` | No | Health check |
| POST | `/auth/login` | No | Login, returns JWT |
| POST | `/users/register` | No | Register new user |
| GET | `/users/` | No | List all users |
| GET | `/users/me` | Yes | Get current user |
| GET | `/users/{id}` | No | Get user by ID |
| PUT | `/users/{id}` | Yes | Update own account |
| DELETE | `/users/{id}` | Yes | Delete own account |
| POST | `/blogs/` | Yes | Create blog |
| GET | `/blogs/` | No | List all blogs |
| GET | `/blogs/{id}` | No | Get blog by ID |
| PUT | `/blogs/{id}` | Yes | Update own blog |
| DELETE | `/blogs/{id}` | Yes | Delete own blog |
| POST | `/seed` | No | Manually seed the database |

## Seed credentials (dummy data)

| Username | Email | Password |
|----------|-------|----------|
| alice | alice@example.com | password123 |
| bob | bob@example.com | password123 |
| charlie | charlie@example.com | password123 |

## Deploy to Render

1. Push this repository to GitHub.
2. Go to [Render](https://render.com) and create a **New Web Service**.
3. Connect your GitHub repo.
4. Create a **brand new PostgreSQL** database on Render (never reuse an old one).
5. Set Access Control to allow all traffic: `0.0.0.0/0`.
6. Copy the **External Database URL** and set it as `DATABASE_URL` in your service's environment variables.
7. Also set `SECRET_KEY` to a secure random string.
8. Render will automatically use `render.yaml` for build and start commands.

## Manual seed (if needed)

```bash
python seed.py
```

Or call the API endpoint:

```bash
curl -X POST http://localhost:8000/seed
```

## Docker

```bash
docker build -t blog-api .
docker run -p 10000:10000 --env-file .env blog-api
```
