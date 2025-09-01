from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import User
from app.schemas.users_schema import NewUserForm
from app.schemas.social_schema import SocialMember
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

async def get_user(email: str, db: AsyncSession, provider: str = None) -> User | None:
    '''
    사용자 조회
    '''
    # 소셜 로그인 확인
    if provider:
        result = await db.execute(select(User).where(User.email == email, User.provider == provider))

    else:
        result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()

async def create_user(new_user: NewUserForm, db: AsyncSession):
    '''
    회원가입
    '''
    user = User(
        user_name = new_user.name,
        email=new_user.email,
        hashed_pw = pwd_context.hash(new_user.password),
        provider = new_user.provider
    )
    db.add(user)
    await db.commit()
    return user

async def create_social_user(new_user: SocialMember, db:AsyncSession):
    '''
    소셜 회원가입
    '''
    user = User(
        user_name=new_user.name,
        email=new_user.email,
        provider=new_user.provider
    )
    db.add(user)
    await db.commit()
    return user

def verify_password(plain_password: str, hashed_password: str) -> bool:
    '''
    패스워드 확인
    '''
    return pwd_context.verify(plain_password, hashed_password)