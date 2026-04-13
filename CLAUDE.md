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
- Added `get_messages`, `conversations`, `get_user_by_id` to imports from `client.api`.
- Added `get_user_by_id(userId)` to `client/api.py` hitting `GET /users/profile/{userId}`.
- **Case 4 (View conversations)**: Resolves other user's username via `get_user_by_id`, prints `1. alice — last message`.
- **Case 3 (View messages)**: Same list, user picks one, messages printed as `[YYYY-MM-DD HH:MM] You: ...` or `[...] alice: ...`.

### Per-user token isolation (DONE)
- **client/token_storage.py**: Token file name scoped to `CHAT_USER` env var (`mytoken_{CHAT_USER}.json`).
- Run two CLI sessions on same machine: `CHAT_USER=alice python -m client.main` and `CHAT_USER=bob python -m client.main`.

---

## Remaining Work

_Nothing tracked yet. Add new items here as they come up._

---

## Recent Commits (on develop branch)
- `3056f23` — Wire menu cases 3 & 4, add per-user token isolation, add CLAUDE.md
- `8481ab7` — Fix FastAPIError caused by SQLAlchemy UUID types leaking into Pydantic fields
- `2f8585f` — Rename Message.timeStamp to timestamp and add migration
- `400d750` — Fix delete_conversation bug, add offline message delivery, fix get_messages URL
