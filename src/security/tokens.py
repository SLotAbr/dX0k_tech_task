import jwt
from src.config import config
from datetime import datetime, timedelta
from fastapi import status, HTTPException


class JWTHandler:
    @staticmethod
    def encode(payload: dict) -> str:
        expire = datetime.utcnow() + timedelta(
            minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        payload.update({"exp": expire})
        return jwt.encode(
            payload, config.SECRET_KEY, algorithm=config.ALGORITHM
        )
    
    @staticmethod
    def decode(token: str) -> dict:
        try:
            return jwt.decode(
                token, config.SECRET_KEY, algorithms=[config.ALGORITHM]
            )
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )


















