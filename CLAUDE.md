# CLAUDE.md — Project Rules & Architecture Guidelines

These rules MUST be followed in every session, for every change, without exception.

---

## 1. Project Structure

Always create a modular structure:
- `app/` folder for all source code
- `.env` file for secrets (never commit this)
- `requirements.txt` for dependencies

---

## 2. Compatibility

- Target Python 3.9+
- CRITICAL: Do NOT use the `|` operator for unions (e.g., `str | None`).
- Use `from typing import Optional` (e.g., `Optional[str]`) for backward compatibility.

---

## 3. Database

- Use SQLAlchemy (2.0 style) and Pydantic (v2)
- Use Alembic for database migrations
- CRITICAL: The app must AUTO-CREATE the database itself if it does not exist. Do NOT assume the database already exists.
- In `seed.py`:
  1. Connect to the PostgreSQL server (not a specific database) and check if the target database exists.
  2. If it does NOT exist, CREATE it automatically.
  3. Then connect to the target database.
  4. Auto-create all tables.
  5. Auto-seed dummy data if tables are empty.
- Use `sqlalchemy_utils` (`database_exists`, `create_database`) or raw SQL via `psycopg2` to create the database.
- Add `sqlalchemy-utils` to `requirements.txt`.
- The app must work out-of-the-box with ZERO manual setup — no need to manually create a database.

---

## 4. Seeding & Startup (CRITICAL — No Lifespan Seeding)

- Do NOT run seed logic inside FastAPI's lifespan.
- Do NOT run seed logic on app startup at all.
- REASON: With multiple Uvicorn workers (`--workers 4`), each worker runs lifespan separately, causing duplicate inserts and integrity errors.
- Instead, `seed.py` is a STANDALONE script that runs ONCE BEFORE the server starts:
  a) `seed.py` creates the database if it doesn't exist
  b) `seed.py` creates all tables
  c) `seed.py` inserts dummy data if tables are empty
  d) THEN the server starts with workers
- The FastAPI app's lifespan should ONLY contain non-data logic (e.g., logging "App started").
- This is enforced in `start.sh`, `start.bat`, `render.yaml`, and `Dockerfile` — `seed.py` always runs first.

---

## 5. Dependencies (requirements.txt)

- NEVER pin version numbers in `requirements.txt`
- Write ONLY the package name, one per line
- Example: `fastapi` NOT `fastapi==0.100.0`
- No `==` or `>=` or `~=` version specifiers at all

---

## 6. Deployment-Ready

- Include a `Dockerfile` for containerized deployment
- Include a `render.yaml` for Render deployment
- Use environment variables for all secrets
- **Render PostgreSQL (CRITICAL — Always Create NEW):**
  * When deploying to Render, ALWAYS create a brand new PostgreSQL database. NEVER reuse or connect to an existing database.
  * Even if a database already exists on the user's Render account, create a fresh one for this project.
  * Set Access Control to allow ALL inbound traffic (0.0.0.0/0) so it is accessible from anywhere.
  * Use the new database's External Database URL as the `DATABASE_URL` environment variable.
  * This ensures a clean slate — no leftover tables, no schema conflicts, no stale data from old projects.
- `render.yaml` build command must run `seed.py` FIRST:
  ```
  buildCommand: pip install -r requirements.txt && python seed.py
  startCommand: uvicorn app.main:app --host 0.0.0.0 --port $PORT --workers 4
  ```
- `Dockerfile` must also run `seed.py` before starting:
  ```
  CMD python seed.py && uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
  ```

---

## 7. GitHub Integration (CRITICAL)

- At the VERY START of any new project, before generating any code, ask ONLY for the GitHub repository URL.
- Do NOT ask anything else. No other questions.
- Initialize git and set the remote origin to that GitHub URL immediately.

---

## 8. Git Commits (MANDATORY)

- After EVERY change, new feature, or fix: automatically `git add`, commit with a descriptive message, and push to GitHub. Never skip this step.
- Commit messages should be clear, e.g.:
  - `feat: add database connection setup`
  - `fix: resolve seed script error`

---

## 9. Password Hashing (CRITICAL — Avoid bcrypt bugs)

- Do NOT use `passlib` for password hashing. `passlib` has compatibility issues with newer versions of `bcrypt` (`AttributeError` on `__about__`).
- Instead, use `bcrypt` directly:
  ```python
  import bcrypt
  hashed = bcrypt.hashpw(
      password.encode('utf-8')[:72],
      bcrypt.gensalt()
  )
  ```
- ALWAYS truncate passwords to 72 bytes BEFORE hashing: `password.encode('utf-8')[:72]`
- Add `bcrypt` to `requirements.txt` (NOT `passlib`)

---

## 10. Startup Scripts (CRITICAL)

- Create a `start.sh` script (macOS/Linux) that:
  a) Installs dependencies (`pip install -r requirements.txt`)
  b) Runs `python seed.py` (creates DB + tables + data)
  c) Starts the server (`uvicorn app.main:app --reload`)
- Create a `start.bat` script (Windows) that:
  a) Installs dependencies (`pip install -r requirements.txt`)
  b) Runs `python seed.py` (creates DB + tables + data)
  c) Starts the server (`uvicorn app.main:app --reload`)
- `seed.py` runs FIRST, THEN the server starts. This is the ONLY correct order.
- Make `start.sh` executable (`chmod +x start.sh`)
- Users should ONLY need to run `./start.sh` or `start.bat` to get the full app running.
