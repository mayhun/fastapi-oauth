from pydantic import BaseModel, EmailStr, field_validator, Field

class UserForm(BaseModel):
    '''
    일반 로그인 요청 모델
    '''
    email: EmailStr = Field(
                    default=None,
                    description='사용자 메일',
                    example='test@gmail.com'
                    )
    
    password: str = Field(
                    default=None,
                    title='패스워드',
                    description='8자 이상, 공백 없음, 영문, 숫자 1개 이상 조합',
                    example='may12345'
    )

    # 공백만 입력 금지
    @field_validator("email", "password", mode="before")
    @classmethod
    def not_empty(cls, v):
        if v is None:
            raise ValueError("필수 항목을 입력하세요")
        if isinstance(v, str):
            v = v.strip()
            if v == '':
                raise ValueError('필수 항목을 입력하세요')
        return v
    
    # 비밀번호 규칙
    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str):
        if len(v) < 8:
            raise ValueError('비밀번호는 8자리 이상 영문과 숫자를 포함하여 작성해주세요.')
        if not any(ch.isdigit() for ch in v):
            raise ValueError('비밀번호는 숫자를 최소 1개 포함해야합니다.')
        if not any(ch.isalpha() for ch in v):
            raise ValueError('비밀번호는 영문자를 최소 1개 포함해야합니다.')
        return v

class NewUserForm(UserForm):
    '''
    일반 회원가입 요청 모델
    '''
    name: str = Field(
                default=None,
                description='사용자 이름',
                example='may'
                )
    provider: str = Field(
        default='LOCAL',
        description='OAuth2.0 소셜 출처'
    )
    # 공백만 입력 금지
    @field_validator("name", mode="before")
    @classmethod
    def not_empty(cls, v):
        if v is None:
            raise ValueError("필수 항목을 입력하세요")
        if isinstance(v, str):
            v = v.strip()
            if v == '':
                raise ValueError('필수 항목을 입력하세요')
        return v
