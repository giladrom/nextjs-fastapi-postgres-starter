from fastapi import FastAPI, HTTPException, status, BackgroundTasks
from pydantic import BaseModel
from sqlalchemy import select, insert, or_
from seed import seed_user_if_needed
from sqlalchemy.ext.asyncio import AsyncSession
from db_engine import engine
from models import User, Message
from typing import Any
import datetime
from fastapi.middleware.cors import CORSMiddleware
import lorem
import html
import re

seed_user_if_needed()

app = FastAPI()

# Set up FastAPI CORS to allow CRUD HTTP calls
origins = [
    "http://localhost",
    "http://localhost:3000",
    
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserRead(BaseModel):
    id: int
    name: str

class MessageRead(BaseModel):
    id: int
    sender_id: int
    recipient_id: int
    timestamp: datetime.datetime
    message: str

class MessageWrite(BaseModel):
    sender_id: int
    message: str

# Generate a mock AI response. Server UID is hard-coded in this example.
async def generate_response(user_id: int):
 async with AsyncSession(engine) as session:
        async with session.begin():           
            # Add a new message to the DB
            
            session.add(Message(recipient_id=user_id, sender_id=2, message=lorem.sentence() ))
            session.commit()
            return f"ok"


@app.get("/users/me")
async def get_my_user():
    async with AsyncSession(engine) as session:
        async with session.begin():
            # Sample logic to simplify getting the current user. There's only one user.
            result = await session.execute(select(User))
            user = result.scalars().first()

            if user is None:
                raise HTTPException(status_code=404, detail="User not found")
            return UserRead(id=user.id, name=user.name)

# Get all messages for the specified user ID
@app.get("/messages/")
async def get_my_messages(user_id: int):
    async with AsyncSession(engine) as session:
        async with session.begin():
            # Get all messages our user has sent or received

            result = await session.execute(select(Message).where(
                or_(Message.sender_id == user_id, 
                    Message.recipient_id == user_id)).order_by(Message.timestamp))
            messages = result.scalars()

            return [MessageRead(id=message.id, sender_id=message.sender_id, 
                                recipient_id=message.recipient_id,
                                timestamp = message.timestamp,
                                message=message.message) for message in messages]

# Send a new message to the server. Server UID is hard-coded in this example.
@app.post("/messages/", status_code=status.HTTP_201_CREATED)
async def send_new_message(msg: MessageWrite, background_tasks: BackgroundTasks):
    async with AsyncSession(engine) as session:
        async with session.begin():           
            # Add a new message to the DB, check length and sanitize input
            if len(msg.message) > 512:
                raise HTTPException(status_code=500, detail="Message is too long")
            
            # Sanitize input string before writing to the DB (remove script tags and escape HTML)
            sanitized_message = re.sub(r'<script\b[^>]*>(.*?)</script>', '', msg.message, flags=re.IGNORECASE) 
            sanitized_message = html.escape(sanitized_message)
            
            session.add(Message(recipient_id=2, sender_id=msg.sender_id, message=sanitized_message))            
            session.commit()    
    
    # Generate mock AI response without blocking
    background_tasks.add_task(generate_response, msg.sender_id)

            