from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, field_validator
from typing import Optional
import re


# API들을 묶어서 관리할 Router를 생성합니다.
router = APIRouter(
    prefix="/practice_api",
    tags=["practice_api"]
)


# 과제에서 제공한 기본 회원 데이터
user_list = [
    {
        "id": 1,
        "name": "홍길동",
        "age": 24,
        "email": "gildong24@example.com",
        "password": "Password1234!!"
    },
    {
        "id": 2,
        "name": "장문복",
        "age": 21,
        "email": "moonluck12@example.com",
        "password": "Check1321!"
    },
    {
        "id": 3,
        "name": "임우진",
        "age": 31,
        "email": "limousine33@example.com",
        "password": "lwsPAssword12@"
    }
]


# -----------------------------------------
# 공통 검증 함수
# -----------------------------------------

def validate_email(email: str):
    email_pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"

    if len(email) > 30:
        raise ValueError("이메일은 최대 30자까지 입력할 수 있습니다.")

    if not re.fullmatch(email_pattern, email):
        raise ValueError("올바른 이메일 형식이 아닙니다.")

    return email


def validate_password(password: str):
    if len(password) < 8 or len(password) > 20:
        raise ValueError("비밀번호는 최소 8자, 최대 20자여야 합니다.")

    if not re.search(r"[A-Z]", password):
        raise ValueError("비밀번호에는 대문자가 최소 1개 필요합니다.")

    if not re.search(r"[a-z]", password):
        raise ValueError("비밀번호에는 소문자가 최소 1개 필요합니다.")

    if not re.search(r"[^A-Za-z0-9]", password):
        raise ValueError("비밀번호에는 특수문자가 최소 1개 필요합니다.")

    return password


# -----------------------------------------
# Request Body 모델
# -----------------------------------------

class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=10)
    age: int = Field(ge=14)
    email: str
    password: str

    @field_validator("email")
    @classmethod
    def check_email(cls, value):
        return validate_email(value)

    @field_validator("password")
    @classmethod
    def check_password(cls, value):
        return validate_password(value)


class UserUpdate(BaseModel):
    age: Optional[int] = Field(default=None, ge=14)
    email: Optional[str] = None
    password: Optional[str] = None

    @field_validator("email")
    @classmethod
    def check_email(cls, value):
        if value is None:
            return value
        return validate_email(value)

    @field_validator("password")
    @classmethod
    def check_password(cls, value):
        if value is None:
            return value
        return validate_password(value)


# -----------------------------------------
# 응답용 함수
# password는 조회 결과에서 제외
# -----------------------------------------

def user_response(user):
    return {
        "id": user["id"],
        "name": user["name"],
        "age": user["age"],
        "email": user["email"]
    }


# -----------------------------------------
# 1. 모든 회원 정보 조회
# -----------------------------------------

@router.get("/users")
def get_users():
    return [user_response(user) for user in user_list]


# -----------------------------------------
# 2. 특정 회원 정보 조회
# -----------------------------------------

@router.get("/users/{user_id}")
def get_user(user_id: int):

    for user in user_list:
        if user["id"] == user_id:
            return user_response(user)

    raise HTTPException(
        status_code=404,
        detail="해당 회원을 찾을 수 없습니다."
    )


# -----------------------------------------
# 3. 회원 정보 추가
# -----------------------------------------

@router.post("/users", status_code=201)
def create_user(user: UserCreate):

    # 이메일 중복 검사
    for existing_user in user_list:
        if existing_user["email"] == user.email:
            raise HTTPException(
                status_code=400,
                detail="이미 사용 중인 이메일입니다."
            )

    # 새로운 id 자동 생성
    new_id = max(
        [existing_user["id"] for existing_user in user_list],
        default=0
    ) + 1

    new_user = {
        "id": new_id,
        "name": user.name,
        "age": user.age,
        "email": user.email,
        "password": user.password
    }

    user_list.append(new_user)

    return user_response(new_user)


# -----------------------------------------
# 4. 회원 정보 수정
# -----------------------------------------

@router.patch("/users/{user_id}")
def update_user(user_id: int, update_data: UserUpdate):

    # 모든 항목이 입력되지 않은 경우
    if (
        update_data.age is None
        and update_data.email is None
        and update_data.password is None
    ):
        raise HTTPException(
            status_code=400,
            detail="수정할 정보를 하나 이상 입력해주세요."
        )

    # 수정할 회원 찾기
    target_user = None

    for user in user_list:
        if user["id"] == user_id:
            target_user = user
            break

    if target_user is None:
        raise HTTPException(
            status_code=404,
            detail="해당 회원을 찾을 수 없습니다."
        )

    # 이메일이 입력된 경우 중복 확인
    if update_data.email is not None:
        for user in user_list:
            if (
                user["id"] != user_id
                and user["email"] == update_data.email
            ):
                raise HTTPException(
                    status_code=400,
                    detail="이미 사용 중인 이메일입니다."
                )

        target_user["email"] = update_data.email

    # 나이가 입력된 경우 수정
    if update_data.age is not None:
        target_user["age"] = update_data.age

    # 비밀번호가 입력된 경우 수정
    if update_data.password is not None:
        target_user["password"] = update_data.password

    return user_response(target_user)


# -----------------------------------------
# 5. 특정 회원 정보 삭제
# -----------------------------------------

@router.delete("/users/{user_id}")
def delete_user(user_id: int):

    for user in user_list:
        if user["id"] == user_id:
            user_list.remove(user)

            return {
                "message": "회원 정보가 삭제되었습니다."
            }

    raise HTTPException(
        status_code=404,
        detail="해당 회원을 찾을 수 없습니다."
    )