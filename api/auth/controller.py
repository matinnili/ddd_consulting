from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from user_domain_service.utils import verify_password, create_access_token
from user_domain_service.service import UserService
from user_domain_service.uow import SqlUserUnitOfWork

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


class Token(BaseModel):
    access_token: str
    token_type: str


@router.post("/token", response_model=Token)
async def login(uow : SqlUserUnitOfWork,form_data: OAuth2PasswordRequestForm = Depends()):
    """
    OAuth2 compatible login endpoint.
    Returns JWT token on successful authentication.
    """
    
    service = UserService(uow)
    
    try:
        user = await service.login(form_data.username, form_data.password)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(
        data={
            "sub": user.username,
            "access_level": getattr(user, 'access_level', 3),
            "company_name": getattr(user, 'company_name', '')
        }
    )
    
    return Token(access_token=access_token, token_type="bearer")