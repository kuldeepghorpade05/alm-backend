from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from auth import router as auth_router
from config import settings  # optional if you want a secret key from .env

app = FastAPI(title="ALM Backend - OAuth Test")

# 🔑 Add this BEFORE mounting routers
app.add_middleware(
    SessionMiddleware,
    secret_key="YOUR_RANDOM_SECRET_KEY",  # can also use settings.SECRET_KEY from .env
    https_only=False  # True in production with HTTPS
)

# Mount auth router
app.include_router(auth_router, prefix="/api/auth", tags=["Auth"])

@app.get("/")
async def hello():
    return {"message": "Hello World"}
