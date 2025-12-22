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

    async def list(self,filters: dict =None) -> List[User]:
        # Implementation for listing all users from a SQL database
        session=self.session
        query=session.query(User)
        if filters:
            if filters.get("username"):
                query=query.filter(User.username==filters["username"])
            if filters.get("first_name"):
                query=query.filter(User.first_name==filters["first_name"])
            if filters.get("last_name"):
                query=query.filter(User.last_name==filters["last_name"])
            if filters.get("gender"):
                query=query.filter(User.gender==filters["gender"])
        users=query.all()
        return users