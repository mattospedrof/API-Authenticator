import httpx
from sqlalchemy.orm import Session
from app.models.user import User, OAuthProvider
from app.core.security import create_access_token, create_refresh_token
from app.core.config import settings


async def handle_google_oauth(code: str, db: Session) -> dict:
    token_url = "https://oauth2.googleapis.com/token"
    data = {
        "code": code,
        "client_id": settings.GOOGLE_CLIENT_ID,
        "client_secret": settings.GOOGLE_CLIENT_SECRET,
        "redirect_uri": f"{settings.FRONTEND_URL}/oauth/google/callback",
        "grant_type": "authorization_code",
    }
    async with httpx.AsyncClient() as client:
        token_res = await client.post(token_url, data=data)
        token_data = token_res.json()
        user_res = await client.get(
            "https://www.googleapis.com/oauth2/v2/userinfo",
            headers={"Authorization": f"Bearer {token_data['access_token']}"}
        )
        user_info = user_res.json()

    return _get_or_create_oauth_user(db, user_info["email"], user_info["name"], OAuthProvider.google, user_info["id"])


async def handle_github_oauth(code: str, db: Session) -> dict:
    async with httpx.AsyncClient() as client:
        token_res = await client.post(
            "https://github.com/login/oauth/access_token",
            data={
                "client_id": settings.GITHUB_CLIENT_ID,
                "client_secret": settings.GITHUB_CLIENT_SECRET,
                "code": code,
            },
            headers={"Accept": "application/json"}
        )
        token_data = token_res.json()
        user_res = await client.get(
            "https://api.github.com/user",
            headers={"Authorization": f"Bearer {token_data['access_token']}"}
        )
        email_res = await client.get(
            "https://api.github.com/user/emails",
            headers={"Authorization": f"Bearer {token_data['access_token']}"}
        )
        user_info = user_res.json()
        emails = email_res.json()
        primary_email = next((e["email"] for e in emails if e["primary"]), None)

    return _get_or_create_oauth_user(db, primary_email, user_info["name"] or user_info["login"], OAuthProvider.github, str(user_info["id"]))


def _get_or_create_oauth_user(db: Session, email: str, name: str, provider: OAuthProvider, oauth_id: str) -> dict:
    user = db.query(User).filter(User.email == email).first()
    if not user:
        user = User(email=email, name=name, oauth_provider=provider, oauth_id=oauth_id, is_verified=True)
        db.add(user)
        db.commit()
        db.refresh(user)

    access_token = create_access_token({"sub": str(user.id)})
    refresh_token = create_refresh_token({"sub": str(user.id)})
    user.refresh_token = refresh_token
    db.commit()
    return {"access_token": access_token, "refresh_token": refresh_token}
