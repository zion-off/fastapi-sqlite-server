from fastapi import FastAPI, Depends, HTTPException
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from typing import List
import datetime
from auth import generate_token
from models import Base, User, Message
from schemas import (
    UserSchema,
    UserResponse,
    LoginRequest,
    LoginResponse,
    MessageSchema,
    MessageRequest,
    HistoryRequest,
    UpdateMessageRequest,
    DeleteMessageRequest,
)


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Message Server",
)

token_dict = {}


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.post("/api/users", response_model=UserResponse, tags=["Users"])
async def register(request: UserSchema, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == request.username).first()
    if user:
        raise HTTPException(status_code=400, detail="Username already exists")
    user = User(name=request.name, username=request.username, password=request.password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@app.post("/api/users/login", response_model=LoginResponse, tags=["Users"])
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = (
        db.query(User)
        .filter(User.username == request.username, User.password == request.password)
        .first()
    )
    if not user:
        raise HTTPException(status_code=400, detail="Wrong username or password")
    token = generate_token(data={"sub": user.username})
    token_dict[user.username] = token
    return {"username": user.username, "token": token}


@app.get("/api/users", response_model=List[UserResponse], tags=["Users"])
async def list_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users


@app.post("/api/messages", response_model=MessageSchema, tags=["Messages"])
async def send_message(request: MessageRequest, db: Session = Depends(get_db)):
    if not request.token or token_dict.get(request.user_id) != request.token:
        raise HTTPException(status_code=401, detail="Unauthorized")
    message = Message(
        message=request.message, user_id=request.user_id, created_at=datetime.now()
    )
    db.add(message)
    db.commit()
    db.refresh(message)
    return message


@app.get("/api/messages", response_model=List[MessageSchema], tags=["Messages"])
async def get_messages(request: HistoryRequest, db: Session = Depends(get_db)):
    if not request.token or token_dict.get(request.user_id) != request.token:
        raise HTTPException(status_code=401, detail="Unauthorized")
    skip = request.skip if request.skip is not None else 0
    limit = request.limit if request.limit is not None else 10
    messages = db.query(Message).offset(skip).limit(limit).all()
    return messages


@app.patch("/api/messages/{message_id}", response_model=MessageSchema, tags=["Messages"])
async def update_message(
    request: UpdateMessageRequest, message_id: int, db: Session = Depends(get_db)
):
    if not request.token or token_dict.get(request.user_id) != request.token:
        raise HTTPException(status_code=401, detail="Unauthorized")
    if not request.message_id:
        raise HTTPException(status_code=400, detail="Message ID is required")
    message = db.query(Message).filter(Message.id == message_id).first()
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    message.message = request.message
    db.commit()
    db.refresh(message)
    return message


@app.delete("/api/messages/{message_id}", response_model=MessageSchema, tags=["Messages"])
async def delete_message(
    request: DeleteMessageRequest, message_id: int, db: Session = Depends(get_db)
):
    if not request.token or token_dict.get(request.user_id) != request.token:
        raise HTTPException(status_code=401, detail="Unauthorized")
    if not request.message_id:
        raise HTTPException(status_code=400, detail="Message ID is required")
    message = db.query(Message).filter(Message.id == message_id).first()
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    db.delete(message)
    db.commit
    return message
