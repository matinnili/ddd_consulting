from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from typing import Optional
from pydantic import BaseModel

# Configuration - move to config.py later
SECRET_KEY = "your-secret-key-change-in-production"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")


class TokenData(BaseModel):
    username: Optional[str] = None
    access_level: Optional[int] = None
    company_name: Optional[str] = None


async def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    """
    Validates JWT token and returns user data.
    Use as dependency for protected endpoints.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        
        return {
            "username": username,
            "access_level": payload.get("access_level", 3),
            "company_name": payload.get("company_name", "")
        }
    except JWTError:
        raise credentials_exception


def require_access_level(min_level: int):
    """
    Factory that returns a dependency requiring specific access level.
    Lower number = higher privilege (1=admin, 2=manager, 3=employee)
    """
    async def check_access(current_user: dict = Depends(get_current_user)) -> dict:
        if current_user.get("access_level", 99) > min_level:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Insufficient permissions. Required access level: {min_level}"
            )
        return current_user
    return check_access