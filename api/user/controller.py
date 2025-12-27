from fastapi import APIRouter
from user_domain_service.service import UserService
from user_domain_service.uow import SqlUnitOfWork
from user_domain_service.repository import UserRepository
from user_domain_service.models import User
from user_domain_service.schemas import UserUpdateProfile,UserFilter
from user_domain_service.dependencies import get_current_user
from user_domain_service.exceptions import UserNotFoundError,UserAlreadyExistsError
from user_domain_service.utils import get_password_hash
from user_domain_service.utils import get_password_hash
from fastapi import Depends
router = APIRouter()


router = APIRouter(prefix="/api/v1/employer")

@router.post("/add_employee", response_model=str)
async def add_employee(new_employee: dict, current_user: dict = Depends(UserService().login)):
    pass
   
