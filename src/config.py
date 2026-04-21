from pydantic.v1 import BaseSettings


class Config(BaseSettings):
    DATABASE_URL: str
    TEST_DATABASE_URL: str
    
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 5
    
    RATE_LIMIT_REQESTS: int = 60
    RATE_LIMIT_WINDOW_SECONDS: int = 60
    
    REDIS_URL: str
    REDIS_TIME_TO_LIVE_SECONDS: int = 60 * 5
    
    CELERY_BROKER_URL: str
    
    PAGINATION_LIMIT: int = 200
    
    class Config:
        env_file = ".env.example"


config: Config = Config()

