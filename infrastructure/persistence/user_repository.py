from repository import UserRepository
from models import User
from typing import List, Optional


class SqlUserRepository(UserRepository):

    def __init__(self, session):
        self.session = session

    async def add(self, user: User) -> None:
        # Implementation for adding a user to a SQL database
        session=self.session
        session.add(user)
        session.commit()

    async def get(self, user_id: str) -> Optional[User]:
        # Implementation for retrieving a user by ID from a SQL database
        session=self.session
        user=session.query(User).filter_by(id=user_id)
        return user.first()

    async def list(self) -> List[User]:
        # Implementation for listing all users from a SQL database
        session=self.session
        users=session.query(User).all()
        return users