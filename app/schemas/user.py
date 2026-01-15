from pydantic import BaseModel, EmailStr

# Base schema (field yang selalu ada)
class UserBase(BaseModel):
    email: EmailStr

# Schema buat Register (Input dari user)
class UserCreate(UserBase):
    password: str

# Schema buat Response (Output ke user)
class UserResponse(UserBase):
    id: int
    is_active: bool

    class Config:
        # Ini penting biar Pydantic bisa baca data dari SQLAlchemy
        from_attributes = True
    
class Token(BaseModel):
    access_token: str
    token_type: str