from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash

async def get_user_by_email(db: AsyncSession, email: str):
    # Query cari user berdasarkan email
    result = await db.execute(select(User).filter(User.email == email))
    return result.scalars().first()

async def create_user(db: AsyncSession, user: UserCreate):
    # 1. Hash password user
    hashed_password = get_password_hash(user.password)
    
    # 2. Bikin object User baru
    db_user = User(
        email=user.email,
        hashed_password=hashed_password
    )
    
    # 3. Add & Commit ke DB
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user) # Refresh biar dapet ID baru
    return db_user