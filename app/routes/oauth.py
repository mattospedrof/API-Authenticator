from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.user import TokenResponse
from app.services import oauth_service
from app.core.config import settings

router = APIRouter()


@router.get("/google/url")
def google_auth_url():
    url = (
        "https://accounts.google.com/o/oauth2/v2/auth"
        f"?client_id={settings.GOOGLE_CLIENT_ID}"
        f"&redirect_uri={settings.FRONTEND_URL}/oauth/google/callback"
        "&response_type=code"
        "&scope=openid email profile"
    )
    return {"url": url}


@router.post("/google/callback", response_model=TokenResponse)
async def google_callback(code: str, db: Session = Depends(get_db)):
    return await oauth_service.handle_google_oauth(code, db)


@router.get("/github/url")
def github_auth_url():
    url = (
        "https://github.com/login/oauth/authorize"
        f"?client_id={settings.GITHUB_CLIENT_ID}"
        "&scope=user:email"
    )
    return {"url": url}


@router.post("/github/callback", response_model=TokenResponse)
async def github_callback(code: str, db: Session = Depends(get_db)):
    return await oauth_service.handle_github_oauth(code, db)
