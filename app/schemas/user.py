from pydantic import BaseModel, Field

from app.models.enums import Department, Gender, Role


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


# 회원 정보 수정 요청 데이터
class UserProfileUpdate(BaseModel):
    department: Department | None = None
    phone_number: str | None = Field(
        default=None,
        min_length=10,
        max_length=20,
        pattern=r"^01[016789]-?\d{3,4}-?\d{4}$",
    )

# 회원 권한 변경 요청 데이터
class UserRoleUpdate(BaseModel):
    role: Role
