
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
