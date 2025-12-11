from fastapi import FastAPI, HTTPException
from typing import Optional
from enum import Enum
from pydantic import BaseModel, Field
from routes.users import router as users_route
from routes.messages import router as messages_route
from routes.conversations import router as conversations_route
import database


app = FastAPI()

app.include_router(users_route, prefix="/users")
app.include_router(messages_route, prefix="/messages")
app.include_router(conversations_route, prefix="/conversations")


@app.get("/")
def test():
    return {"message": "Hello World!"}
