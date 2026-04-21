from fastapi import FastAPI, Depends
import contextlib

from src.config import config
from src.api import router

from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from src.middlewares import RateLimitMiddleware


def make_middleware() -> list[Middleware]:
    middleware = [
        Middleware(
            CORSMiddleware,
            # allow_origins=config.CORS_ORIGINS,
            allow_origins=["*"], # ["http://127.0.0.1:3001"]
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        ),
        # """
        Middleware(
            RateLimitMiddleware,
            throttle_rate=config.RATE_LIMIT_REQESTS,
            window_len=config.RATE_LIMIT_WINDOW_SECONDS
        ),
        # """
    ]
    return middleware


def create_app() -> FastAPI:
    app_ = FastAPI(
        # lifespan = lifespan, 
        middleware = make_middleware(),
    )
    app_.include_router(
        router,
    )
    return app_


app = create_app()









