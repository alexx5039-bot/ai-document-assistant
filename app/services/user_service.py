from app.core.security import hash_password, verify_password, create_access_token
from app.models import User, Document
from app.models.enum import DocumentStatus
from app.repositories.user_repository import UserRepository
from app.schemas.auth import UserCreate, UserLogin, TokenResponse
from fastapi import status, HTTPException


class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def create_user(self, user_data: UserCreate) -> User:

        existing = await self.repo.get_by_email(email=user_data.email)

        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this email already exists",
            )
        password_hash = hash_password(user_data.password)

        return await self.repo.create(
            email=user_data.email,
            password_hash=password_hash
        )

    async def authenticate(self, user_data: UserLogin) -> str:
        user = await self.repo.get_by_email(user_data.email)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        if not verify_password(user_data.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User is inactive",
            )

        return create_access_token(user.id)



    async def get_user(self, user_id: int) -> User | None:
        user = await self.repo.get_by_id(user_id=user_id)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return user

    async def get_user_by_email(self, email: str) -> User | None:
        user = await self.repo.get_by_email(email=email)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return user

