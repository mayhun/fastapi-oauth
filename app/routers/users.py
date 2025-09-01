from fastapi import APIRouter, Depends, HTTPException, status, Response
from app.schemas import users_schema
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app import crud

router = APIRouter(prefix='/api/users')

@router.post('', summary='회원가입', tags=['Users'])
async def signup(new_user:users_schema.NewUserForm, db: AsyncSession = Depends(get_db)):
    '''
    회원가입
    '''
    user = await crud.get_user(new_user.email, db, provider='LOCAL')
    if user:
        raise HTTPException(status_code=409, detail='User already exists')
    
    await crud.create_user(new_user, db)
    
    return {'message': f'{new_user.name} User create Success'}

@router.post('/login', summary='로그인', tags=['Auth'])
async def login(req: users_schema.UserForm, db: AsyncSession = Depends(get_db)):
    '''
    로그인
    '''
    if not req.email or not req.password:
        raise HTTPException(status_code=400, detail='Missing email or password')
    
    user = await crud.get_user(req.email, db)
    if not user or not crud.verify_password(req.password, user.hashed_pw):
        raise HTTPException(status_code=401, detail='Login failed')
    
    return {'message': 'Login Success'}