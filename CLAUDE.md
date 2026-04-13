# Session Context

FastAPI backend + Python CLI client (ChatCLI). PostgreSQL DB via SQLAlchemy + Alembic. WebSocket-based real-time messaging.

---

## Work Completed

### Bug fixes & infrastructure
- **alembic/env.py**: Escaped `%` as `%%` in DATABASE_URL before passing to `set_main_option` — fixes configparser interpolation error on passwords with URL-encoded characters (e.g. `%3F`).
- **Alembic merge**: Merged two diverged heads (`9f8c3e2d1a7b` and `a3c1f8e20d47`) into `e42a105954c8`.
- **app/routes/users.py**: Removed `-> User` return type annotations from route handlers — FastAPI was trying to validate the SQLAlchemy `User` model as a Pydantic response model, crashing on SQLAlchemy's `UUID` type.
- **app/routes/messages.py**: Replaced wildcard service imports with explicit named imports — wildcards were overwriting `from uuid import UUID as Uuid` with SQLAlchemy's UUID, breaking path parameter validation.

### Item 1 — Conversation schema/model mismatch (DONE)
- Added `dateCreated` and `lastMessage` to `Conversation` DB model and Pydantic schema.
- Created migration and wired `update_last_message()` to be called after every new message is saved in `message_ops.create_message()`.

### Item 3 — delete_conversation bug (DONE)
- **app/services/conversation_ops.py**: Fixed `delete_conversation()` — changed `.first()` to `.delete()` so it returns a row count instead of an ORM object.
- **app/routes/conversations.py**: Wired the stubbed delete route. Route function named `delete__conversation` (double underscore) to avoid name collision with the imported service function `delete_conversation`.

### Item 4 — Offline message delivery (DONE)
- **app/models.py**: Added `delivered = Column(Boolean, nullable=False, server_default="false")` to `Message`.
- **Migration `c3d4e5f6a7b8`**: Adds `delivered` column to `message` table.
- **app/services/message_ops.py**: Added `get_undelivered_messages(userId)` and `mark_messages_delivered(messageIds)`.
- **app/websocket_manager.py**: `connect()` now calls `_deliver_offline_messages()` on reconnect, which pushes all undelivered messages then marks them delivered. `process_incoming_message()` now calls `mark_messages_delivered` immediately when recipient is online.

### Item 5 — get_messages broken URL (DONE)
- **client/api.py**: Fixed `get_messages()` to accept `conversationId: str` and hit `/messages/{conversationId}`. Added `raise_for_status()`.

### Column rename: timeStamp → timestamp (DONE)
- **app/models.py**: Renamed `Message.timeStamp` to `Message.timestamp`.
- **Migration `d4e5f6a7b8c9`**: Renames column `timeStamp` → `timestamp` in `message` table.
- Updated all references in `message_ops.py`, `routes/messages.py`, and `websocket_manager.py`.

### Item 2 — Wire client menu options 3 & 4 in client/main.py (DONE)
- Added `get_messages` and `conversations` to imports from `client.api`.
- **Case 4 (View conversations)**: Calls `conversations()`, prints each with index, conversationId, and lastMessage.
- **Case 3 (View messages)**: Shows conversations list, prompts user to pick one by index, calls `get_messages(conversationId)`, prints each message with sender and timestamp.

---

## Remaining Work

_Nothing tracked yet. Add new items here as they come up._

---

## Recent Commits (on develop branch)
- `8481ab7` — Fix FastAPIError caused by SQLAlchemy UUID types leaking into Pydantic fields
- `2f8585f` — Rename Message.timeStamp to timestamp and add migration
- `400d750` — Fix delete_conversation bug, add offline message delivery, fix get_messages URL
