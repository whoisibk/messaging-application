# 💬 Real-Time Messaging Application

<div align="center">

![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-blue.svg)
![WebSocket](https://img.shields.io/badge/WebSocket-Enabled-orange.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

*A production-ready, real-time messaging platform combining REST API authentication with persistent WebSocket connections for instant, bi-directional chat and PostgreSQL data persistence.*

[Features](#-features) • [Architecture](#-architecture) • [Quick Start](#-quick-start) • [API Documentation](#-api-documentation) • [Contributing](#-contributing)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Architecture](#-architecture)
- [Technology Stack](#-technology-stack)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Configuration](#%EF%B8%8F-configuration)
- [Usage](#-usage)
- [API Documentation](#-api-documentation)
- [WebSocket Protocol](#-websocket-protocol)
- [Database Schema](#-database-schema)
- [Client Application](#-client-application)
- [Development](#-development)
- [Testing](#-testing)
- [Deployment](#-deployment)
- [Roadmap](#-roadmap)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 Overview

This is a **full-stack real-time messaging application** built with modern Python technologies. It demonstrates best practices in building scalable, secure, and maintainable chat applications with features like:

- 🔐 **JWT-based authentication** with OAuth2 password flow
- 🚀 **Real-time messaging** using WebSocket connections
- 💾 **Persistent message storage** in PostgreSQL
- 🏗️ **Clean architecture** with separation of concerns
- 📝 **Type-safe** with Pydantic models
- 🔄 **Database migrations** with Alembic
- 🖥️ **CLI client** for testing and demonstration

---

## ✨ Features

### Core Functionality

- ✅ **User Authentication & Authorization**
  - Secure user registration with password hashing
  - JWT token-based authentication
  - OAuth2 password flow implementation
  - Token refresh and validation
  - Per-user token isolation for multi-session use

- ✅ **Real-Time Messaging**
  - WebSocket connections for instant message delivery
  - Bi-directional communication
  - Online/offline user detection
  - Offline message delivery — undelivered messages are pushed on reconnect

- ✅ **Conversation Management**
  - One-on-one conversations
  - Automatic conversation creation
  - Message history retrieval with resolved usernames
  - Conversation listing with last message preview

- ✅ **Data Persistence**
  - PostgreSQL database integration
  - SQLAlchemy ORM for database operations
  - Alembic for database migrations
  - UUID-based primary keys for scalability

### Technical Features

- 🔒 **Security First**
  - Password hashing with industry-standard algorithms
  - JWT token expiration and validation
  - SQL injection prevention through ORM
  - CORS configuration ready

- 🏗️ **Clean Architecture**
  - Layered architecture (routes, services, models)
  - Dependency injection
  - Separation of concerns — API layer, actions layer, and menu layer are distinct
  - Type hints throughout

- 📊 **API Design**
  - RESTful API endpoints
  - Automatic API documentation (Swagger/OpenAPI)
  - Request/response validation with Pydantic
  - Proper HTTP status codes

---

## 🏛️ Architecture

### System Architecture

```
┌─────────────┐         ┌──────────────────────────────────────┐
│   Client    │◄───────►│          FastAPI Server              │
│             │  HTTP   │                                      │
│  - CLI App  │  WS     │  ┌────────────┐  ┌──────────────┐  │
│  - Web App  │         │  │   Routes   │  │  WebSocket   │  │
│  - Mobile   │         │  │            │  │   Manager    │  │
└─────────────┘         │  │ • Users    │  │              │  │
                        │  │ • Messages │  │ • Connect    │  │
                        │  │ • Convos   │  │ • Disconnect │  │
                        │  └──────┬─────┘  └──────┬───────┘  │
                        │         │                │          │
                        │  ┌──────▼────────────────▼──────┐  │
                        │  │      Services Layer          │  │
                        │  │                              │  │
                        │  │  • User Operations           │  │
                        │  │  • Message Operations        │  │
                        │  │  • Conversation Operations   │  │
                        │  └──────────────┬───────────────┘  │
                        │                 │                  │
                        │  ┌──────────────▼───────────────┐  │
                        │  │     Database (PostgreSQL)    │  │
                        │  │                              │  │
                        │  │  • Users Table               │  │
                        │  │  • Messages Table            │  │
                        │  │  • Conversations Table       │  │
                        │  └──────────────────────────────┘  │
                        └──────────────────────────────────────┘
```

### Request Flow

**REST API Request:**
```
Client → Router → Service → Database → Service → Router → Client
```

**WebSocket Message:**
```
Client A → WS Manager → Service → Database → WS Manager → Client B
```

---

## 🛠️ Technology Stack

### Backend
- **[FastAPI](https://fastapi.tiangolo.com/)** - Modern, fast web framework for building APIs
- **[Python 3.9+](https://www.python.org/)** - Programming language
- **[PostgreSQL](https://www.postgresql.org/)** - Robust relational database
- **[SQLAlchemy](https://www.sqlalchemy.org/)** - SQL toolkit and ORM
- **[Alembic](https://alembic.sqlalchemy.org/)** - Database migration tool
- **[Pydantic](https://pydantic-docs.helpmanual.io/)** - Data validation using Python type hints
- **[python-jose](https://python-jose.readthedocs.io/)** - JWT implementation
- **[passlib](https://passlib.readthedocs.io/)** - Password hashing library
- **[Uvicorn](https://www.uvicorn.org/)** - ASGI server

### Client
- **Python** - CLI client implementation
- **websockets** - WebSocket client library
- **httpx** - Async-capable HTTP library for API calls

---

## 📁 Project Structure

```
messaging-application/
│
├── 📂 app/                          # Main FastAPI application
│   ├── 📄 __init__.py
│   ├── 📄 main.py                   # Application entry point & FastAPI instance
│   ├── 📄 database.py               # Database connection setup
│   ├── 📄 models.py                 # SQLAlchemy database models
│   ├── 📄 schemas.py                # Pydantic request/response models
│   ├── 📄 websocket_endpoint.py     # WebSocket route endpoint
│   ├── 📄 websocket_manager.py      # WebSocket connection manager
│   │
│   ├── 📂 routes/                   # API route handlers
│   │   ├── 📄 users.py              # User authentication & profile routes
│   │   ├── 📄 messages.py           # Message sending & retrieval routes
│   │   └── 📄 conversations.py      # Conversation management routes
│   │
│   ├── 📂 services/                 # Business logic layer
│   │   ├── 📄 user_ops.py           # User CRUD operations
│   │   ├── 📄 message_ops.py        # Message operations
│   │   └── 📄 conversation_ops.py   # Conversation operations
│   │
│   └── 📂 utils/                    # Utility functions
│       └── 📄 auth.py               # JWT & password hashing utilities
│
├── 📂 client/                       # CLI client application
│   ├── 📄 __init__.py
│   ├── 📄 main.py                   # Menu system — calls action functions only
│   ├── 📄 actions.py                # Orchestration layer — business logic & output
│   ├── 📄 auth.py                   # Authentication handlers (login/signup/logout)
│   ├── 📄 api.py                    # Pure HTTP layer — fetches and returns data
│   ├── 📄 ws.py                     # WebSocket client — real-time chat session
│   └── 📄 token_storage.py          # Token persistence (scoped per CHAT_USER)
│
├── 📂 alembic/                      # Database migrations
│   ├── 📄 env.py
│   ├── 📄 script.py.mako
│   └── 📂 versions/
│
├── 📄 alembic.ini                   # Alembic configuration
├── 📄 .gitignore
└── 📄 README.md                     # This file
```

---

## 🚀 Installation

### Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.9+** ([Download](https://www.python.org/downloads/))
- **PostgreSQL 12+** ([Download](https://www.postgresql.org/download/))
- **pip** (Python package manager)
- **git** (Version control)

### Step 1: Clone the Repository

```bash
git clone https://github.com/whoisibk/messaging-application.git
cd messaging-application
```

### Step 2: Create Virtual Environment

```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Database Setup

```bash
# Using psql:
psql -U postgres
CREATE DATABASE messaging_app_db;
\q
```

### Step 5: Configure Environment

Create a `.env` file in the project root (see [Configuration](#%EF%B8%8F-configuration)).

### Step 6: Run Database Migrations

```bash
alembic upgrade head
```

---

## ⚙️ Configuration

Create a `.env` file in the project root:

```env
# Database
DATABASE_URL=postgresql://username:password@localhost/messaging_app_db

# JWT
SECRET_KEY=your-secret-key-here-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Server
HOST=127.0.0.1
PORT=8000

# Client
API_BASE_URL=http://127.0.0.1:8000

# Multi-session isolation — set per terminal to run two clients on the same machine
CHAT_USER=alice
```

### Generate a Secret Key

```python
import secrets
print(secrets.token_urlsafe(32))
```

---

## 💻 Usage

### Starting the Server

```bash
# Development mode with auto-reload
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

The server will start at `http://127.0.0.1:8000`

### Using the CLI Client

```bash
python -m client.main
```

The CLI has two menu screens:

**When not logged in:**
```
1. Login
2. Sign Up
3. Exit
```

**When logged in:**
```
1. View my profile
2. Send a message      ← opens real-time WebSocket chat, type /quit to exit
3. View messages       ← pick a conversation, see history with usernames
4. View conversations  ← list all conversations with last message preview
5. Logout
```

The menu loops after every action — you are always returned to the menu until you log out or exit.

### Running Multiple Sessions on the Same Machine

Token files are scoped to `CHAT_USER`, so two terminals can be logged in as different users simultaneously:

```bash
# Terminal 1
CHAT_USER=alice python -m client.main

# Terminal 2
CHAT_USER=bob python -m client.main
```

### API Documentation

Once the server is running:

- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

---

## 📚 API Documentation

### Authentication Endpoints

#### Sign Up
```http
POST /users/signup
Content-Type: application/json

{
  "userName": "johndoe",
  "userEmail": "john@example.com",
  "password": "securepassword123",
  "firstName": "John",
  "lastName": "Doe"
}
```

**Response (200 OK):**
```json
{
  "userId": "550e8400-e29b-41d4-a716-446655440000",
  "userName": "johndoe",
  "userEmail": "john@example.com",
  "firstName": "John",
  "lastName": "Doe"
}
```

#### Login
```http
POST /users/login
Content-Type: application/x-www-form-urlencoded

username=johndoe&password=securepassword123
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Message Endpoints

#### Get Messages in Conversation
```http
GET /messages/{conversationId}
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
[
  {
    "messageId": "660e8400-e29b-41d4-a716-446655440000",
    "senderId": "550e8400-e29b-41d4-a716-446655440000",
    "recipientId": "770e8400-e29b-41d4-a716-446655440000",
    "conversationId": "880e8400-e29b-41d4-a716-446655440000",
    "messageText": "Hello, how are you?",
    "timestamp": "2026-04-14T10:30:00",
    "delivered": true
  }
]
```

### Conversation Endpoints

#### Get All Conversations
```http
GET /conversations/get-conversations
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
[
  {
    "conversationId": "880e8400-e29b-41d4-a716-446655440000",
    "user1_Id": "550e8400-e29b-41d4-a716-446655440000",
    "user2_Id": "770e8400-e29b-41d4-a716-446655440000",
    "dateCreated": "2026-04-14T09:00:00",
    "lastMessage": "Hello, how are you?"
  }
]
```

#### Delete Conversation
```http
DELETE /conversations/{conversationId}
Authorization: Bearer <access_token>
```

---

## 🔌 WebSocket Protocol

### Connection

```
ws://127.0.0.1:8000/ws/chat?token=<access_token>
```

### Sending a Message

```json
{
  "recipientId": "770e8400-e29b-41d4-a716-446655440000",
  "message": "Hello!"
}
```

### Server Events

All server-to-client frames are JSON with an `event` field:

**Incoming message (`event: "message"`):**
```json
{
  "event": "message",
  "data": {
    "senderId": "550e8400-e29b-41d4-a716-446655440000",
    "message": "Hello!",
    "timestamp": "2026-04-14T10:30:00"
  }
}
```

**Delivery acknowledgement (`event: "ack"`):**
```json
{
  "event": "ack",
  "data": {
    "deliveryStatus": "delivered"
  }
}
```

**Error (`event: "error"`):**
```json
{
  "event": "error",
  "detail": "Recipient not found"
}
```

### Connection Manager

The `ConnectionManager` handles:
- ✅ WebSocket connection lifecycle
- ✅ Online/offline user detection
- ✅ Message routing to connected users
- ✅ Offline message delivery on reconnect
- ✅ Marking messages as delivered

---

## 🗄️ Database Schema

### Users Table

| Column | Type | Constraints |
|--------|------|-------------|
| userId | UUID | PRIMARY KEY |
| userName | VARCHAR(15) | UNIQUE, NOT NULL |
| userEmail | VARCHAR(100) | UNIQUE, NOT NULL |
| passwordHash | VARCHAR(255) | NOT NULL |
| firstName | VARCHAR(50) | NOT NULL |
| lastName | VARCHAR(50) | NOT NULL |
| dateCreated | TIMESTAMP | NOT NULL |

### Messages Table

| Column | Type | Constraints |
|--------|------|-------------|
| messageId | UUID | PRIMARY KEY |
| senderId | UUID | FOREIGN KEY → user.userId |
| recipientId | UUID | FOREIGN KEY → user.userId |
| conversationId | UUID | FOREIGN KEY → conversation.conversationId |
| messageText | VARCHAR(250) | NOT NULL |
| timestamp | TIMESTAMP | NOT NULL |
| delivered | BOOLEAN | NOT NULL, default false |

### Conversations Table

| Column | Type | Constraints |
|--------|------|-------------|
| conversationId | UUID | PRIMARY KEY |
| user1_Id | UUID | FOREIGN KEY → user.userId |
| user2_Id | UUID | FOREIGN KEY → user.userId |
| dateCreated | TIMESTAMP | NOT NULL |
| lastMessage | VARCHAR(250) | nullable |

### Entity Relationship Diagram

```
┌──────────────────┐
│      User        │
├──────────────────┤
│ userId (PK)      │
│ userName         │
│ userEmail        │
│ passwordHash     │
│ firstName        │
│ lastName         │
│ dateCreated      │
└────────┬─────────┘
         │
         │ 1:N
         │
┌────────▼─────────┐         ┌──────────────────┐
│   Conversation   │────────►│     Message      │
├──────────────────┤   1:N   ├──────────────────┤
│ conversationId   │         │ messageId (PK)   │
│ user1_Id (FK)    │         │ senderId (FK)    │
│ user2_Id (FK)    │         │ recipientId (FK) │
│ dateCreated      │         │ conversationId   │
│ lastMessage      │         │ messageText      │
└──────────────────┘         │ timestamp        │
                             │ delivered        │
                             └──────────────────┘
```

---

## 🖥️ Client Application

### Architecture

The client is split into three layers with clear responsibilities:

```
client/
├── main.py          # Menu system only — calls action functions, no logic
├── actions.py       # Orchestration layer — combines API calls, handles I/O & printing
├── auth.py          # Login / signup / logout flows
├── api.py           # Pure HTTP layer — one function per endpoint, no side effects
├── ws.py            # WebSocket client — real-time chat session
└── token_storage.py # Token persistence, scoped to CHAT_USER env var
```

| Layer | Responsibility |
|-------|---------------|
| `main.py` | Displays menus, reads user input, calls the right action |
| `actions.py` | Orchestrates API calls, formats output, handles conversation/message flows |
| `api.py` | Makes HTTP requests, returns raw data — no printing |
| `ws.py` | Manages WebSocket connection, resolves sender IDs to usernames in real time |

### Features

- 🔐 **User authentication** (login/signup/logout)
- 💬 **Real-time messaging** via WebSocket with usernames displayed
- 📋 **Message history** with resolved usernames and timestamps
- 📋 **Conversation list** with last message preview
- 💾 **Token persistence** scoped per `CHAT_USER`
- 🔄 **Persistent menus** — always returns to the menu after each action

---

## 🧪 Development

### Code Style

- **PEP 8** style guide
- **Type hints** throughout
- **Separation of concerns** — API layer does not print; menu layer does not contain logic

### Running in Development Mode

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 --log-level debug
```

---

## 🧪 Testing

### Manual Testing

```bash
python -m app.main
# Visit http://127.0.0.1:8000/docs
```

### Testing with cURL

```bash
# Sign up
curl -X POST "http://127.0.0.1:8000/users/signup" \
  -H "Content-Type: application/json" \
  -d '{"userName":"testuser","userEmail":"test@example.com","password":"testpass123","firstName":"Test","lastName":"User"}'

# Login
curl -X POST "http://127.0.0.1:8000/users/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=testuser&password=testpass123"

# Get conversations
curl -X GET "http://127.0.0.1:8000/conversations/get-conversations" \
  -H "Authorization: Bearer <your_token_here>"
```

### WebSocket Testing

- **[websocat](https://github.com/vi/websocat)** - CLI WebSocket client
- **[Postman](https://www.postman.com/)** - API testing with WebSocket support
- **Browser DevTools** - JavaScript WebSocket testing

---

## 🚀 Deployment

### Production Checklist

- [ ] Set strong `SECRET_KEY` in environment
- [ ] Configure production database
- [ ] Set up HTTPS/WSS with a reverse proxy
- [ ] Configure CORS for your frontend domain
- [ ] Configure logging
- [ ] Set up database backups
- [ ] Implement rate limiting

### Nginx Reverse Proxy

```nginx
upstream messaging_app {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://messaging_app;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /ws {
        proxy_pass http://messaging_app;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
    }
}
```

---

## 🗺️ Roadmap

### Planned Features

- [ ] **Group Messaging** - Multi-user conversations
- [ ] **File Sharing** - Send images and documents
- [ ] **Typing Indicators** - Real-time typing status
- [ ] **Read Receipts** - Per-message read confirmation
- [ ] **User Presence** - Online/offline/away status
- [ ] **Message Search** - Full-text search
- [ ] **Web Frontend** - Browser-based client
- [ ] **Message Encryption** - End-to-end encryption

### Improvements

- [ ] Unit and integration tests
- [ ] API rate limiting
- [ ] Redis for caching and session management
- [ ] CI/CD pipeline
- [ ] Comprehensive logging and monitoring

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

### Guidelines

- Follow PEP 8
- Add type hints to new functions
- Keep PRs focused and atomic
- Update documentation as needed

---

## 📄 License

This project is licensed under the **MIT License**.

```
MIT License

Copyright (c) 2026 whoisibk

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 📧 Contact

**Developer:** whoisibk

- GitHub: [@whoisibk](https://github.com/whoisibk)
- Project Link: [https://github.com/whoisibk/messaging-application](https://github.com/whoisibk/messaging-application)

---

<div align="center">

**⭐ If you found this project helpful, please consider giving it a star! ⭐**

Made with ❤️ by [whoisibk](https://github.com/whoisibk)

</div>
