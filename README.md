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

Whether you're learning about WebSockets, building a chat application, or looking for a reference implementation of FastAPI best practices, this project serves as a comprehensive example. 

---

## ✨ Features

### Core Functionality

- ✅ **User Authentication & Authorization**
  - Secure user registration with password hashing
  - JWT token-based authentication
  - OAuth2 password flow implementation
  - Token refresh and validation

- ✅ **Real-Time Messaging**
  - WebSocket connections for instant message delivery
  - Bi-directional communication
  - Online/offline user detection
  - Message persistence for offline users

- ✅ **Conversation Management**
  - One-on-one conversations
  - Automatic conversation creation
  - Message history retrieval
  - Conversation listing per user

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
  - Separation of concerns
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
┌─────────────┐         ┌────────────���─────────────────────────┐
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
                        │  │  • User Operations          │  │
                        │  │  • Message Operations       │  │
                        │  │  • Conversation Operations  │  │
                        │  └──────────────┬───────────────┘  │
                        │                 │                  │
                        │  ┌──────────────▼───────────────┐  │
                        │  │     Database (PostgreSQL)    │  │
                        │  │                              │  │
                        │  │  • Users Table              │  │
                        │  │  • Messages Table           │  │
                        │  │  • Conversations Table      │  │
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
- **requests** - HTTP library for API calls

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
│   ├── 📄 main.py                   # Client entry point
│   ├── 📄 auth.py                   # Authentication handlers
│   ├── 📄 api.py                    # REST API client
│   ├── 📄 ws. py                     # WebSocket client
│   └── 📄 token_storage.py          # Token persistence
│
├── 📂 alembic/                      # Database migrations
│   ├── 📄 env.py
│   ├── 📄 script.py. mako
│   └── 📂 versions/
│
├── 📄 alembic.ini                   # Alembic configuration
├── 📄 guide.txt                     # Development guide
├── 📄 . gitignore
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
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux: 
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
# Install required packages
pip install fastapi uvicorn sqlalchemy psycopg2-binary alembic pydantic python-jose[cryptography] passlib[bcrypt] websockets python-multipart requests

# Or if you have requirements.txt:
pip install -r requirements.txt
```

### Step 4: Database Setup

```bash
# Create PostgreSQL database
createdb messaging_app_db

# Or using psql:
psql -U postgres
CREATE DATABASE messaging_app_db;
\q
```

### Step 5: Configure Database Connection

Update the database connection string in `app/database.py`:

```python
DATABASE_URL = "postgresql://username:password@localhost/messaging_app_db"
```

### Step 6: Run Database Migrations

```bash
# Initialize Alembic (if not already done)
alembic init alembic

# Create initial migration
alembic revision --autogenerate -m "Initial migration"

# Apply migrations
alembic upgrade head
```

---

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# Database Configuration
DATABASE_URL=postgresql://username:password@localhost/messaging_app_db

# JWT Configuration
SECRET_KEY=your-secret-key-here-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Server Configuration
HOST=127.0.0.1
PORT=8000
DEBUG=True

# CORS Settings (for web clients)
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8080
```

### Generate Secret Key

```python
# Generate a secure secret key
import secrets
print(secrets.token_urlsafe(32))
```

---

## 💻 Usage

### Starting the Server

```bash
# Development mode with auto-reload
python -m app.main

# Or using uvicorn directly
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

# Production mode
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

The server will start at `http://127.0.0.1:8000`

### Using the CLI Client

```bash
# Start the CLI client
python -m client.main
```

**CLI Menu Options:**

1. **Login** - Authenticate with existing credentials
2. **Sign Up** - Create a new user account
3. **View Profile** - Display current user information
4. **Send Message** - Send a message to another user
5. **View Messages** - Retrieve message history
6. **View Conversations** - List all conversations
7. **Logout** - End current session

### API Documentation

Once the server is running, visit: 

- **Swagger UI**:  http://127.0.0.1:8000/docs
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
    "messageText": "Hello, how are you?"
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
    "user2_Id": "770e8400-e29b-41d4-a716-446655440000"
  }
]
```

#### Get Conversation by ID
```http
GET /conversations/{conversationId}
```

---

## 🔌 WebSocket Protocol

### Connection

```javascript
// WebSocket endpoint
ws://127.0.0.1:8000/ws

