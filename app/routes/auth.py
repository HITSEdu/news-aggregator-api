from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.auth import (
    get_password_hash,
    create_access_token,
    verify_password, create_refresh_token,
)
from app.models.database import get_db
from app.models.user import User as DBUser
from app.schemas.auth import Token
from app.schemas.user import UserBase, UserAuth, UserWithTicker
from app.utils.captcha import verify_recaptcha
from app.utils.config import config
from app.utils.convertor import ticker_db_to_dto

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=Token)
async def register(user_data: UserAuth, db: AsyncSession = Depends(get_db)):
    if not await verify_recaptcha(user_data.captchaToken):
        raise HTTPException(status_code=400, detail="Invalid reCAPTCHA token")
    existing_user = await db.execute(
        select(DBUser).where(DBUser.email == user_data.email)
    )
    if existing_user.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )
    hashed_password = get_password_hash(user_data.password)
    db_user = DBUser(
        email=user_data.email,
        login=user_data.login,
        hashed_password=hashed_password,
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    access_token_expires = timedelta(minutes=config.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": db_user.email}, expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(
        data={"sub": db_user.email}, expires_delta=access_token_expires
    )
    return Token(
        token=access_token,
        refreshToken=refresh_token,
        user=UserWithTicker(
            email=db_user.email,
            login=db_user.login,
            tickers=ticker_db_to_dto(db_user.tickers),
        )
    )


@router.post("/login", response_model=Token)
async def login(user_data: UserBase, db: AsyncSession = Depends(get_db)):
    # if not await verify_recaptcha(user_data.captcha_token):
    #     raise HTTPException(status_code=400, detail="Invalid reCAPTCHA token")
    db_user = await db.execute(select(DBUser).where(DBUser.email == user_data.email))
    db_user = db_user.scalar_one_or_none()
    if not db_user or not verify_password(user_data.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=config.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": db_user.email}, expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(
        data={"sub": db_user.email}, expires_delta=access_token_expires
    )
    return Token(
        token=access_token,
        refreshToken=refresh_token,
        user=UserWithTicker(
            email=db_user.email,
            login=db_user.login,
            tickers=ticker_db_to_dto(db_user.tickers),
        )
    )
