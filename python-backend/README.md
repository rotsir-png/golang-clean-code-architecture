# Python FastAPI Backend

A Python implementation inspired by the Go Clean Architecture repository.

## Tech Stack

- Python
- FastAPI
- PostgreSQL
- JWT Authentication
- Pytest

## Features

- User Registration and Login
- Password Hashing
- Access and Refresh Tokens
- Refresh Token Rotation
- Logout with Refresh Token Revocation
- Protected User Profile
- Read-only User CRUD endpoints
- Permission-based User Listing
- PostgreSQL Table Description
- Automated Tests

## Prerequisites

- Python
- PostgreSQL

## Installation

### 1. Create Virtual Environment

From the `python-backend` directory:

```powershell
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use `.\.venv\Scripts\python.exe` directly for the commands below.

### 2. Install Dependencies

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### 3. Create PostgreSQL Database

Create a database named `khaojai_db`.

Then run the SQL schema from the `python-backend` directory:

```powershell
psql -U postgres -d khaojai_db -f sql/schema.sql
```

### 4. Configure Environment Variables

Copy `.env.example` to `.env`:

```powershell
Copy-Item .env.example .env
```

Edit `.env` and set:

- `KHAOJAI_DB_PASSWORD`: Your PostgreSQL password
- `KHAOJAI_JWT_SECRET`: A securely generated random secret

Never commit `.env` to Git.

### 5. Run the API

```powershell
.\.venv\Scripts\python.exe -m uvicorn main:app --reload
```

Open the API documentation:

http://127.0.0.1:8000/docs

## Run Automated Tests

```powershell
.\.venv\Scripts\python.exe -m pytest tests/ -v
```

## Architecture

The project is organized into:

- `domain/` — Domain models and repository interfaces
- `usecases/` — Application business logic
- `infrastructure/` — PostgreSQL repositories, JWT, and password hashing
- `main.py` — FastAPI routes and dependency wiring
- `tests/` — Automated tests

## Security Notes

- Passwords are stored as hashes.
- JWT access tokens have a limited lifetime.
- Refresh tokens are stored as SHA-256 hashes.
- Refresh tokens are rotated and revoked on logout.
- User listing and database schema description are permission-controlled.
- Logout does not immediately invalidate previously issued access tokens.

## Known Limitations

- CRUD supports a limited read-only implementation for users.
- MongoDB is not implemented.
- The application uses a local PostgreSQL setup.
- Automated tests do not cover all database integration scenarios.
- Database migrations and production deployment configuration are not yet implemented.
## Architecture Explanation

### Overview

This project is a Python FastAPI implementation based on the original Go Clean Architecture repository.

The goal is to separate business logic, HTTP handling, and database operations so that each layer has a clear responsibility.

### Project Structure

```text
python-backend/
├── main.py
├── domain/
│   ├── user.py
│   ├── user_repository.py
│   └── crud_repository.py
├── usecases/
│   ├── register_user.py
│   ├── login_user.py
│   └── read_crud.py
├── interfaces/
│   ├── auth_routes.py
│   └── crud_routes.py
├── infrastructure/
│   ├── database.py
│   ├── user_repository.py
│   ├── crud_repository.py
│   ├── password_hasher.py
│   ├── jwt_service.py
│   ├── refresh_token_repository.py
│   └── permission_repository.py
├── sql/
│   └── schema.sql
└── tests/
```

### Layer Responsibilities

**1. Domain Layer**

Defines the core user model and repository contracts.

This layer does not depend on FastAPI or PostgreSQL implementation details.

**2. Use Case Layer**

Contains application operations such as user registration, login validation, and reading records.

Business operations are separated from HTTP route handling. Repository interfaces and injected password functions help reduce coupling to infrastructure implementations.

**3. Interface Layer**

Uses FastAPI routers to receive HTTP requests, validate request data, invoke application operations, and return HTTP responses.

Authentication and CRUD endpoints are separated into different route modules.

**4. Infrastructure Layer**

Provides technical implementations for PostgreSQL access, password hashing, JWT creation and validation, refresh token storage, and permission queries.

**5. Application Entry Point**

`main.py` creates the FastAPI application and registers the authentication and CRUD routers.

### Example: User Login Flow

1. The client sends a request to `POST /users/login`.
2. The authentication router receives the request.
3. The login use case retrieves the user through a repository.
4. The password is verified against its stored hash.
5. The authentication router creates JWT access and refresh tokens using infrastructure services.
6. The refresh token is recorded in PostgreSQL as a hash.
7. The API returns the authentication result.

### Design Decisions

- **FastAPI:** Used for REST API development, request validation, and interactive API documentation.
- **PostgreSQL:** Used for persistent user and authentication data.
- **Repository abstraction:** Separates application operations from database-specific implementations.
- **Password hashing:** Avoids storing plaintext passwords.
- **JWT authentication:** Uses separate access and refresh tokens.
- **Refresh token rotation:** Replaces refresh tokens after successful refresh requests.
- **Automated testing:** Uses pytest with fake repositories to test application behavior without requiring a database for every test.

### Differences and Limitations

This implementation preserves the main user registration and authentication concepts of the original Go project while adapting them to Python and FastAPI.

It is not a complete one-to-one port of every Go component. The current CRUD implementation focuses on read operations for users, and MongoDB support has not been implemented.

The application also uses a local PostgreSQL configuration. Production deployment, database migrations, and comprehensive database integration test automation are outside the current implementation scope.

### Validation

The project includes automated tests covering authentication, API behavior, CRUD operations, permissions, and token handling.

Manual API testing with PostgreSQL has also been performed for registration, login, and duplicate-email handling.

These tests provide evidence for the tested behaviors but do not guarantee complete production readiness.