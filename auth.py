from fastapi import APIRouter, Request, HTTPException
from authlib.integrations.starlette_client import OAuth
from starlette.config import Config as StarletteConfig
from config import settings
from pydantic import BaseModel, EmailStr

router = APIRouter()

# Defined a Pydantic model for the user
class User(BaseModel):
    firstname: str | None = None
    lastname: str | None = None
    email: EmailStr
    picture: str | None = None

# Created OAuth instance
oauth = OAuth(StarletteConfig(".env"))

# Register Google OAuth
oauth.register(
    name="google",
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)

# Login endpoint → redirects to Google consent screen
@router.get("/login")
async def login(request: Request):
    redirect_uri = request.url_for("auth_callback")
    return await oauth.google.authorize_redirect(request, redirect_uri)

# Callback endpoint → receives code and fetches user info
@router.get("/callback", response_model=User)
async def auth_callback(request: Request):
    token = await oauth.google.authorize_access_token(request)
    user_info = await oauth.google.userinfo(token=token)

    if not user_info:
        raise HTTPException(status_code=400, detail="Failed to fetch user info")

    # Parse user info into Pydantic model
    user = User(
        firstname=user_info.get("given_name"),
        lastname=user_info.get("family_name"),
        email=user_info.get("email"),
        picture=user_info.get("picture"),
    )

    # For now, just return user info (no DB)
    return user
