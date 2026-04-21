from fastapi import status, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from src.models import User
from src.database import get_async_session
from .tokens import JWTHandler


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token") 


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_async_session),
) -> User:
    payload = JWTHandler.decode(token)
    user = await session.get(User, payload.get("user_id"))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User with given id is not found"
        )
    return user





