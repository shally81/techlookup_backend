from fastapi import FastAPI, Depends, HTTPException, Request
from starlette.responses import JSONResponse
from .schemas import DetectRequest, DetectResponse
from .rate_limiter import MemoryRateLimiter
from .config import get_settings
from .fetcher import fetch_html
from .detector import detect
import asyncio

app = FastAPI(title="TechLookup API", version="0.1")

settings = get_settings()
limiter = MemoryRateLimiter(settings.rate_limit)

@app.post("/detect", response_model=DetectResponse)
async def detect_handler(body: DetectRequest, request: Request):
    client_ip = request.client.host
    if not limiter.allow(client_ip):
        raise HTTPException(status_code=429, detail="Rate limit exceeded")

    html, headers = await fetch_html(str(body.url))
    tech = detect(html, headers)
    return DetectResponse(url=body.url, technologies=tech)

@app.exception_handler(Exception)
async def handle_any(request: Request, exc: Exception):
    return JSONResponse(status_code=500, content={"detail": str(exc)})