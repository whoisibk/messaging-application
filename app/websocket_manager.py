from fastapi import WebSocket
from uuid import UUID as Uuid

from app.routes.messages import save_message
from app.services.message_ops import get_undelivered_messages, mark_messages_delivered


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
        await self._deliver_offline_messages(userId, websocket)

    async def _deliver_offline_messages(self, userId: Uuid, websocket: WebSocket):
        """Push any undelivered messages to a user who just connected."""
        missed = get_undelivered_messages(userId)
        if not missed:
            return
        for msg in missed:
            await websocket.send_json({
                "event": "message",
                "data": {
                    "messageId": str(msg.messageId),
                    "conversationId": str(msg.conversationId),
                    "senderId": str(msg.senderId),
                    "recipientId": str(msg.recipientId),
                    "message": msg.messageText,
                    "timestamp": msg.timeStamp.isoformat(),
                    "deliveryStatus": "delivered",
                },
            })
        mark_messages_delivered([msg.messageId for msg in missed])

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

    async def process_incoming_message(self, senderId: Uuid, message_info: dict) -> dict:
        """
        Send a text message to a specific connected user.
        Args:
            senderId (Uuid): The unique identifier of the sender user.
            recipientId (Uuid): The unique identifier of the recipient user.
            message (str): The text message to send.
        Returns:
            Dict
        Raises:
            ValueError: If the recipient user with the specified ID is not currently connected.

        """

        recipientId_raw = message_info.get("recipientId")
        message = message_info.get("message")

        if recipientId_raw is None:
            raise ValueError("Missing required field: recipientId")

        if not isinstance(message, str) or not message.strip():
            raise ValueError("Message must be a non-empty string")

        try:
            recipientId = Uuid(str(recipientId_raw))
        except ValueError as error:
            raise ValueError("recipientId must be a valid UUID") from error

        message_record = save_message(
            senderId=senderId,
            recipientId=recipientId,
            messageText=message.strip(),
        )

        outbound_message = {
            "messageId": message_record["messageId"],
            "conversationId": str(message_record["conversationId"]),
            "senderId": str(message_record["senderId"]),
            "recipientId": str(message_record["recipientId"]),
            "message": message_record["message"],
            "timestamp": message_record["timestamp"].isoformat(),
        }

        deliveryStatus = "stored_offline"
        if self.is_connected(recipientId):
            await self.active_connections[recipientId].send_json(
                {
                    "event": "message",
                    "data": {
                        **outbound_message,
                        "deliveryStatus": "delivered",
                    },
                }
            )
            mark_messages_delivered([Uuid(outbound_message["messageId"])])
            deliveryStatus = "delivered"

        return {
            **outbound_message,
            "deliveryStatus": deliveryStatus,
        }

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
            await self.active_connections[connection].send_text(message)

    def is_connected(self, userId: Uuid) -> bool:
        """
        Check whether a user is currently connected.
        Args:
            userId (Uuid): The unique identifier of the user to check.
        Returns:
            bool: True if the user is connected, False otherwise.
        """
        return userId in self.active_connections
