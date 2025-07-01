# Backend API Documentation: A Comprehensive Guide

## Table of Contents

1.  [Introduction](#1-introduction)
2.  [Project Setup and Running the Backend](#2-project-setup-and-running-the-backend)
3.  [Detailed Backend Folder Structure and File Explanations](#3-detailed-backend-folder-structure-and-file-explanations)
    *   [File-by-File Explanation:](#file-by-file-explanation)
        *   [`.env`](#env)
        *   [`app/main.py`](#appmainpy)
        *   [`app/database.py`](#appdatabasepy)
        *   [`app/models.py`](#appmodelspy)
        *   [`app/schemas.py`](#appschemaspy)
        *   [`app/dependencies.py`](#appdependenciespy)
        *   [`app/crud.py`](#appcrudpy)
        *   [`app/routers/auth.py`](#approutersauthpy)
        *   [`app/routers/users.py`](#approutersuserspy)
        *   [`app/routers/properties.py`](#approuterspropertiespy)
        *   [`tests/test_main.py`](#teststest_mainpy)
4.  [Backend-Frontend Integration: How They Talk](#4-backend-frontend-integration-how-they-talk)
5.  [Future Enhancements (Planned/Potential)](#5-future-enhancements-plannedpotential)
6.  [Conclusion](#6-conclusion)

---

## 1. Introduction

Welcome to the backend documentation for the Rent Management System. This document provides a comprehensive overview of the API, its architecture, and how to work with it. It is designed to be easily understood by developers of all levels, from beginners to experienced programmers.

The backend is built using **FastAPI**, a modern, high-performance Python web framework. It is responsible for handling all business logic, data storage, and user authentication. It acts as the brain of the application, processing requests from the frontend, interacting with the database, and sending back responses.

**Key Technologies Used:**

*   **FastAPI:** A Python web framework for building APIs quickly and efficiently. It's known for its speed and automatic interactive API documentation.
*   **SQLAlchemy:** A powerful and flexible SQL toolkit and Object-Relational Mapper (ORM) for Python. It allows us to interact with databases using Python objects instead of raw SQL queries.
*   **Pydantic:** A data validation and settings management library using Python type hints. It ensures that the data received by our API is in the correct format and automatically generates API documentation.
*   **JWT (JSON Web Tokens):** A compact, URL-safe means of representing claims between two parties. We use it for securely authenticating users.
*   **Passlib:** A comprehensive password hashing library for Python, used to securely store and verify user passwords.
*   **Uvicorn:** An ASGI (Asynchronous Server Gateway Interface) server that runs our FastAPI application.

---

## 2. Project Setup and Running the Backend

To get the backend API up and running on your local machine, follow these steps:

1.  **Open your terminal or command prompt.**

2.  **Navigate to the backend directory:**
    ```bash
    cd /home/dagi/Documents/Rent-managment-system/backend
    ```

3.  **Create a Python Virtual Environment (Recommended):**
    A virtual environment isolates your project's dependencies from other Python projects on your system, preventing conflicts.
    ```bash
    python -m venv venv
    ```

4.  **Activate the Virtual Environment:**
    *   **On macOS/Linux:**
        ```bash
        source venv/bin/activate
        ```
    *   **On Windows:**
        ```bash
        .\venv\Scripts\activate
        ```

5.  **Install Dependencies:**
    All required Python packages are listed in the `requirements.txt` file located in the project root. This command will install them into your active virtual environment.
    ```bash
    pip install -r ../requirements.txt
    ```

6.  **Run the Development Server:**
    This command starts the FastAPI application using Uvicorn. The `--reload` flag is very useful during development as it automatically restarts the server whenever you make changes to your code.
    ```bash
    uvicorn app.main:app --reload --port 8000
    ```
    -   `app.main:app`: Tells Uvicorn to find the `app` object (our FastAPI application instance) within the `main.py` file inside the `app` directory.
    -   `--reload`: Enables auto-reloading of the server on code changes.
    -   `--port 8000`: Specifies that the server should run on port 8000. You can access it in your browser or from the frontend at `http://localhost:8000`.

7.  **Access Interactive API Documentation:**
    FastAPI automatically generates interactive API documentation based on your code. Once the server is running, you can explore all available endpoints and test them directly from your browser:
    -   **Swagger UI:** Open `http://localhost:8000/docs` in your web browser.
    -   **ReDoc:** Open `http://localhost:8000/redoc` in your web browser.

---

## 3. Detailed Backend Folder Structure and File Explanations

The backend codebase is structured logically to separate different concerns, making it easier to understand, maintain, and scale. Here's a detailed breakdown:

```
backend/
├── .env                       # Environment variables (e.g., for secrets, database connection strings).
├── README.md                  # General information about the backend project.
├── app/                       # Contains the core FastAPI application logic.
│   ├── __init__.py            # Marks the 'app' directory as a Python package.
│   ├── crud.py                # Create, Read, Update, Delete operations for database models.
│   ├── database.py            # Database connection setup and session management.
│   ├── dependencies.py        # Reusable functions for dependency injection (e.g., authentication).
│   ├── main.py                # Main FastAPI application instance and router inclusion.
│   ├── models.py              # SQLAlchemy ORM models (defines database table structures).
│   ├── schemas.py             # Pydantic schemas (defines data shapes for requests/responses).
│   └── routers/               # API endpoint definitions, grouped by functionality.
│       ├── __init__.py        # Marks the 'routers' directory as a Python package.
│       ├── auth.py            # Authentication-related API endpoints.
│       ├── properties.py      # Property management API endpoints (currently a placeholder).
│       └── users.py           # User-related API endpoints.
└── tests/                     # Contains automated tests for the backend.
    ├── __init__.py            # Marks the 'tests' directory as a Python package.
    └── test_main.py           # Example tests for the main application logic.
```

#### File-by-File Explanation:

*   **`.env`**:
    *   **Purpose**: This file is used to store environment-specific variables, such as database connection strings, API keys, or any other sensitive information that should not be hardcoded directly into the source code or committed to version control. It's loaded by the `python-dotenv` library.
    *   **Example Content**: `DATABASE_URL="sqlite:///./sql_app.db"`, `SECRET_KEY="your-super-secret-key"`

*   **`app/main.py`**:
    *   **Purpose**: This is the main entry point for your FastAPI application. It initializes the FastAPI app, sets up global middleware (like CORS), and includes all the API routers.
    *   **Key Code Snippets & Explanation**:
        ```python
        from fastapi import FastAPI
        from fastapi.middleware.cors import CORSMiddleware
        from app.routers import auth, users # Import your API routers
        from app.database import Base, engine

        app = FastAPI() # Initialize the FastAPI application

        # CORS Middleware: Essential for frontend-backend communication
        # This allows your frontend (running on a different port/domain) to make requests to this backend.
        # allow_origins=["*"] means any origin can access your API (for development).
        # In production, you should replace "*" with your frontend's specific domain (e.g., "https://your-frontend.com").
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        # Database Table Creation: Ensures all tables defined in models.py are created in the database
        Base.metadata.create_all(bind=engine)

        # Include Routers: Connects the API endpoints defined in auth.py and users.py to the main app.
        app.include_router(auth.router)
        app.include_router(users.router)
        # Future: app.include_router(properties.router)
        ```

*   **`app/database.py`**:
    *   **Purpose**: This file is responsible for setting up the database connection using SQLAlchemy. It defines the database engine and a session maker, which are crucial for interacting with your database.
    *   **Key Code Snippets & Explanation**:
        ```python
        from sqlalchemy import create_engine
        from sqlalchemy.ext.declarative import declarative_base
        from sqlalchemy.orm import sessionmaker

        # SQLALCHEMY_DATABASE_URL: Reads the database URL from the environment variables.
        # This makes it easy to switch databases (e.g., SQLite, PostgreSQL) without changing code.
        SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db" # Default to SQLite for simplicity

        # create_engine: Establishes the connection to the database.
        # connect_args={"check_same_thread": False} is needed for SQLite only, 
        # as SQLite works with a single thread and FastAPI uses multiple threads.
        engine = create_engine(
            SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
        )

        # SessionLocal: A session factory. Each database interaction will use an instance of this session.
        # The `autocommit=False` and `autoflush=False` ensure that changes are not saved automatically.
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

        # Base: The base class for our SQLAlchemy models. Our database models will inherit from this.
        Base = declarative_base()

        # Dependency to get a database session for each request.
        # This ensures that each request gets its own independent database session,
        # which is then closed after the request is finished.
        def get_db():
            db = SessionLocal()
            try:
                yield db
            finally:
                db.close()
        ```

*   **`app/models.py`**:
    *   **Purpose**: This file defines the structure of your database tables using SQLAlchemy's ORM (Object-Relational Mapping). Each class here corresponds to a table in your database, and its attributes define the columns of that table.
    *   **Key Code Snippets & Explanation**:
        ```python
        from sqlalchemy import Boolean, Column, Integer, String, DateTime, Enum
        from sqlalchemy.sql import func
        from .database import Base
        import enum

        # UserRole: An Enum to define allowed roles for users (e.g., tenant, landlord, admin).
        class UserRole(str, enum.Enum):
            tenant = "tenant"
            landlord = "landlord"
            admin = "admin"

        # User: Defines the 'users' table in the database.
        # Inherits from Base (from database.py) to be recognized by SQLAlchemy.
        class User(Base):
            __tablename__ = "users"

            id = Column(Integer, primary_key=True, index=True) # Unique ID, auto-incrementing
            email = Column(String, unique=True, index=True) # User's email, must be unique
            full_name = Column(String)
            password = Column(String, nullable=True) # Hashed password (can be null for Google users)
            role = Column(Enum(UserRole), default=UserRole.tenant) # User's role
            phone_number = Column(String, nullable=True)
            profile_picture = Column(String, nullable=True)
            is_active = Column(Boolean, default=True) # Whether the user account is active
            created_at = Column(DateTime(timezone=True), server_default=func.now()) # Timestamp of creation
            google_id = Column(String, unique=True, nullable=True) # Google ID for OAuth users

        # Future: Property model (example)
        # class Property(Base):
        #     __tablename__ = "properties"
        #     id = Column(Integer, primary_key=True, index=True)
        #     address = Column(String)
        #     rent = Column(Float)
        #     landlord_id = Column(Integer, ForeignKey("users.id"))
        #     landlord = relationship("User", back_populates="properties")
        ```

*   **`app/schemas.py`**:
    *   **Purpose**: This file defines Pydantic models (schemas) that are used for data validation and serialization. They ensure that data coming into the API (requests) and going out of the API (responses) conforms to a defined structure. FastAPI uses these schemas to automatically generate API documentation.
    *   **Key Code Snippets & Explanation**:
        ```python
        from pydantic import BaseModel, EmailStr
        from typing import Optional
        from datetime import datetime
        from app.models import UserRole # Import the UserRole Enum from models

        # UserBase: Common fields for user data.
        class UserBase(BaseModel):
            email: EmailStr # EmailStr ensures it's a valid email format
            full_name: str
            role: UserRole
            phone_number: Optional[str] = None # Optional fields can be None
            profile_picture: Optional[str] = None

        # UserCreate: Schema for creating a new user (includes password).
        class UserCreate(UserBase):
            password: str

        # User: Schema for returning user data (excludes password, includes ID, etc.).
        # Config.from_attributes = True is for SQLAlchemy compatibility.
        class User(Base):
            id: int
            is_active: bool
            created_at: datetime
            google_id: Optional[str] = None
            class Config:
                from_attributes = True

        # Token: Schema for the JWT token returned upon successful login.
        class Token(BaseModel):
            access_token: str
            token_type: str

        # TokenData: Schema for data contained within the JWT token.
        class TokenData(BaseModel):
            email: Optional[str] = None

        # LoginCredentials: Schema for login requests (email and password).
        # This is what the frontend sends to the /auth/login endpoint.
        class LoginCredentials(BaseModel):
            email: EmailStr
            password: str

        # Future: Property schemas (example)
        # class PropertyBase(BaseModel):
        #     address: str
        #     rent: float

        # class PropertyCreate(PropertyBase):
        #     pass

        # class Property(PropertyBase):
        #     id: int
        #     landlord_id: int
        #     class Config:
        #         from_attributes = True
        ```

*   **`app/dependencies.py`**:
    *   **Purpose**: This file contains reusable functions that can be injected into API endpoints using FastAPI's Dependency Injection system. This is particularly useful for tasks like database session management and authentication.
    *   **Key Code Snippets & Explanation**:
        ```python
        from datetime import datetime, timedelta
        from typing import Optional
        from fastapi import Depends, HTTPException, status
        from fastapi.security import OAuth2PasswordBearer
        from jose import JWTError, jwt
        from sqlalchemy.orm import Session
        from .database import get_db
        from .models import User
        from .schemas import TokenData
        from passlib.context import CryptContext
        import os

        # Load environment variables (e.g., SECRET_KEY, ALGORITHM)
        from dotenv import load_dotenv
        load_dotenv()

        # Password Hashing Context: Used for hashing and verifying passwords.
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

        # OAuth2PasswordBearer: Handles JWT token extraction from Authorization header.
        oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

        # SECRET_KEY: Used to sign JWT tokens. Keep this secret and secure!
        SECRET_KEY = os.getenv("SECRET_KEY")
        ALGORITHM = "HS256"
        ACCESS_TOKEN_EXPIRE_MINUTES = 30 # Token expiration time

        # create_access_token: Generates a new JWT token.
        def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
            to_encode = data.copy()
            if expires_delta:
                expire = datetime.utcnow() + expires_delta
            else:
                expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            to_encode.update({"exp": expire}) # Add expiration time to token payload
            encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
            return encoded_jwt

        # get_current_user: Dependency to get the currently authenticated user.
        # This function is used in protected API endpoints.
        async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
            credentials_exception = HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
            try:
                # Decode and verify the JWT token
                payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
                email: str = payload.get("sub") # Extract user's email from token
                if email is None:
                    raise credentials_exception
                token_data = TokenData(email=email)
            except JWTError:
                raise credentials_exception
            
            # Fetch the user from the database using the email from the token
            user = db.query(User).filter(User.email == token_data.email).first()
            if user is None:
                raise credentials_exception
            return user
        ```

*   **`app/crud.py`**:
    *   **Purpose**: This file is intended to contain functions for Create, Read, Update, and Delete (CRUD) operations on your database models. By centralizing these operations here, you keep your API endpoints clean and focused on request/response handling, while the database logic is encapsulated.
    *   **Example (User CRUD)**:
        ```python
        from sqlalchemy.orm import Session
        from . import models, schemas

        def get_user(db: Session, user_id: int):
            return db.query(models.User).filter(models.User.id == user_id).first()

        def get_user_by_email(db: Session, email: str):
            return db.query(models.User).filter(models.User.email == email).first()

        def create_user(db: Session, user: schemas.UserCreate):
            # Note: Password hashing should happen before calling this CRUD function
            db_user = models.User(**user.model_dump())
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
            return db_user

        # Add more CRUD functions for properties, etc., as needed.
        ```

*   **`app/routers/auth.py`**:
    *   **Purpose**: This file defines all the API endpoints related to user authentication, including registration, login, and Google OAuth.
    *   **Key Code Snippets & Explanation**:
        ```python
        from fastapi import APIRouter, Depends, HTTPException, status
        from sqlalchemy.orm import Session
        from authlib.integrations.starlette_client import OAuth # For Google OAuth
        from starlette.requests import Request
        from starlette.config import Config
        from app.database import get_db
        from app.models import User
        from app.schemas import UserCreate, User as UserSchema, Token, LoginCredentials # Import schemas
        from app.dependencies import create_access_token, pwd_context, get_current_user
        import os
        from dotenv import load_dotenv

        load_dotenv() # Load environment variables

        router = APIRouter(prefix="/auth", tags=["auth"]) # Define API router with prefix /auth

        # Google OAuth setup (using Authlib)
        config = Config(environ=os.environ)
        oauth = OAuth(config)
        oauth.register(
            name="google",
            client_id=os.getenv("GOOGLE_CLIENT_ID"),
            client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
            server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
            client_kwargs={"scope": "openid email profile"}
        )

        @router.post("/register", response_model=UserSchema)
        def register(user: UserCreate, db: Session = Depends(get_db)):
            # Check if email already exists
            db_user = db.query(User).filter(User.email == user.email).first()
            if db_user:
                raise HTTPException(status_code=400, detail="Email already registered")
            
            # Hash the password before storing it
            hashed_password = pwd_context.hash(user.password)
            
            # Create new user in the database
            db_user = User(
                email=user.email,
                full_name=user.full_name,
                password=hashed_password,
                role=user.role,
                phone_number=user.phone_number,
                profile_picture=user.profile_picture
            )
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
            return db_user # Return the created user data

        @router.post("/login", response_model=Token)
        def login(credentials: LoginCredentials, db: Session = Depends(get_db)):
            # Find user by email and verify password
            user = db.query(User).filter(User.email == credentials.email).first()
            if not user or (user.password and not pwd_context.verify(credentials.password, user.password)):
                raise HTTPException(status_code=400, detail="Incorrect email or password")
            
            # Check if user is active
            if not user.is_active:
                raise HTTPException(status_code=400, detail="Inactive user")
            
            # Create and return JWT access token
            access_token = create_access_token(data={"sub": user.email})
            return {"access_token": access_token, "token_type": "bearer"}

        @router.get("/google")
        async def google_login(request: Request):
            # Redirects user to Google's authentication page
            redirect_uri = "http://localhost:8000/auth/google/callback"
            return await oauth.google.authorize_redirect(request, redirect_uri)

        @router.get("/google/callback", response_model=Token)
        async def google_callback(request: Request, db: Session = Depends(get_db)):
            # Handles the callback from Google after successful authentication
            token = await oauth.google.authorize_access_token(request)
            user_info = token.get("userinfo")
            if not user_info:
                raise HTTPException(status_code=400, detail="Failed to fetch user info")
            
            # Check if user already exists via Google ID
            db_user = db.query(User).filter(User.google_id == user_info["sub"]).first()
            if not db_user:
                # If not, create a new user with Google details
                db_user = User(
                    email=user_info["email"],
                    full_name=user_info.get("name", "Unknown"),
                    google_id=user_info["sub"],
                    role="tenant"
                )
                db.add(db_user)
                db.commit()
                db.refresh(db_user)
            
            if not db_user.is_active:
                raise HTTPException(status_code=400, detail="Inactive user")
            
            # Create and return JWT for the Google-authenticated user
            access_token = create_access_token(data={"sub": db_user.email})
            return {"access_token": access_token, "token_type": "bearer"}
        ```

*   **`app/routers/users.py`**:
    *   **Purpose**: This file defines API endpoints related to user management, specifically for retrieving user information.
    *   **Key Code Snippets & Explanation**:
        ```python
        from fastapi import APIRouter, Depends
        from sqlalchemy.orm import Session
        from app.database import get_db
        from app.models import User
        from app.schemas import User as UserSchema
        from app.dependencies import get_current_user # Import the authentication dependency

        router = APIRouter(prefix="/users", tags=["users"]) # Define API router with prefix /users

        @router.get("/me", response_model=UserSchema)
        # This endpoint requires authentication. get_current_user will validate the JWT token.
        def read_users_me(current_user: User = Depends(get_current_user)):
            # If get_current_user succeeds, current_user will contain the User object from the database.
            return current_user # Returns the current user's data (excluding sensitive info like password)
        ```

*   **`app/routers/properties.py`**:
    *   **Purpose**: This file is currently a placeholder but is intended to contain API endpoints for managing rental properties (e.g., creating, listing, updating, deleting properties).
    *   **Example Future Content**:
        ```python
        # from fastapi import APIRouter, Depends, HTTPException, status
        # from sqlalchemy.orm import Session
        # from app.database import get_db
        # from app.models import Property, User
        # from app.schemas import PropertyCreate, Property as PropertySchema
        # from app.dependencies import get_current_user

        # router = APIRouter(prefix="/properties", tags=["properties"])

        # @router.post("/", response_model=PropertySchema)
        # def create_property(property: PropertyCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
        #     # Example: Only landlords can create properties
        #     if current_user.role != "landlord":
        #         raise HTTPException(status_code=403, detail="Only landlords can add properties")
        #     db_property = Property(**property.model_dump(), landlord_id=current_user.id)
        #     db.add(db_property)
        #     db.commit()
        #     db.refresh(db_property)
        #     return db_property
        ```

*   **`tests/test_main.py`**:
    *   **Purpose**: Contains automated tests for your backend API. Writing tests is crucial for ensuring that your code works as expected and doesn't break when you make changes. These tests typically simulate requests to your API and check the responses.
    *   **Example Test Structure**:
        ```python
        # from fastapi.testclient import TestClient
        # from app.main import app

        # client = TestClient(app)

        # def test_read_main():
        #     response = client.get("/")
        #     assert response.status_code == 200
        #     assert response.json() == {"message": "Hello World"}

        # def test_register_user():
        #     response = client.post(
        #         "/auth/register",
        #         json={
        #             "email": "test@example.com",
        #             "full_name": "Test User",
        #             "password": "testpassword",
        #             "role": "tenant"
        #         },
        #     )
        #     assert response.status_code == 200
        #     assert response.json()["email"] == "test@example.com"
        ```

---

## 4. Backend-Frontend Integration: How They Talk

The frontend and backend are separate applications that communicate with each other over HTTP requests. Think of it like ordering food at a restaurant:

*   **Frontend (You, the Customer):** You make a request (order food).
*   **Backend (The Kitchen/Chef):** The kitchen receives your order, prepares it, and sends it back to you.

Here's how this communication happens in our system:

1.  **HTTP Requests:** The frontend uses the `axios` library to send HTTP requests (like `GET`, `POST`, `PUT`, `DELETE`) to specific URLs (endpoints) exposed by the backend.

2.  **JSON Data Format:** For most data exchange, both the frontend and backend use **JSON (JavaScript Object Notation)**. It's a lightweight, human-readable format for sending data.

3.  **CORS (Cross-Origin Resource Sharing):** Because your frontend and backend run on different "origins" (e.g., `localhost:5173` for frontend and `localhost:8000` for backend), web browsers enforce a security measure called CORS. The backend's `main.py` includes `CORSMiddleware` to explicitly tell the browser that it's safe for the frontend to make requests to it.

4.  **Authentication (JWT Tokens):**
    *   **Login:** When you log in from the frontend, your credentials are sent to the backend's `/auth/login` endpoint.
    *   **Token Generation:** If successful, the backend generates a **JWT (JSON Web Token)**. This token is like a temporary ID card. It's signed by the backend's secret key, so the backend can always verify its authenticity.
    *   **Token Storage (Frontend):** The frontend receives this token and stores it securely (e.g., in `localStorage`).
    *   **Authenticated Requests:** For any subsequent request to a protected endpoint (like fetching user details or properties), the frontend includes this JWT in the `Authorization` header of the HTTP request (e.g., `Authorization: Bearer <your_jwt_token>`).
    *   **Token Validation (Backend):** The backend's `get_current_user` dependency (in `app/dependencies.py`) intercepts these requests, extracts the token, verifies its signature and expiration, and identifies the user. If the token is invalid or missing, the request is rejected with a `401 Unauthorized` error.

5.  **Data Flow Example (Login Process):**
    *   **Frontend Action:** User enters email/password on `LoginPage` and clicks login.
    *   **Frontend (`authService.ts`):** Calls `authApi.post('/auth/login', params)`.
    *   **Backend (`auth.py`):** `login` endpoint receives `LoginCredentials`, verifies, creates `access_token`.
    *   **Backend Response:** Sends `{"access_token": "...", "token_type": "bearer"}`.
    *   **Frontend (`authService.ts`):** Receives token, saves it to `localStorage`, then calls `api.get('/users/me', { headers: { Authorization: `Bearer ${token}` } })`.
    *   **Backend (`users.py`):** `read_users_me` endpoint uses `get_current_user` to validate the token and returns the `User` object.
    *   **Frontend (`AuthContext.tsx`):** Receives user data, updates global state, and the user is now logged in and redirected to the dashboard.

---

## 5. Future Enhancements (Planned/Potential)

This project provides a solid foundation. Here are some areas where it can be expanded:

*   **Property Management:** Implement full CRUD operations for properties in `app/routers/properties.py` and corresponding frontend pages/components.
*   **User Profiles:** Allow users to update their profile information (e.g., phone number, profile picture).
*   **Role-Based Access Control (RBAC):** Implement more granular permissions based on user roles (tenant, landlord, admin).
*   **Notifications:** Add real-time notifications for events (e.g., new messages, rent due).
*   **Payments Integration:** Integrate with a payment gateway for rent collection.
*   **Testing:** Expand unit and integration tests for both frontend and backend to ensure robustness.
*   **Deployment:** Set up continuous integration/continuous deployment (CI/CD) pipelines for automated deployment.

---

## 6. Conclusion

This documentation aims to provide a clear and comprehensive understanding of the Rent Management System's backend. By understanding its structure, technologies, and how it integrates with the frontend, you should be well-equipped to contribute to its development. Happy coding!