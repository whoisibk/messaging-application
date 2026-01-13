from fastapi import APIRouter, WebSocket, Depends
import json

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
            # containing senderId, recipientId, message
            data = await websocket.receive_json()

            # parse json data
            data = json.loads(data)   

            
            # server forwards json message to the intended recipient
            await manager.send_personal_message(
                message_info=data
            )


    except WebSocketException:
        manager.disconnect(userId)
