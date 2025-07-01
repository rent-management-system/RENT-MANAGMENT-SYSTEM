# Backend API Documentation

## 1. Introduction

Welcome to the backend documentation for the Rent Management System. This document provides a comprehensive overview of the API, its architecture, and how to work with it.

The backend is built using **FastAPI**, a modern, high-performance Python web framework. It is responsible for handling all business logic, data storage, and user authentication.

**Technology Stack:**
- **Framework:** FastAPI
- **Database:** SQLAlchemy with SQLite (for simplicity, can be swapped for PostgreSQL, etc.)
- **Data Validation:** Pydantic
- **Authentication:** JWT (JSON Web Tokens) with Passlib for password hashing.

---

## 2. Project Setup

To get the backend running locally, follow these steps:

1.  **Navigate to the backend directory:**
    ```bash
    cd /home/dagi/Documents/Rent-managment-system/backend
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install dependencies:**
    All required Python packages are listed in `requirements.txt`.
    ```bash
    pip install -r ../requirements.txt
    ```

4.  **Run the development server:**
    The application is run using `uvicorn`, an ASGI server.
    ```bash
    uvicorn app.main:app --reload --port 8000
    ```
    - `--reload`: The server will automatically restart when you make code changes.
    - `--port 8000`: The server will be accessible at `http://localhost:8000`.

5.  **Access API Docs:**
    FastAPI automatically generates interactive API documentation. Once the server is running, you can access it at:
    - **Swagger UI:** `http://localhost:8000/docs`
    - **ReDoc:** `http://localhost:8000/redoc`

---

## 3. Folder Structure

The backend code is organized to separate concerns, making it modular and maintainable.

```
backend/
├── app/
│   ├── __init__.py
│   ├── crud.py
│   ├── database.py
│   ├── dependencies.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   └── routers/
│       ├── __init__.py
│       ├── auth.py
│       └── users.py
└── tests/
    ├── __init__.py
    └── test_main.py
```

#### File-by-File Explanation:

- **`app/main.py`**: This is the heart of the application. It creates the main `FastAPI` instance, includes the API routers, and sets up middleware like CORS.

- **`app/database.py`**: This file handles all database connections. It creates the SQLAlchemy engine and the `SessionLocal` class, which is used to create new database sessions for each request.

- **`app/models.py`**: Defines the structure of your database tables using SQLAlchemy's ORM (Object-Relational Mapping). Each class in this file represents a table in the database (e.g., the `User` class maps to the `users` table).

- **`app/schemas.py`**: Contains Pydantic models, which we call "schemas". These define the shape of the data for API requests and responses. They are used for data validation, conversion, and documentation. For example, `UserCreate` defines the fields required to create a new user, while `User` defines the fields that are returned by the API.

- **`app/dependencies.py`**: Holds common dependencies used across different endpoints. The most important one is `get_current_user`, which validates the JWT token from the request header and returns the corresponding user from the database. This is how we protect endpoints and know who the current user is.

- **`app/crud.py`**: "CRUD" stands for Create, Read, Update, Delete. This file will contain the functions that directly interact with the database to perform these operations (e.g., a function `create_user` that takes user data and adds a new user to the database).

- **`app/routers/`**: This directory holds the different API route modules.
    - **`auth.py`**: Contains all endpoints related to authentication, such as `/register`, `/login`, and Google OAuth routes.
    - **`users.py`**: Contains endpoints for user-related actions, like `/users/me` which fetches the profile of the currently logged-in user.

- **`tests/`**: Contains all automated tests for the application to ensure reliability.

---

## 4. Authentication Flow (JWT)

1.  **Login:** The user sends their `email` and `password` to the `POST /auth/login` endpoint.
2.  **Verification:** The server checks if a user with that email exists and if the provided password is correct.
3.  **Token Creation:** If the credentials are valid, the server generates a unique **JWT access token**. This token contains the user's email (`sub`, for "subject") and an expiration time.
4.  **Token Storage:** The server sends this token back to the frontend. The frontend is responsible for storing it (e.g., in `localStorage`).
5.  **Authenticated Requests:** For any subsequent request to a protected endpoint (like `/users/me`), the frontend must include the token in the `Authorization` header like this: `Authorization: Bearer <the_token>`.
6.  **Token Validation:** The `get_current_user` dependency on the backend automatically reads this header, decodes the token, verifies its signature and expiration, and fetches the user from the database. If the token is invalid or expired, it returns a `401 Unauthorized` error.

---

## 5. API Endpoints (Detailed)

### Authentication (`/auth`)

#### `POST /auth/register`
- **Description:** Creates a new user account.
- **Request Body (`UserCreate` schema):**
  ```json
  {
    "email": "user@example.com",
    "full_name": "Test User",
    "password": "a_strong_password",
    "role": "tenant",
    "phone_number": "1234567890"
  }
  ```
- **Success Response (200 OK):** Returns the newly created user's data (`User` schema).
- **Error Responses:**
  - `400 Bad Request`: If the email is already registered.
  - `422 Unprocessable Entity`: If the request body is malformed.

#### `POST /auth/login`
- **Description:** Authenticates a user and returns a JWT access token.
- **Request Body (`LoginCredentials` schema):**
  ```json
  {
    "email": "user@example.com",
    "password": "a_strong_password"
  }
  ```
- **Success Response (200 OK):** Returns an access token (`Token` schema).
  ```json
  {
    "access_token": "ey...",
    "token_type": "bearer"
  }
  ```
- **Error Responses:**
  - `400 Bad Request`: If the email or password is incorrect.
  - `422 Unprocessable Entity`: If the request body is malformed.

### Users (`/users`)

#### `GET /users/me`
- **Description:** Retrieves the profile of the currently authenticated user.
- **Authentication:** Requires a valid JWT token in the `Authorization` header.
- **Request Body:** None.
- **Success Response (200 OK):** Returns the user's data (`User` schema).
- **Error Responses:**
  - `401 Unauthorized`: If the token is missing, invalid, or expired.