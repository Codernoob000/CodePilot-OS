from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.models.user import User
from app.core.security import create_access_token
from app.schemas.user import  Token
from app.services.user import InvalidCredentialsError
from app.schemas.user import UserCreate, UserRead
from app.services.user import (
    EmailAlreadyExistsError,
    UsernameAlreadyExistsError,
    UserService,
)
from app.api.dependencies import (
    get_current_user,
    get_user_service,
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

@router.post(
    "/register",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
)
async def register(
    user_data: UserCreate,
    service: UserService = Depends(get_user_service),
):
    try:
        return await service.register_user(user_data)

    except EmailAlreadyExistsError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc

    except UsernameAlreadyExistsError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc

@router.post(
    "/login",
    response_model=Token,
    status_code=status.HTTP_200_OK,
)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    service: UserService = Depends(get_user_service),
):
    try:
        user = await service.authenticate_user(
            email=form_data.username,
            password=form_data.password,
        )

        access_token = create_access_token(str(user.id))

        return Token(
            access_token=access_token,
            token_type="bearer",
        )

    except InvalidCredentialsError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
        ) from exc

@router.get(
    "/me",
    response_model=UserRead,
)
async def get_me(
    current_user: User = Depends(get_current_user),
):
    return current_user