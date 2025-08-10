from fastapi import FastAPI
from app.routes import auth_router, users_router  # Исправленный импорт
from app.core.config import settings

app = FastAPI(
    title="Auth Service API",
    version="1.0.0",
    openapi_url="/api/openapi.json"
)

# Включаем роутеры
app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.include_router(users_router, prefix="/api/users", tags=["users"])

@app.get("/")
def health_check():
    return {"status": "ok", "version": app.version}