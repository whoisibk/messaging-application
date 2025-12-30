from fastapi import WebSocket
from uuid import UUID as Uuid


class ConnectionManager:
    """Manages WebSocket connections for real-time communication."""

    def __init__(self):
        """Initialize the ConnectionManager with an empty dictionary of active connections."""
        self.active_connections: dict[Uuid, WebSocket] = {}

    async def connect(self, userId: Uuid, websocket: WebSocket):
        """
         Accept a WebSocket connection and store it associated with a user ID.
        Args:
            userId (Uuid): The unique identifier of the user connecting.
            websocket (WebSocket): The WebSocket connection object to accept and store.
        Returns:
            None
        Raises:
            None
        """
        await websocket.accept()
        self.active_connections[userId] = websocket

    def disconnect(self, userId: Uuid):
        """
        Remove a user's WebSocket connection from active connections.
        Args:
            userId (Uuid): The unique identifier of the user to disconnect.
        Returns:
            None
        Raises:
            ValueError: If the user with the specified ID is not currently connected.
        """
        if userId in self.active_connections:
            self.active_connections.pop(userId)
        else:
            raise ValueError(f"User with ID {userId} not connected")

    async def send_personal_message(self, recipientId: Uuid, message: str):
        """
        Send a text message to a specific connected user.
        Args:
            recipientId (Uuid): The unique identifier of the recipient user.
            message (str): The text message to send.
        Returns:
            None
        Raises:
            ValueError: If the recipient user with the specified ID is not currently connected.

        """
        if recipientId in self.active_connections:
            await self.active_connections[recipientId].send_text(message)
        else:
            raise ValueError(f"User with ID {recipientId} not connected.")

    async def broadcast(self, message: str):
        """
        Send a text message to all currently connected users.
        Args:
            message (str): The text message to broadcast to all connections.
        Returns:
            None
        Raises:
            None
        """
        for connection in self.active_connections:
            self.active_connections[connection].send_text(message)

    def is_connected(self, userId: Uuid) -> bool:
        """
        Check whether a user is currently connected.
        Args:
            userId (Uuid): The unique identifier of the user to check.
        Returns:
            bool: True if the user is connected, False otherwise.
        """
        return userId in self.active_connections
