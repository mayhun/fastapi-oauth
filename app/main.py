from fastapi import FastAPI, APIRouter
from app.routers import users, oauth
from app.database import engine, Base
from app import models

from starlette.middleware.cors import CORSMiddleware

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 앱 시작 시 테이블 생성
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # 앱 종료 시 커넥션 정리(선택)
    await engine.dispose()

app = FastAPI(lifespan=lifespan)

app.include_router(users.router)
app.include_router(oauth.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