// Connection with authentication
const ws = new WebSocket('ws://127.0.0.1:8000/ws', {
  headers: {
    'Authorization': 'Bearer <access_token>'
  }
});
```

### Message Format

**Sending a Message:**
```json
{
  "senderId": "550e8400-e29b-41d4-a716-446655440000",
  "recipientId": "770e8400-e29b-41d4-a716-446655440000",
  "message": "Hello, this is a test message"
}
```

**Receiving a Message:**
```json
{
  "status": 200,
  "conversationId": "880e8400-e29b-41d4-a716-446655440000",
  "timestamp": "2026-01-22T10:30:00",
  "message": "Hello, this is a test message",
  "sent by": "550e8400-e29b-41d4-a716-446655440000"
}
```

### Connection Manager

The `ConnectionManager` class handles:
- ✅ WebSocket connection lifecycle
- ✅ User online/offline status
- ✅ Message routing to connected users
- ✅ Automatic message persistence for offline users
- ✅ Broadcasting capabilities

---

## 🗄️ Database Schema

### Users Table

| Column | Type | Constraints |
|--------|------|-------------|
| userId | UUID | PRIMARY KEY, UNIQUE |
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
| senderId | UUID | FOREIGN KEY → user. userId |
| recipientId | UUID | FOREIGN KEY → user. userId |
| conversationId | UUID | FOREIGN KEY → conversation. conversationId |
| messageText | VARCHAR(250) | NOT NULL |
| timeStamp | TIMESTAMP | NOT NULL |

### Conversations Table

| Column | Type | Constraints |
|--------|------|-------------|
| conversationId | UUID | PRIMARY KEY, UNIQUE |
| user1_Id | UUID | FOREIGN KEY → user. userId |
| user2_Id | UUID | FOREIGN KEY → user.userId |

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
└──────────────────┘         │ conversationId   │
                             │ messageText      │
                             │ timeStamp        │
                             └──────────────────┘
```

---

## 🖥️ Client Application

### Features

The CLI client (`client/`) provides: 

- 🔐 **User authentication** (login/signup)
- 💬 **Real-time messaging** via WebSocket
- 📋 **Profile viewing**
- 💾 **Token persistence** across sessions
- 🎨 **User-friendly CLI interface**

### Client Architecture

```python
client/
├── main.py              # Entry point & menu system
├── auth.py              # Login/signup handlers
├── api.py               # REST API client
├── ws.py                # WebSocket client
└── token_storage.py     # Token persistence
```

### Example Usage

```python
# client/main.py

from client.auth import SignUp, Login
from client.api import send_message
from client.ws import WebSocketClient

# User flow
if not logged_in:
    Login()  # or SignUp()

# Send message via API
send_message(recipient_id, message_text)

# Real-time WebSocket communication
ws_client = WebSocketClient(token)
await ws_client.connect()
await ws_client.send_message(message_data)
```

---

## 🧪 Development

### Code Style

This project follows:
- **PEP 8** style guide
- **Type hints** throughout
- **Docstrings** for all functions/classes
- **Clean architecture** principles

### Project Guidelines

1. **Separation of Concerns**
   - Routes handle HTTP/WebSocket
   - Services contain business logic
   - Models define data structures
   - Utils provide helper functions

2. **Type Safety**
   - Use Pydantic models for validation
   - Add type hints to all functions
   - Leverage Python 3.9+ features

3. **Error Handling**
   - Use appropriate HTTP status codes
   - Provide descriptive error messages
   - Handle database exceptions gracefully

### Running in Development Mode

```bash
# With auto-reload
uvicorn app.main:app --reload

# With specific configuration
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 --log-level debug
```

---

## 🧪 Testing

### Manual Testing

Use the interactive API documentation:

```bash
# Start server
python -m app.main

# Visit http://127.0.0.1:8000/docs
# Use the "Try it out" feature in Swagger UI
```

### Testing with cURL

```bash
# Sign up
curl -X POST "http://127.0.0.1:8000/users/signup" \
  -H "Content-Type: application/json" \
  -d '{
    "userName": "testuser",
    "userEmail":  "test@example.com",
    "password": "testpass123",
    "firstName": "Test",
    "lastName": "User"
  }'

# Login
curl -X POST "http://127.0.0.1:8000/users/login" \
  -H "Content-Type:  application/x-www-form-urlencoded" \
  -d "username=testuser&password=testpass123"

# Get conversations (with token)
curl -X GET "http://127.0.0.1:8000/conversations/get-conversations" \
  -H "Authorization: Bearer <your_token_here>"
```

### WebSocket Testing

