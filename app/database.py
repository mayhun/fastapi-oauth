from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from typing import AsyncGenerator
import os

# SQLite 
DB_URL = "sqlite+aiosqlite:///./social_login.db"

# Async Engine 생성
engine = create_async_engine(DB_URL, echo=True, future=True)

# Async 세센팩토리
SessionLocal = async_sessionmaker(
    bind=engine,              # DB 연결 엔진
    class_=AsyncSession,      # 비동기 세션 클래스 사용
    autoflush=False,          # 자동 flush 비활성화 (직접 commit/flush)
    autocommit=False,         # 자동 commit 비활성화 (명시적 commit 필요)
    expire_on_commit=False    # commit 후에도 ORM 객체를 만료시키지 않음 (재사용 가능)
)

# Base 모델
Base = declarative_base()

# Dependency Injection 
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session