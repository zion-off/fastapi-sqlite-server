from pydantic import BaseModel


class UserSchema(BaseModel):
    id: int
    name: str
    username: str
    password: str


class RegisterRequest(BaseModel):
    name: str
    username: str
    password: str

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    id: int
    name: str
    username: str

    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    user_id: int
    token: str

    class Config:
        from_attributes = True


class MessageSchema(BaseModel):
    id: int
    message: str
    created_at: str
    user_id: int


class MessageRequest(BaseModel):
    message: str
    user_id: int
    token: str

    class Config:
        from_attributes = True


class UpdateMessageRequest(BaseModel):
    user_id: int
    message_id: int
    message: str
    token: str

    class Config:
        from_attributes = True


class DeleteMessageRequest(BaseModel):
    user_id: int
    message_id: int
    token: str

    class Config:
        from_attributes = True
