# User Management Microservice

This microservice handles user authentication, authorization, and profile management for the Rental Management System. It is built with FastAPI, PostgreSQL, and uses JWT for secure authentication.

## Features

-   **Standard Registration:** Users can register with email/password.
-   **Secure Login:** Email/password login returns JWT (Access and Refresh Tokens) with comprehensive user claims.
-   **Google OAuth 2.0:** Register/login via Google (implementation details for Google OAuth callback not fully provided in this microservice, assumed to be handled externally or integrated via a separate endpoint).
-   **Profile Management:** Get/update user profiles (name, email, role, phone number, preferred language, preferred currency).
-   **RBAC:** Role-Based Access Control with roles: Admin, Owner, Tenant, Broker. Endpoints are restricted based on user roles.
-   **Administrative Functions:** Admins can list all users or get a user by ID.
-   **Mandatory Password Change:** For pre-seeded admin accounts on first login.
-   **JWT Verification Endpoint:** For other microservices to verify user details, returning `{user_id, role, email, phone_number, preferred_language}`.
-   **Multilingual Support:** For English, Amharic, and Afaan Oromo.
-   **Phone Number Encryption:** `phone_number` is stored encrypted using AES-256.
-   **Database Retry Logic:** Implemented for robustness against transient database issues.

## Technologies Used

-   Python 3.10+
-   FastAPI
-   PostgreSQL (asyncpg)
-   SQLAlchemy (ORM) & Alembic (Migrations)
-   Pydantic (Data Validation & Settings)
-   `passlib[bcrypt]` (Password Hashing)
-   `python-jose[cryptography]` (JWT)
-   `cryptography` (AES Encryption)
-   `asyncio-retry` (for database retries)

## Setup Instructions

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd Rent-managment-system
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python3 -m venv Bate
    source Bate/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    ./Bate/bin/pip install -r backend/user_service/requirements.txt
    ```

4.  **Configure Environment Variables:**
    Create a `.env` file in the `backend/user_service/` directory based on `backend/user_service/.env.example`. Ensure you generate a strong `AES_SECRET_KEY`.
    ```ini
    # backend/user_service/.env
    DATABASE_URL="postgresql+asyncpg://dagi:your_password@localhost:5432/rent_db"
    JWT_SECRET="your_jwt_secret_key_here"
    JWT_ALGORITHM="HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES=15
    REFRESH_TOKEN_EXPIRE_DAYS=7
    DEFAULT_ADMIN_EMAIL="admin@example.com"
    DEFAULT_ADMIN_PASSWORD="your_secure_default_admin_password"
    # Optional second admin
    # DEFAULT_ADMIN_EMAIL_2="admin2@example.com"
    # DEFAULT_ADMIN_PASSWORD_2="your_second_secure_default_admin_password"
    GOOGLE_CLIENT_ID="your_google_client_id"
    GOOGLE_CLIENT_SECRET="your_google_client_secret"
    AES_SECRET_KEY="your_aes_secret_key_here_generate_a_new_one"
    ```
    **Important:** Replace placeholders with your actual values. For `AES_SECRET_KEY`, generate one using `python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"`. 

5.  **Run Database Migrations:**
    Ensure your PostgreSQL database is running and accessible via the `DATABASE_URL`. The `migrate.sh` script (or Alembic commands) should be used to apply migrations and create tables. The `seed_admin` function will automatically pre-seed admin users on application startup if they don't exist.
    ```bash
    # Assuming you have Alembic configured and migrate.sh runs it
    chmod +x migrate.sh
    ./migrate.sh
    ```
    Alternatively, you can manually apply the schema from `backend/user_service/sql/schema.sql` if Alembic is not fully set up yet.

## Running the Application

To start the FastAPI application:

```bash
./Bate/bin/uvicorn backend.user_service.app.main:app --host 0.0.0.0 --port 8000 --reload
```

The API documentation will be available at `http://localhost:8000/docs` (Swagger UI) and `http://localhost:8000/redoc` (ReDoc).

## Running Tests

To run the unit and integration tests:

```bash
./Bate/bin/pytest backend/user_service/tests
```

## API Documentation

