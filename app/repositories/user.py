from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    # 같은 이메일 또는 휴대폰 번호를 가진 사용자가 있는지 확인
    async def find_duplicate(
        self,
        email: str,
        phone_number: str,
    ) -> User | None:
        result = await self.session.execute(
            select(User).where(
                or_(
                    User.email == email,
                    User.phone_number == phone_number,
                )
            )
        )

        return result.scalar_one_or_none()

    # 이메일로 사용자 조회
    async def find_by_email(self, email: str) -> User | None:
        result = await self.session.execute(
            select(User).where(User.email == email)
        )

        return result.scalar_one_or_none()

    # 사용자 ID로 조회
    async def find_by_id(self, user_id: int) -> User | None:
        result = await self.session.execute(
            select(User).where(User.id == user_id)
        )

        return result.scalar_one_or_none()

    # 비밀번호 변경
    async def update_password(
        self,
        user: User,
        hashed_password: str,
    ) -> User:
        user.hashed_password = hashed_password

        await self.session.commit()
        await self.session.refresh(user)

        return user

    # 새로운 사용자 저장
    async def create(self, user: User) -> User:
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)

        return user