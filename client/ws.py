import asyncio
import json

import websockets
from fastapi import WebSocket
from websockets.exceptions import ConnectionClosed

from client.api import get_user_by_username, get_user_by_id


"""Client-side program to handle websocket connections for real-time messaging."""

_sender_cache: dict[str, str] = {}


def _resolve_sender(sender_id: str) -> str:
    if sender_id not in _sender_cache:
        try:
            user = get_user_by_id(sender_id)
            _sender_cache[sender_id] = user["userName"]
        except Exception:
            _sender_cache[sender_id] = sender_id
    return _sender_cache[sender_id]


async def receive_messages(websocket: WebSocket):
    """Receive and print websocket events from the server."""
    while True:
        try:
            payload = await websocket.recv()
        except ConnectionClosed:
            print("\nConnection closed by server.")
            return

        try:
            event = json.loads(payload)
        except json.JSONDecodeError:
            print("\nReceived non-JSON websocket frame")
            continue

        event_name = event.get("event")
        data = event.get("data", {})

        if event_name == "message":
            sender = _resolve_sender(str(data.get("senderId", "")))
            ts = str(data.get("timestamp", ""))[:16].replace("T", " ")
            print(f"\n[{ts}] {sender}: {data.get('message')}")
        elif event_name == "ack":
            print(f"\n[sent] {data.get('deliveryStatus')}")
        elif event_name == "error":
            print(f"\n[error] {event.get('detail')}")
        else:
            print(f"\n[event] {event}")


async def chat_session(ws_url: str):
    """Run an interactive chat session with concurrent send/receive."""
    async with websockets.connect(ws_url) as websocket:
        print("Connected to realtime chat. Type /quit to exit.")

        receiver_task = asyncio.create_task(receive_messages(websocket))

        try:
            while True:
                recipient_username = await asyncio.to_thread(
                    input, "Recipient username: "
                )
                recipient_username = recipient_username.strip()
                if recipient_username.lower() == "/quit":
                    break

                message = await asyncio.to_thread(input, "Message: ")
                message = message.strip()

                if not message:
                    print("Message cannot be empty")
                    continue

                try:
                    recipient = get_user_by_username(recipient_username)
                    recipient_id = recipient["userId"]
                except Exception as error:
                    print(f"Could not resolve recipient: {error}")
                    continue

                await websocket.send(
                    json.dumps(
                        {
                            "recipientId": recipient_id,
                            "message": message,
                        }
                    )
                )

        finally:
            receiver_task.cancel()
            await asyncio.gather(receiver_task, return_exceptions=True)
    
