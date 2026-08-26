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

    # 새로운 사용자 저장
    async def create(self, user: User) -> User:
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)

        return user