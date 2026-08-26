from pwdlib import PasswordHash
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.enums import Role
from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate


password_hash = PasswordHash.recommended()


class UserService:
    def __init__(self, session: AsyncSession):
        self.repository = UserRepository(session)

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
    