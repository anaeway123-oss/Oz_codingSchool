from pwdlib import PasswordHash
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import (
    create_access_token,
    create_refresh_token,
    verify_password,
)
from app.models.enums import Role
from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.user import (
    UserCreate,
    UserLogin,
    UserPasswordUpdate,
    UserProfileUpdate,
)

password_hash = PasswordHash.recommended()


class UserService:
    def __init__(self, session: AsyncSession):
        self.repository = UserRepository(session)

    # 회원가입
    async def create_user(self, user_data: UserCreate) -> User:
        # 이메일 또는 휴대폰 번호 중복 확인
        duplicate_user = await self.repository.find_duplicate(
            email=user_data.email,
            phone_number=user_data.phone_number,
        )

        if duplicate_user is not None:
            raise ValueError("이미 사용 중인 이메일 또는 휴대폰 번호입니다.")

        # 비밀번호 해싱
        hashed_password = password_hash.hash(user_data.password)

        # 신규 사용자 객체 생성
        new_user = User(
            email=user_data.email,
            hashed_password=hashed_password,
            name=user_data.name,
            department=user_data.department,
            gender=user_data.gender,
            phone_number=user_data.phone_number,
            role=Role.PENDING,
        )

        # DB 저장
        return await self.repository.create(new_user)

    # 로그인
    async def login(self, login_data: UserLogin) -> dict:
        # 이메일로 사용자 조회
        user = await self.repository.find_by_email(login_data.email)

        if user is None:
            raise ValueError("이메일 또는 비밀번호가 올바르지 않습니다.")

        # 비밀번호 확인
        if not verify_password(
            login_data.password,
            user.hashed_password,
        ):
            raise ValueError("이메일 또는 비밀번호가 올바르지 않습니다.")

        # Access Token / Refresh Token 생성
        access_token = create_access_token(user.id)
        refresh_token = create_refresh_token(user.id)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }

    # 회원 정보 수정
    async def update_profile(
        self,
        user: User,
        profile_data: UserProfileUpdate,
    ) -> User:
        # 요청에 실제로 포함된 값만 추출
        update_data = profile_data.model_dump(
            exclude_unset=True,
            exclude_none=True,
        )

        # 수정할 값이 하나도 없는 경우
        if not update_data:
            raise ValueError("수정할 정보를 하나 이상 입력해주세요.")

        # 휴대폰 번호가 전달된 경우 중복 확인
        phone_number = update_data.get("phone_number")

        if phone_number is not None:
            duplicate_user = await self.repository.find_by_phone_number(
                phone_number
            )

            if (
                duplicate_user is not None
                and duplicate_user.id != user.id
            ):
                raise ValueError("이미 사용 중인 휴대폰 번호입니다.")

        # 전달된 항목만 DB에 반영
        return await self.repository.update_profile(
            user=user,
            department=update_data.get("department"),
            phone_number=phone_number,
        )

    # 비밀번호 변경
    async def change_password(
        self,
        user: User,
        password_data: UserPasswordUpdate,
    ) -> User:
        # 현재 비밀번호 확인
        if not verify_password(
            password_data.current_password,
            user.hashed_password,
        ):
            raise ValueError("현재 비밀번호가 일치하지 않습니다.")

        # 새로운 비밀번호 해싱
        new_hashed_password = password_hash.hash(
            password_data.new_password
        )

        # 변경된 비밀번호 DB 저장
        return await self.repository.update_password(
            user,
            new_hashed_password,
        )