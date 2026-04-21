from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_async_session
from src import schemas
from src.models import User
from src.security import PasswordHandler, JWTHandler, get_current_user


UsersRouter = APIRouter()


@UsersRouter.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(
    register_user: schemas.RegisterUser, 
    session: AsyncSession = Depends(get_async_session),
) -> schemas.ReadUser:
    """Регистрация нового пользователя с использованием уникальных пользовательского имени и почты.
    """
    query = select(User).filter(User.username == register_user.username)
    query = await session.scalars(query)
    user = query.one_or_none()
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="User with this username already exists"
        )
    query = select(User).filter(User.email == register_user.email)
    query = await session.scalars(query)
    user = query.one_or_none()
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="User with this email already exists"
        )
    user = User(
        username = register_user.username, 
        email = register_user.email, 
        hashed_password = PasswordHandler.hash_password(
            register_user.password
        )
    )
    session.add(user)
    await session.commit()
    return user


@UsersRouter.post("/token")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_async_session),
) -> schemas.Token:
    """Служебная конечная точка для получения JWT токена доступа из OAuth2 формы авторизации.
    """
    query = select(User).filter(User.username == form_data.username)
    query = await session.scalars(query)
    user = query.one_or_none()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Incorrect username or password"
        )
    if not PasswordHandler.verify_password(
        form_data.password, user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Incorrect username or password"
        )
    return schemas.Token(
        access_token = JWTHandler.encode(payload={"user_id":user.id}),
        token_type = "bearer"
    )


@UsersRouter.get("/me")
async def get_me(
    user: User = Depends(get_current_user)
) -> schemas.ReadUser:
    """ Предоставляет информацию об аккаунте авторизованного пользователя.
    """
    return user



















