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
    