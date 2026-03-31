from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.config import settings
from app.api.jobs import router as jobs_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f"🚀 {settings.app_name} v{settings.app_version} iniciando...")
    yield
    print(f"👋 {settings.app_name} encerrando...")


app = FastAPI(
    title=settings.app_name,
    description=settings.app_description,
    version=settings.app_version,
    lifespan=lifespan,
)

app.include_router(jobs_router)


@app.get("/", tags=["health"])
async def root() -> dict:
    return {
        "app": settings.app_name,
        "version": settings.app_version,
        "status": "online",
        "debug": settings.debug,
    }


@app.get("/health", tags=["health"])
async def health_check() -> dict:
    return {"status": "ok"}