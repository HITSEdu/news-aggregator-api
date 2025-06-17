from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.schemas.auth import Token
from app.schemas.user import UserAuth, User
from app.models.user import User as DBUser
from app.auth.auth import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    get_password_hash,
    create_access_token,
    verify_password,
)
from app.models.database import get_db
from datetime import timedelta

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=User)
async def register(user_data: UserAuth, db: AsyncSession = Depends(get_db)):
    # Проверка существования пользователя
    existing_user = await db.execute(
        select(DBUser).where(DBUser.email == user_data.email)
    )
    if existing_user.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )

    hashed_password = get_password_hash(user_data.password)
    db_user = DBUser(email=user_data.email, hashed_password=hashed_password)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    user_response = User(
        id=db_user.id,
        email=db_user.email,
        password=db_user.hashed_password,
        created_at=db_user.created_at,
    )
    return user_response


@router.post("/login", response_model=Token)
async def login(user_data: UserAuth, db: AsyncSession = Depends(get_db)):
    user = await db.execute(select(DBUser).where(DBUser.email == user_data.email))
    user = user.scalar_one_or_none()

    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
