from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.db.dependencies import get_user_service, get_current_user
from app.models import User
from app.schemas.auth import UserCreate, TokenResponse, UserLogin
from app.schemas.user import UserResponse
from app.services.user_service import UserService

router = APIRouter()

@router.post("/register", response_model=UserResponse)
async def register(
        user_data: UserCreate,
        service: UserService = Depends(get_user_service)
):
    return await service.create_user(user_data)

@router.post("/login", response_model=TokenResponse)
async def login(
        form_data:OAuth2PasswordRequestForm = Depends(),
        service: UserService = Depends(get_user_service)
):
    token = await service.authenticate(
        UserLogin(
            email=form_data.username,
            password=form_data.password
        )
    )
    return TokenResponse(
        access_token=token,
        token_type="bearer"
    )

@router.get("/me", response_model=UserResponse)
async def me(
        current_user: User = Depends(get_current_user)
):
    return current_user

