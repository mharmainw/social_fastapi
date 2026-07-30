# Social FastAPI

[![API Tests](https://github.com/mharmainw/social_fastapi/actions/workflows/tests.yml/badge.svg)](https://github.com/mharmainw/social_fastapi/actions/workflows/tests.yml)

A production-ready social API built with FastAPI and PostgreSQL. It provides
user accounts, JWT authentication, post management, voting, database
migrations, automated tests, Docker images, and continuous deployment to
FastAPI Cloud.

## Features

- User registration and lookup
- OAuth2 password login with JWT bearer tokens
- Secure password hashing with Passlib and bcrypt
- Authenticated post creation, listing, retrieval, updating, and deletion
- Post ownership authorization
- Add and remove votes
- Vote counts included with post responses
- Search, pagination, and result limits for post listings
- PostgreSQL persistence with SQLAlchemy
- Alembic database migrations
- Custom dark Swagger UI
- Isolated pytest API suite
- Docker and Docker Compose support
- GitHub Actions CI/CD
- Automatic Docker Hub publishing
- Automatic FastAPI Cloud deployment

## Technology

| Component | Technology |
| --- | --- |
| Runtime | Python 3.11 |
| API | FastAPI |
| Validation | Pydantic 2 and pydantic-settings |
| ORM | SQLAlchemy 2 |
| Database | PostgreSQL |
| Migrations | Alembic |
| Authentication | OAuth2, JWT, python-jose |
| Password hashing | Passlib, bcrypt 4.0.1 |
| Package manager | uv |
| Tests | pytest, HTTPX, SQLite, PostgreSQL |
| Containers | Docker, Docker Compose |
| CI/CD | GitHub Actions |
| Deployment | FastAPI Cloud and Docker Hub |

## API endpoints

| Method | Path | Authentication | Description |
| --- | --- | --- | --- |
| `GET` | `/` | No | Service status and documentation link |
| `POST` | `/users/` | No | Create a user |
| `GET` | `/users/{id}` | No | Get a user |
| `POST` | `/login` | No | Authenticate and receive a JWT |
| `GET` | `/posts/` | Bearer token | List and search posts |
| `GET` | `/posts/{id}` | Bearer token | Get a post and vote count |
| `POST` | `/posts/` | Bearer token | Create a post |
| `PUT` | `/posts/{id}` | Bearer token | Update an owned post |
| `DELETE` | `/posts/{id}` | Bearer token | Delete an owned post |
| `POST` | `/vote/` | Bearer token | Add or remove a vote |
| `GET` | `/docs` | No | Custom Swagger UI |
| `GET` | `/openapi.json` | No | OpenAPI schema |

The `/login` endpoint uses OAuth2 form data. Enter the account email in the
`username` field and the account password in the `password` field.

Voting uses this request body:

```json
{
  "post_id": 1,
  "dir": 1
}
```

Use `dir: 1` to add a vote and `dir: 0` to remove it.

## Project structure

```text
app/
  main.py                 FastAPI application and middleware
  config.py               Environment-based settings
  database.py             SQLAlchemy engine and sessions
  models.py               Database models
  oauth2.py               JWT creation and validation
  schemas.py              Pydantic request and response models
  swagger.py              Custom Swagger UI
  utils.py                Password hashing helpers
  routers/
    auth.py               Login endpoint
    post.py               Post endpoints
    user.py               User endpoints
    vote.py               Voting endpoint
alembic/                  Database migrations
tests/test_api.py         Isolated API test suite
.github/workflows/        CI/CD workflow
Dockerfile                Production API image
docker-compose.yaml       Local Docker stack
docker-compose-prod.yaml  Production-style Docker stack
pyproject.toml            Project metadata and dependencies
uv.lock                   Locked dependency versions
```

## Requirements

- Python 3.11
- uv
- PostgreSQL, unless using Docker Compose
- Docker Desktop, optional

Install uv if it is not already available:

```bash
pip install uv
```

## Environment configuration

Create a `.env` file in the project root:

```dotenv
DATABASE_HOSTNAME=localhost
DATABASE_PORT=5432
DATABASE_PASSWORD=replace-with-your-password
DATABASE_NAME=posts
DATABASE_USERNAME=postgres
SECRET_KEY=replace-with-a-long-random-secret
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Do not commit `.env` or real credentials. The repository ignores `.env` files.

Generate a secure JWT secret with Python:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

## Local setup

Install the locked runtime and development dependencies:

```bash
uv sync --frozen --group dev
```

Apply database migrations:

```bash
uv run alembic upgrade head
```

Start the development server:

```bash
uv run fastapi dev
```

Open:

- API root: `http://127.0.0.1:8000/`
- Swagger UI: `http://127.0.0.1:8000/docs`
- OpenAPI schema: `http://127.0.0.1:8000/openapi.json`

## Tests

Run the complete test suite:

```bash
uv run pytest -q
```

Run only the API tests with detailed output:

```bash
uv run pytest tests/test_api.py -v
```

Local tests use an isolated in-memory SQLite database by default and never
modify the configured PostgreSQL database.

In GitHub Actions, tests use a temporary PostgreSQL 16 service. Each run creates
a unique schema, runs all tests, removes the schema, and destroys the database
container when the job finishes.

## Docker

Start the local API and PostgreSQL stack:

```bash
docker compose up -d --build
docker compose exec api alembic upgrade head
```

View API logs:

```bash
docker compose logs -f api
```

Stop the stack:

```bash
docker compose down
```

Run the production-style Compose configuration:

```bash
docker compose -f docker-compose-prod.yaml up -d --build
docker compose -f docker-compose-prod.yaml exec api alembic upgrade head
```

The PostgreSQL named volume preserves database data between container
recreations. Do not use `docker compose down -v` unless the database volume
should also be deleted.

## Docker Hub

The CI/CD pipeline publishes successful `main` builds to:

```text
mharmainw/social-fastapi:latest
```

Pull the current image:

```bash
docker pull mharmainw/social-fastapi:latest
```

## CI/CD

The GitHub Actions workflow runs on pushes and pull requests targeting `main`.

Pull request flow:

```text
Start PostgreSQL -> Install dependencies -> Run pytest
```

Push-to-main flow:

```text
Start PostgreSQL
  -> Run pytest
  -> Build and push the Docker image
  -> Deploy to FastAPI Cloud
```

Docker publishing requires these GitHub repository secrets:

```text
SOCIAL_FASTAPI_DOCKER_USERNAME
SOCIAL_FASTAPI_DOCKER_ACCESS_TOKEN
```

FastAPI Cloud deployment requires:

```text
FASTAPI_CLOUD_TOKEN
FASTAPI_CLOUD_APP_ID
```

Application secrets and the production PostgreSQL or Supabase configuration
belong in the FastAPI Cloud application settings. The disposable CI database
credentials are test-only and are never used by the deployed application.

## Database migrations

Create a migration after changing SQLAlchemy models:

```bash
uv run alembic revision --autogenerate -m "Describe the change"
```

Apply all migrations:

```bash
uv run alembic upgrade head
```

Show the current migration:

```bash
uv run alembic current
```

## Deployment behavior

Every successful push to `main` deploys the latest source to FastAPI Cloud.
Deployment is skipped when tests, the Docker build, or Docker Hub publishing
fails.

FastAPI Cloud builds the application from source. The Docker Hub image is a
separate deployment artifact and is not used automatically by FastAPI Cloud.
