from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.services import oauth_service
from app.schemas.social_schema import SocialLogin, PROVIDER_ENUM
from app import crud
from app.database import get_db

router = APIRouter(prefix='/api/oauth')

@router.post('/{provider}', summary='OAuth 2.0 소셜 로그인 / 회원 가입', tags=['OAuth'])
async def social_auth(provider: str, form: SocialLogin, db: AsyncSession = Depends(get_db)):
    '''
    소셜 로그인
    - OAuth 2.0 소셜 로그인
        - 미가입 사용자 로그인 시 자동 회원가입 처리
    '''
    
    # provider에 따라 분기 처리
    provider = PROVIDER_ENUM.from_str(provider.lower())
    if not provider:
        raise HTTPException(status_code=404)
    try:
        if provider == PROVIDER_ENUM.GOOGLE:
            user_data = oauth_service.auth_google(form.code)
        elif provider == PROVIDER_ENUM.KAKAO:
            user_data = oauth_service.auth_kakao(form.code)
        elif provider == PROVIDER_ENUM.NAVER:
            user_data = oauth_service.auth_naver(form.code)
        
        user = await crud.get_user(user_data.email, db, provider=user_data.provider)
        print(f"user: {user}")
        
        # 존재하는 회원 시 로그인
        if user and user.status != '9':
            return {'message': 'oauth login successful', 'name': user_data.name}
        else:
            # 존재하지 않는 회원시 회원 가입 처리
            await crud.create_social_user(user_data, db)
        return {'message': 'oauth register successful', 'name': user_data.name}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))