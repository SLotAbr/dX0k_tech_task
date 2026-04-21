from collections import defaultdict
import time

from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse
from fastapi import Request, status


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, throttle_rate, window_len):
        super().__init__(app)
        self.throttle_rate = throttle_rate
        self.window_len = window_len
        self.counters = defaultdict(lambda: {
            "previous": 0,
            "current": 0,
            "current_start":0
        })
    
    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        now = time.time()
        window_start = now // self.window_len * self.window_len
        
        await self._clean_up_counters()
        
        counter = self.counters[client_ip]
        
        if counter["current_start"] != window_start:
            counter["previous"] = counter["current"]
            counter["current"] = 0
            counter["current_start"] = window_start
        
        weight = (now - window_start) / self.window_len 
        estimated = (counter["previous"] * (1 - weight)) + counter["current"]
        if estimated >= self.throttle_rate:
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={"detail":"Too many requests"},
                headers={
                    "X-RateLimit-Limit": str(self.throttle_rate), 
                    "Retry-After": str(self.window_len)
                }
            )
        counter["current"] += 1
        return await call_next(request)
    
    async def _clean_up_counters(self):
        for key in self.counters:
            if time.time() - self.counters[key]["current_start"] >= 2*self.window_len:
                self.counters.pop(key)




























