from sqlalchemy import Column, Integer, VARCHAR, DateTime
from datetime import datetime

from app.database import Base

class User(Base):
    __tablename__ = 'Users'

    user_no = Column(Integer, primary_key=True, autoincrement=True, comment="사용자 고유번호 (PK)")
    user_name = Column(VARCHAR(10), nullable=False, comment="사용자 이름")
    email = Column(VARCHAR(100), nullable=False, unique=True, comment="사용자 이메일 (로그인 ID)")
    hashed_pw = Column(VARCHAR(100), nullable=True, comment="비밀번호 해시값 (소셜 로그인일 경우 NULL)")
    role = Column(VARCHAR(20), nullable=False, default='MEMBER', comment="권한(ADMIN / MEMBER 등)")
    status = Column(VARCHAR(1), nullable=False, default='1', comment="계정 상태 (1=활성, 0=비활성)")
    regdate = Column(DateTime, nullable=False, default=datetime.now, comment="가입일시")
    provider = Column(VARCHAR(20), nullable=False, comment="소셜 로그인 공급자 (GOOGLE/KAKAO/NAVER/LOCAL)")