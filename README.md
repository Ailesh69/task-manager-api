# Task Manager API

A robust and lightweight RESTful API built with **FastAPI** and **SQLAlchemy** to manage users and their associated tasks. This project demonstrates a clean implementation of the CRUD pattern with a PostgreSQL backend.

## 🚀 Features

- **User Management**: Create and retrieve user profiles.
- **Task Tracking**: Create, update, and delete tasks for specific users.
- **Data Validation**: Strong typing and request validation using Pydantic schemas.
- **Database Integration**: Persistent storage using PostgreSQL and SQLAlchemy ORM.
- **Auto-generated Documentation**: Interactive API docs via Swagger UI.

### 🔐 Authentication
- JWT-based login system
- Access tokens with expiration
- Environment-based secret configuration (.env)

### 🛡 Route Protection
- Protected endpoints using Bearer token authentication
- Only authenticated users can access task routes

### 🔒 Authorization
- Users can only access their own tasks
- User identity extracted from JWT payload
- Prevents cross-user data access

   ⚡ Advanced API Capabilities

- Pagination support (skip, limit)
- Filtering by completion status (completed)
- Dynamic sorting (sort, order)
- Automatic timestamp tracking (created_at)

## 🛠️ Tech Stack

- **Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **ORM**: [SQLAlchemy](https://www.sqlalchemy.org/)
- **Database**: [PostgreSQL](https://www.postgresql.org/)
- **Validation**: [Pydantic](https://docs.pydantic.dev/)
- **Server**: [Uvicorn](https://www.uvicorn.org/)

## 📋 Prerequisites

- Python 3.10+
- PostgreSQL installed and running.
- A database named `taskmanager` created in your PostgreSQL instance.

## ⚙️ Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/taskmanager.git
   cd taskmanager
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install fastapi uvicorn sqlalchemy psycopg2-binary pydantic
   ```

4. **Configure Database**:
   Update the connection string in `app/db.py` with your PostgreSQL credentials:
   ```python
   engine = create_engine("postgresql://<username>:<password>@localhost:5432/taskmanager")
   ```

5. **Run the application**:
   ```bash
   uvicorn app.main:app --reload
   ```

The API will be available at `http://127.0.0.1:8000`.

## 📖 API Endpoints

### Users
- `POST /user/` - Create a new user.
- `GET /user/` - List all users.

### Tasks
- `GET /user/{user_id}/task/` - Get all tasks for a specific user.
- `POST /user/{user_id}/task/` - Create a new task for a user.
- `PUT /user/{user_id}/task/{task_id}` - Update the completion status of a task.
- `DELETE /task/{task_id}` - Remove a task.

## 🔍 Interactive Documentation

Once the server is running, you can access the interactive Swagger UI documentation at:
`http://127.0.0.1:8000/docs`

## 📝 License

This project is open-source and available under the MIT License.