Use tools like: 
- **[websocat](https://github.com/vi/websocat)** - CLI WebSocket client
- **[Postman](https://www.postman.com/)** - API testing tool
- **Browser DevTools** - JavaScript WebSocket testing

---

## 🚀 Deployment

### Production Checklist

- [ ] Set strong `SECRET_KEY` in environment
- [ ] Configure production database
- [ ] Set `DEBUG=False`
- [ ] Configure CORS for your frontend domain
- [ ] Set up HTTPS/WSS with reverse proxy
- [ ] Configure logging
- [ ] Set up database backups
- [ ] Implement rate limiting
- [ ] Add monitoring and alerting

### Using a Process Manager (PM2 or Systemd)

#### With PM2

```bash
# Install PM2
npm install -g pm2

# Start the application
pm2 start "uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4" --name messaging-app

# Save PM2 configuration
pm2 save

# Set up PM2 to start on boot
pm2 startup
```

#### With Systemd (Linux)

Create a service file at `/etc/systemd/system/messaging-app.service`:

```ini
[Unit]
Description=Messaging Application
After=network. target

[Service]
Type=notify
User=www-data
WorkingDirectory=/path/to/messaging-application
Environment="DATABASE_URL=postgresql://user:pass@localhost/messaging_db"
Environment="SECRET_KEY=your-secret-key"
ExecStart=/path/to/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
Restart=always

[Install]
WantedBy=multi-user.target
```

Then: 
```bash
sudo systemctl daemon-reload
sudo systemctl start messaging-app
sudo systemctl enable messaging-app
sudo systemctl status messaging-app
```

### Nginx Reverse Proxy

```nginx
# /etc/nginx/sites-available/messaging-app

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

    # WebSocket support
    location /ws {
        proxy_pass http://messaging_app;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

Enable the site:
```bash
sudo ln -s /etc/nginx/sites-available/messaging-app /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### SSL/TLS with Let's Encrypt

```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx

# Get SSL certificate
sudo certbot --nginx -d yourdomain.com

# Auto-renewal is set up automatically
```

### Cloud Platform Deployment

#### Heroku

```bash
# Install Heroku CLI and login
heroku login

# Create app
heroku create your-app-name

# Add PostgreSQL
heroku addons:create heroku-postgresql:hobby-dev

# Set environment variables
heroku config:set SECRET_KEY=your-secret-key

# Create Procfile
echo "web: uvicorn app.main:app --host 0.0.0.0 --port \$PORT" > Procfile

# Deploy
git push heroku main
```

#### Railway

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Initialize project
railway init

# Add PostgreSQL
railway add postgresql

# Deploy
railway up
```

#### DigitalOcean App Platform

1. Connect your GitHub repository
2. Select Python as your app type
3. Set build command:  `pip install -r requirements.txt`
4. Set run command: `uvicorn app.main:app --host 0.0.0.0 --port 8080`
5. Add PostgreSQL database
6. Configure environment variables
7. Deploy! 

---

## 🗺️ Roadmap

### Planned Features

- [ ] **Group Messaging** - Multi-user conversations
- [ ] **File Sharing** - Send images, documents, etc.
- [ ] **Message Reactions** - Emoji reactions to messages
- [ ] **Typing Indicators** - Real-time typing status
- [ ] **Read Receipts** - Message delivery confirmation
- [ ] **User Presence** - Online/offline/away status
- [ ] **Message Search** - Full-text search capability
- [ ] **Push Notifications** - Mobile/web notifications
- [ ] **Message Encryption** - End-to-end encryption
- [ ] **Web Frontend** - React/Vue. js web client
- [ ] **Mobile Apps** - iOS and Android clients
- [ ] **Admin Dashboard** - User and system management

### Improvements

- [ ] Unit and integration tests
- [ ] API rate limiting
- [ ] Redis for caching and session management
- [ ] Message queue for async processing
- [ ] Horizontal scaling support
- [ ] Comprehensive logging
- [ ] Performance monitoring
- [ ] CI/CD pipeline

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

### How to Contribute

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Make your changes**
4. **Commit your changes**
   ```bash
   git commit -m 'Add some amazing feature'
   ```
5. **Push to the branch**
   ```bash
   git push origin feature/amazing-feature
   ```
6. **Open a Pull Request**

### Contribution Guidelines

- Follow PEP 8 style guide
- Add type hints to new functions
- Write docstrings for new modules/classes/functions
- Update documentation as needed
- Test your changes thoroughly
- Keep PRs focused and atomic

### Areas for Contribution

- 🐛 Bug fixes
- ✨ New features
- 📝 Documentation improvements
- 🧪 Test coverage
- ♿ Accessibility improvements
- 🌐 Internationalization

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

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

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - Amazing web framework
- [SQLAlchemy](https://www.sqlalchemy.org/) - Powerful ORM
- [Pydantic](https://pydantic-docs.helpmanual.io/) - Data validation library
- [PostgreSQL](https://www.postgresql.org/) - Robust database system

---

<div align="center">

**⭐ If you found this project helpful, please consider giving it a star!  ⭐**

Made with ❤️ by [whoisibk](https://github.com/whoisibk)

</div>
