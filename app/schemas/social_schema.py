from pydantic import BaseModel, Field
from enum import Enum
from typing import Optional, Union


class PROVIDER_ENUM(Enum):
    '''
    소셜 로그인 공급자 정의
    '''
    GOOGLE = "google"
    KAKAO = "kakao"
    NAVER = "naver"
    
    def __init__(self, title):
        self.title = title

    @classmethod
    def from_str(cls, name: str):
        for enum in cls:
            if enum.value == name:
                return enum


class SocialLogin(BaseModel):
    '''
    소셜 로그인 요청 모델
    '''
    code: str


class SocialMember(BaseModel):
    '''
    OAuth2.0 소셜 회원 가입 요청 모델'''
    email: Optional[str] = Field(
        description='소셜계정 메일 정보',
        example='test@gmail.com'
    )
    name: Optional[str] = Field(
        description='소셜 이름 정보',
        example='홍길동'
    )
    provider: Union[str, PROVIDER_ENUM] = Field(
        description='소셜 출처',
        examples='KAKAO'
    )