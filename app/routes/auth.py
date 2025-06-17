from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.auth import (
    get_password_hash,
    create_access_token,
    verify_password,
)
from app.models.database import get_db
from app.models.user import User as DBUser
from app.schemas.auth import Token
from app.schemas.user import UserBase, UserAuth, UserResponse
from app.utils.config import config
from app.utils.captcha import verify_recaptcha

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserResponse)
async def register(user_data: UserAuth, db: AsyncSession = Depends(get_db)):
    # if not await verify_recaptcha(user_data.captcha_token):
    #     raise HTTPException(status_code=400, detail="Invalid reCAPTCHA token")
    existing_user = await db.execute(
        select(DBUser).where(DBUser.email == user_data.email)
    )
    if existing_user.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )
    hashed_password = get_password_hash(user_data.password)
    db_user = DBUser(
        email=user_data.email, login=user_data.login, hashed_password=hashed_password
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    user_response = UserResponse(
        id=db_user.id,
        email=db_user.email,
        login=db_user.login,
        password=db_user.hashed_password,
        favorite_tickers="",
        created_at=db_user.created_at,
    )
    return user_response


@router.post("/login", response_model=Token)
async def login(user_data: UserBase, db: AsyncSession = Depends(get_db)):
    # if not await verify_recaptcha(user_data.captcha_token):
    #     raise HTTPException(status_code=400, detail="Invalid reCAPTCHA token")
    user = await db.execute(select(DBUser).where(DBUser.email == user_data.email))
    user = user.scalar_one_or_none()
    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=config.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
