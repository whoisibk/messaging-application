from fastapi import APIRouter, WebSocket, Depends

from app.routes.users import get_current_user, User
from app.websocket_manager import ConnectionManager
from websockets import WebSocketException

wb_route = APIRouter()
manager = ConnectionManager()


@wb_route.websocket("/chat")
async def websocket_endpoint(
    websocket: WebSocket, user: User = Depends(get_current_user)
):

    userId = user.userId
    manager.connect(userId, websocket)

    try:
        while True:

            # server receives message info from client in JSON format
            data = await websocket.receive_json()

            data = dict(data)  # parse to dict

            recipientId = data.get("recipientId")
            message = data.get("message")

            # send personal message to recipient
            await manager.send_personal_message(
                senderId=userId,
                recipientId=recipientId,
                message=message,
            )

    except WebSocketException:
        manager.disconnect(userId)
