# social_fastapi

Lightweight FastAPI backend for users and posts with SQLAlchemy + PostgreSQL and a custom dark Swagger UI.

## Features

- User routes:
  - `POST /users/` create a user
  - `GET /users/{id}` get user by id
- Post routes:
  - `GET /posts/` list all posts
  - `GET /posts/{id}` get post by id
  - `POST /posts/` create a post
  - `PUT /posts/{id}` update a post
  - `DELETE /posts/{id}` delete a post
- Custom themed Swagger UI available at `GET /docs`

## Project structure

- `app/main.py`: app initialization and router mounting
- `app/routers/user.py`: user endpoints
- `app/routers/post.py`: post endpoints
- `app/models.py`: SQLAlchemy models
- `app/schemas.py`: request/response schemas
- `app/database.py`: SQLAlchemy DB engine/session setup
- `app/swagger.py`: Swagger UI styling customization
- `app/utils.py`: helper methods (password hashing etc.)

## Setup

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

pip install fastapi uvicorn sqlalchemy psycopg2-binary python-dotenv passlib[bcrypt]
```

## Database configuration

`app/database.py` uses:

```python
SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:abc123**@localhost/posts'
```

Update this connection string to match your local PostgreSQL credentials and database.

Create a matching PostgreSQL database and table models through migration/DDL as your setup requires.

## Run

```bash
uv run fastapi dev
# or
uvicorn app.main:app --reload
```

Swagger docs:

- `http://127.0.0.1:8000/docs`
- `http://127.0.0.1:8000/redoc`

## Notes

- If you use PostgreSQL schema names/columns that differ from models, endpoint filters may fail with SQL-level errors.
- Keep `.venv/`, `__pycache__/`, and DB credentials out of version control.
