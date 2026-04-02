from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException

from app.routes.users import get_current_user_ws
from app.websocket_manager import ConnectionManager

wb_route = APIRouter()
manager = ConnectionManager()


@wb_route.websocket("/chat")
async def websocket_endpoint(websocket: WebSocket):
    try:
        user = get_current_user_ws(websocket)
    except HTTPException as error:
        await websocket.close(code=1008, reason=error.detail)
        return

    userId = user.userId
    await manager.connect(userId=userId, websocket=websocket)

    try:
        while True:
            data = await websocket.receive_json()

            if not isinstance(data, dict):
                await websocket.send_json(
                    {
                        "event": "error",
                        "detail": "Invalid payload. Expected a JSON object.",
                    }
                )
                continue

            try:
                ack = await manager.process_incoming_message(
                    senderId=userId,
                    message_info=data,
                )
                await websocket.send_json({"event": "ack", "data": ack})
            except ValueError as error:
                await websocket.send_json(
                    {
                        "event": "error",
                        "detail": str(error),
                    }
                )

    except WebSocketDisconnect:
        manager.disconnect(userId)
