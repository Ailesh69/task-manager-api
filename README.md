# Task Manager API
A robust and production-ready RESTful API built with **FastAPI** and **SQLAlchemy** to manage users and their associated tasks. Features JWT authentication, database migrations, rate limiting, input validation, and LLM-powered chat with persistent memory.

## 🚀 Features

- **User Management**: Create and retrieve user profiles
- **Task Tracking**: Create, update, and delete tasks for specific users
- **Data Validation**: Strong typing and request validation using Pydantic schemas with custom validators
- **Database Integration**: Persistent storage using PostgreSQL and SQLAlchemy ORM
- **Auto-generated Documentation**: Interactive API docs via Swagger UI

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

### ⚡ Advanced API Capabilities
- Pagination support (skip, limit)
- Filtering by completion status (completed)
- Dynamic sorting (sort, order)
- Automatic timestamp tracking (created_at)
- Task priority field (low, medium, high)

### 🗄 Database Migrations
- Alembic migrations for safe schema changes
- No data loss when updating database schema
- Full migration history tracked

### 🚦 Rate Limiting
- 10 requests/minute on general endpoints
- Stricter 5 requests/minute on /login to prevent brute force attacks

### ✅ Input Validation
- Password must be 8+ characters with a number and special character
- Email must be valid format
- Contact number must be exactly 10 digits
- Task title cannot be empty or exceed 100 characters
- Priority must be low, medium, or high

### 🤖 LLM Chat with Persistent Memory
- AI chat powered by Groq LLaMA 3.3 70B
- Full conversation history stored in PostgreSQL
- LLM remembers context across sessions
- Each user has their own isolated conversation history

## 🛠️ Tech Stack
- **Framework**: FastAPI
- **ORM**: SQLAlchemy
- **Database**: PostgreSQL
- **Migrations**: Alembic
- **Validation**: Pydantic
- **Rate Limiting**: SlowAPI
- **LLM**: Groq LLaMA 3.3 70B
- **Server**: Uvicorn

## 📋 Prerequisites
- Python 3.10+
- PostgreSQL installed and running
- A database named `taskmanager` created in your PostgreSQL instance
- Groq API key (get free at console.groq.com)

## ⚙️ Installation & Setup

1. **Clone the repository**:
```bash
   git clone https://github.com/Ailesh69/task-manager-api.git
   cd task-manager-api
```

2. **Create a virtual environment**:
```bash
   python -m venv .venv
   source .venv/bin/activate
```

3. **Install dependencies**:
```bash
   pip install -r requirements.txt
```

4. **Create `.env` file** in the root folder:
```
   DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/taskmanager
   SECRET_KEY=your-secret-key
   ALGORITHM=HS256
   GROQ_API_KEY=your-groq-api-key
```

5. **Run migrations**:
```bash
   alembic upgrade head
```

6. **Start the server**:
```bash
   uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

## 📖 API Endpoints

### Users
- `POST /users/` - Create a new user
- `GET /users/` - List all users (protected)

### Tasks
- `GET /tasks/me` - Get all tasks for current user (protected)
- `POST /tasks` - Create a new task (protected)
- `PUT /tasks/{task_id}` - Update task completion status (protected)
- `DELETE /task/{task_id}` - Delete a task (protected)

### Authentication
- `POST /login` - Login and get JWT access token

### Chat
- `POST /chat` - Chat with AI assistant (protected, persistent memory)

## 🔍 Interactive Documentation
`http://127.0.0.1:8000/docs`

## 📝 License
MIT
