from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import User
from app.core.password_utils import get_password_hash
from app.schemas.user import UserCreate, UserUpdate

async def get_user_by_email(db: AsyncSession, email: str) -> User:
    result = await db.execute(select(User).where(User.email == email))
    return result.scalars().first()

async def get_user_by_username(db: AsyncSession, username: str) -> User:
    result = await db.execute(select(User).where(User.username == username))
    return result.scalars().first()

async def get_user_by_id(db: AsyncSession, user_id: int) -> User:
    return await db.get(User, user_id)

async def create_user(db: AsyncSession, user_data: UserCreate) -> User:
    hashed_password = get_password_hash(user_data.password)
    db_user = User(
        email=user_data.email,
        username=user_data.email,  # Генерация username
        hashed_password=hashed_password
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def update_user(db: AsyncSession, user_id: int, user_data: UserUpdate) -> User:
    user = await get_user_by_id(db, user_id)
    if not user:
        return None

    if user_data.email:
        user.email = user_data.email
    if user_data.password:
        user.hashed_password = get_password_hash(user_data.password)

    await db.commit()
    await db.refresh(user)
    return user

async def delete_user(db: AsyncSession, user_id: int) -> bool:
    user = await get_user_by_id(db, user_id)
    if not user:
        return False

    await db.delete(user)
    await db.commit()
    return True