### Authentication Endpoints (`/api/v1/auth`)

-   **`POST /api/v1/auth/login`**
    -   **Description:** Authenticates a user with email and password. Returns Access and Refresh Tokens with user claims. Requires password change for pre-seeded admins on first login.
    -   **Parameters:** `username` (email), `password` (form data).
    -   **Returns:** Access and Refresh Tokens.

-   **`POST /api/v1/auth/refresh`**
    -   **Description:** Refreshes an expired access token using a refresh token.
    -   **Parameters:** `refresh_token` (body).
    -   **Returns:** New Access and Refresh Tokens.

-   **`POST /api/v1/auth/change-password`**
    -   **Description:** Allows an authenticated user to change their password.
    -   **Parameters:** `old_password`, `new_password` (body).
    -   **Permissions:** Authenticated users.

-   **`GET /api/v1/auth/verify`**
    -   **Description:** Verifies the validity of an access token and returns essential user details for inter-service communication.
    -   **Returns:** `{user_id, role, email, phone_number, preferred_language}`.
    -   **Permissions:** Authenticated users.

### User Endpoints (`/api/v1/users`)

-   **`POST /api/v1/users/register`**
    -   **Description:** Registers a new user. Prevents registration with `ADMIN` role. Validates phone number format.
    -   **Parameters:** `email`, `password`, `full_name`, `phone_number` (optional, `+251[79]XXXXXXXX`), `preferred_language`, `preferred_currency` (body).
    -   **Returns:** Newly created user object.

-   **`GET /api/v1/users/me`**
    -   **Description:** Retrieves the profile of the currently authenticated user.
    -   **Permissions:** Authenticated users.

-   **`PUT /api/v1/users/me`**
    -   **Description:** Updates the profile of the currently authenticated user. Encrypts updated phone number.
    -   **Parameters:** `full_name`, `phone_number` (optional, `+251[79]XXXXXXXX`), `preferred_language`, `preferred_currency` (body).
    -   **Permissions:** Authenticated users.

### Admin Endpoints (`/api/v1/admin`)

-   **`GET /api/v1/admin/users`**
    -   **Description:** Retrieves a list of all users.
    -   **Parameters:** `skip`, `limit` (query).
    -   **Permissions:** Admin users only.

-   **`GET /api/v1/admin/users/{user_id}`**
    -   **Description:** Retrieves details of a specific user by ID.
    -   **Parameters:** `user_id` (path).
    -   **Permissions:** Admin users only.

## Deployment

This microservice can be containerized using the provided `Dockerfile` and deployed to platforms like AWS ECS/Fargate.

```bash
# Build the Docker image
docker build -t user-management-service .

# Run the Docker container (example)
docker run -p 8000:8000 --env-file backend/user_service/.env user-management-service
```

## Ethiopia-Specific Design

-   **Phone Number Validation:** Supports Ethiopian phone number format (e.g., `+251912345678`).
-   **Multilingual Support:** `preferred_language` for English, Amharic, Afaan Oromo.
-   **Currency:** `preferred_currency` defaults to `ETB`.
-   **Unicode Support:** `full_name` supports Unicode characters for Amharic/Afaan Oromo names.

## Integration with Payment Processing

Other microservices (e.g., Payment Processing) can use the `/api/v1/auth/verify` endpoint to retrieve authenticated user details (ID, role, email, phone, language) for authorization and personalized responses. For pay-per-post automation, the Payment Processing service can verify the user's role (e.g., `Owner`) and use the provided `user_id` and `email` to process payments via Chapa.co's sandbox.

## Future Enhancements

-   **Refresh Token Cleanup:** Implement a cron-like job to periodically clean up expired refresh tokens from the database.
-   **Google OAuth Callback:** Fully implement the Google OAuth callback logic within the microservice.
-   **Rate Limiting:** Integrate with an API Gateway (e.g., AWS API Gateway) for rate limiting to prevent abuse.
-   **Logging:** Implement structured logging (e.g., `structlog`) to CloudWatch for better observability and security auditing.
-   **Redis Caching:** Implement Redis caching for frequently accessed data, especially for the `/api/v1/auth/verify` endpoint, to improve scalability.