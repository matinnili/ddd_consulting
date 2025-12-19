from uow import SqlUnitOfWork
from models import User
from typing import List
class UserService:
    def __init__(self, uow: SqlUnitOfWork):
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
    async def list_users(self) -> List[User]:
        with self.uow as uow:
            users = await uow.users.list()
            if not users:
                raise ValueError("No users found")  
            return users
    async def update_user(self, user: User) -> User:
        with self.uow as uow:
            if not await uow.users.get(user.id):
                raise ValueError("User not found")
            user = await uow.users.update(user)
            await uow.commit()
            return user