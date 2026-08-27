from pydantic import BaseModel

from app.models.enums import Department, Gender


# 회원가입 요청 데이터
class UserCreate(BaseModel):
    email: str
    password: str
    name: str
    department: Department
    gender: Gender
    phone_number: str


# 로그인 요청 데이터
class UserLogin(BaseModel):
    email: str
    password: str


# 비밀번호 변경 요청 데이터
class UserPasswordUpdate(BaseModel):
    current_password: str
    new_password: str