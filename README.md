# 📁 Project Dashboard API

A secure, full-featured project management service with user authentication, document upload, and collaboration.

Built with **FastAPI**, **PostgreSQL**, and **JWT authentication**.

---

## ✨ Features

- 🔐 **User Authentication**  
  Register, login, and secure all routes with JWT
- 📂 **Project Management**  
  Create, list, update, and delete projects
- 📎 **Document Upload & Management**  
  Upload, download, update, and delete files per project
- 👥 **Project Sharing**  
  Invite users to projects with participant permissions
---

## 🚀 Quick Start

### 1. Clone the repo
```bash
git clone https://github.com/barackhu1/project-management-service.git
cd project-management-service
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up environment
Create `env` file:

```bash
DB_NAME=project_db
DB_USER=your_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
SECRET_KEY=your-super-secret-key-change-in-production
ENCRYPTION_ALGORITHM=algorithm-that-encrypts
ACCESS_TOKEN_EXPIRE_MINUTES=60
UPLOADS_PATH=path-where-the-docs-will-be-uploaded
```

### 4. Set up PostgreSQL

```bash
CREATE DATABASE project_db;
-- Run schema.sql to create tables
```

### 5. Run the server
```bash
uvicorn app.main:app --reload
```
👉 Open http://127.0.0.1:8000/docs to see the interactive API docs (Swagger UI).

### 🧪 Run Tests

```bash
pytest tests/ -v
```

## 🔐 API Endpoints

| Method | Endpoint | Description |
|--------|---------|-------------|
| `POST` | `/auth` | Register a new user |
| `POST` | `/login` | Login and get JWT token |
| `POST` | `/projects` | Create a project |
| `GET` | `/projects` | List all accessible projects |
| `GET` | `/projects/{id}/info` | Get project details |
| `PUT` | `/projects/{id}/info` | Update project |
| `DELETE` | `/projects/{id}` | Delete project (owner only) |
| `POST` | `/project/{id}/documents` | Upload a document |
| `GET` | `/project/{id}/documents` | List project documents |
| `GET` | `/document/{id}` | Download a document |
| `PUT` | `/document/{id}` | Update a document |
| `DELETE` | `/document/{id}` | Delete a document |
| `POST` | `/project/{id}/invite?user=username` | Invite user to project (owner only) |

## 🗃️ Project Structure
```bash
project-management-service/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── routers/
│   │   ├── auth.py
│   │   ├── projects.py
│   │   └── documents.py
│   ├── crud/
│   │   ├── projects.py
│   │   ├── documents.py
│   │   └── users.py
│   ├── schemas/
│   │   ├── projects.py
│   │   └── users.py
│   └── utils/
│       ├── auth.py
│       ├── auth_dependency.py
│       └── db.py
├── uploads/                  
├── tests/
│   └── test_projects.py   
├── .env                 
├── schema.sql              
├── requirements.txt
└── README.md
```

## 🧰 Technologies Used

- FastAPI – Modern Python web framework
- PostgreSQL – Relational database
- Pydantic – Data validation
- bcrypt – Password hashing
- PyJWT – Token generation
- pytest – Testing

## 🙌 Acknowledgements
Built as a full-stack learning project to demonstrate API design, authentication, and file handling.