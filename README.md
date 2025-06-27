# Rent Management System Backend

This is the **backend** for the Rent Management System, built with [FastAPI](https://fastapi.tiangolo.com/), [SQLAlchemy](https://www.sqlalchemy.org/), and [PostgreSQL](https://www.postgresql.org/).  
It provides RESTful APIs for authentication, user management, and property management.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Folder Structure](#folder-structure)
- [Getting Started](#getting-started)
- [Available Scripts](#available-scripts)
- [Development Notes](#development-notes)
- [Contributing](#contributing)
- [Contact](#contact)

---

## Project Overview

This backend is responsible for:

- User registration, login, and Google OAuth
- Role-based access control (tenant, owner, broker, admin)
- Property CRUD operations
- Secure JWT authentication
- PostgreSQL database integration

---

## Folder Structure

```
backend/
├── .env                  # Environment variables (DB, secrets, etc.)
├── README.md             # This documentation
├── app/                  # Main application code
│   ├── __init__.py
│   ├── crud.py           # CRUD logic for DB models
│   ├── database.py       # DB connection and session
│   ├── dependencies.py   # Auth, JWT, and other dependencies
│   ├── main.py           # FastAPI app entry point
│   ├── models.py         # SQLAlchemy models
│   ├── schemas.py        # Pydantic schemas
│   └── routers/          # API route modules
│       ├── __init__.py
│       ├── auth.py       # Auth endpoints (register, login, Google OAuth)
│       ├── properties.py # Property endpoints
│       └── users.py      # User management endpoints
├── tests/                # Unit and integration tests
│   ├── __init__.py
│   └── test_main.py
```

**Key files:**

- `.env`: Database URL, JWT secret, Google OAuth credentials
- `app/main.py`: FastAPI app and router registration
- `app/models.py`: SQLAlchemy models for User, Property, etc.
- `app/schemas.py`: Pydantic schemas for request/response validation
- `app/routers/`: API endpoints grouped by feature
- `tests/`: Place for all test code

---

## Getting Started

### Prerequisites

- [Python 3.12+](https://www.python.org/)
- [PostgreSQL](https://www.postgresql.org/) (running and accessible)
- [pip](https://pip.pypa.io/en/stable/)

### 1. Clone the repository

```bash
git clone https://github.com/dagiteferi/RENT-MANAGMENT-SYSTEM
cd Rent-managment-system/backend
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv Bata
source Bata/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```
> If `requirements.txt` is missing, install manually:
> ```bash
> pip install fastapi sqlalchemy psycopg2-binary python-dotenv passlib[bcrypt] python-jose[cryptography] authlib
> ```

### 4. Set up environment variables

Copy `.env` and fill in your database and secret values:

```
DATABASE_URL=postgresql://<user>:<password>@localhost:5432/<db>
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
JWT_SECRET_KEY=your-random-secret-key
```

### 5. Run database migrations

If using Alembic or similar, run migrations.  
If not, tables are auto-created on app start (see `Base.metadata.create_all` in `main.py`).

### 6. Start the development server

```bash
uvicorn app.main:app --reload
```

- The API will be available at [http://localhost:8000](http://localhost:8000)
- Interactive docs: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## Available Scripts

- `uvicorn app.main:app --reload` — Start the FastAPI server in development mode
- `pytest` — Run tests in the `tests/` directory

---

## Development Notes

- **Models**: All SQLAlchemy models are in `app/models.py`
- **Schemas**: All Pydantic schemas are in `app/schemas.py`
- **Routers**: Each feature (auth, properties, users) has its own router in `app/routers/`
- **Database**: Connection and session logic is in `app/database.py`
- **Authentication**: JWT-based, with Google OAuth support
- **Password Hashing**: Uses `passlib` with bcrypt

### Adding New Endpoints

- Create a new file in `app/routers/` or add to an existing one.
- Register the router in `app/main.py`.

### Running Tests

```bash
pytest
```

---

## Contributing

1. **Branch from `main`** for new features or bug fixes.
2. **Write clear, descriptive commit messages.**
3. **Test your changes** before pushing.
4. **Open a Pull Request** and request review from the team.

---

## Contact

For questions or help, contact the backend lead or post in the team chat.

---

**Happy coding!**
