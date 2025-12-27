from uow import SqlUnitOfWork, AbstractUnitOfWork
from models import User
from typing import List
from models import ResumeDetail
from api.user.schemas import UserUpdateProfile,UserFilter

class UserService:
    def __init__(self, uow: AbstractUnitOfWork):
        self.uow = uow

    async def login(self, username: str, password: str) -> User:
        with self.uow as uow:
            user = await uow.users.get(username)
            if not user:
                raise ValueError("User not found")
            if user.password != password:
                raise ValueError("Invalid password")
        return user
    async def create_user(self, user: User) -> User:
        with self.uow as uow:
            if await uow.users.get(user.username):
                raise ValueError("User already exists")
            await uow.users.add(user)
            await uow.commit()
        return user
    async def get_user(self, user_id: str) -> User:
        with self.uow as uow:
            user = await uow.users.get(user_id)
            if not user:
                raise ValueError("User not found")
            return user
    async def list_users(self, filters: UserFilter) -> List[User]:
        with self.uow as uow:
            if not filters:
                filters = {}
            else:
                filters = filters.model_dump(exclude_none=True)
            users = await uow.users.list(filters=filters)
            if not users:
                raise ValueError("No users found")  
            return users
    async def update_user_profile(self, user: User, user_update_profile: UserUpdateProfile) -> User:
        with self.uow as uow:
            if not await uow.users.get(user.id):
                raise ValueError("User not found")
            updated_data=user_update_profile.model_dump(exclude_unset=True)
            for key, value in updated_data.items():
                setattr(user, key, value)
            await uow.users.merge(user.username,user)
            
            await uow.commit()
            return user
    async def update_resume_details(self, user: User, resume_details: ResumeDetail) -> User:
        with self.uow as uow:
            if not await uow.users.get(user.username):
                raise ValueError("User not found")
            user.add_resumedetails(resume_details)
            await uow.users.merge(user.username,user)
            await uow.commit()
            return user