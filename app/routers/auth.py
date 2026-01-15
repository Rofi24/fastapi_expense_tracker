from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.security import create_access_token, verify_password
from app.schemas.user import Token, UserCreate, UserResponse
from app.crud import crud_user

router = APIRouter()

# REGISTER
@router.post("/register", response_model=UserResponse)
async def register_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    # 1. Cek apakah email udah kepake?
    db_user = await crud_user.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # 2. Kalau aman, create user baru
    return await crud_user.create_user(db=db, user=user)

# LOGIN
@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: AsyncSession = Depends(get_db)
):
    # 1. Cari user di database by Email
    # Note: OAuth2 form nyimpen email di field 'username'
    user = await crud_user.get_user_by_email(db, email=form_data.username)
    
    # 2. Validasi: User ada? Password bener?
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 3. Kalau lolos, cetak token!
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}