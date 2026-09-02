from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.enums import Department, Role
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
        normalized_phone = phone_number.replace("-", "")

        result = await self.session.execute(
            select(User).where(
                or_(
                    User.email == email,
                    func.replace(User.phone_number, "-", "") == normalized_phone,
                )
            )
        )

        return result.scalars().first()

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

    # 현재 사용자를 제외하고 같은 휴대폰 번호를 가진 사용자 조회
    async def find_other_by_phone_number(
        self,
        phone_number: str,
        exclude_user_id: int,
    ) -> User | None:
        normalized_phone = phone_number.replace("-", "")

        result = await self.session.execute(
            select(User).where(
                func.replace(User.phone_number, "-", "") == normalized_phone,
                User.id != exclude_user_id,
            )
        )

        return result.scalars().first()

    # 전체 사용자 조회
    async def get_all_users(self) -> list[User]:
        result = await self.session.execute(
            select(User)
        )

        return list(result.scalars().all())

    # 회원 정보 수정
    async def update_profile(
        self,
        user: User,
        department: Department | None = None,
        phone_number: str | None = None,
    ) -> User:
        # 전달된 값만 수정
        if department is not None:
            user.department = department

        if phone_number is not None:
            user.phone_number = phone_number

        await self.session.commit()
        await self.session.refresh(user)

        return user

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


    # 회원 권한 변경
    async def update_role(
        self,
        user: User,
        role: Role,
    ) -> User:
        user.role = role

        await self.session.commit()
        await self.session.refresh(user)

        return user

    # 새로운 사용자 저장
    async def create(self, user: User) -> User:
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)

        return user