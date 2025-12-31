from fastapi import APIRouter, WebSocket, Depends

from routes.users import get_current_user, User
from websocket_manager import ConnectionManager
from websockets import WebSocketException

wb_route = APIRouter()
manager = ConnectionManager()

@wb_route.websocket("/")
async def websocket_endpoint(websocket: WebSocket, user: User = Depends(get_current_user)):

    userId = user.userId
    manager.connect(userId, websocket)

    try:
        while True:
            # server receives message info from client in JSON format
            data = await websocket.receive_text()
            # parse json to dict
            data =  dict(data)

            # server forwards the message to the intended recipient
            await manager.send_personal_message(recipientId=data["recipientId"], message=data["message"])
            
        
    except WebSocketException:
        manager.disconnect(userId)
