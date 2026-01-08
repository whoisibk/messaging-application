from fastapi import FastAPI, HTTPException
from uvicorn import run
from typing import Optional
from enum import Enum
from pydantic import BaseModel, Field

from app.routes.users import router as users_route
from app.routes.messages import router as messages_route
from app.routes.conversations import router as conversations_route

from app.websocket_endpoint import wb_route as websocket_route


app = FastAPI()


app.include_router(users_route, prefix="/users")
app.include_router(messages_route, prefix="/messages")
app.include_router(conversations_route, prefix="/conversations")

app.include_router(websocket_route, prefix="/ws")


@app.get("/")
def test():
    return {"message": "Hello World!"}


if __name__ == "__main__":
    run("app.main:app", host="127.0.0.1", port=8000, reload=True)
