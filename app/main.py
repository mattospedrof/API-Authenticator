from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth, users, oauth
from app.core.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Auth API",
    description="Production-ready authentication API with JWT, OAuth, and password recovery.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(oauth.router, prefix="/oauth", tags=["OAuth"])


@app.get("/", tags=["Health"])
def health_check():
    return {"status": "ok", "message": "Auth API is running 🚀"}
