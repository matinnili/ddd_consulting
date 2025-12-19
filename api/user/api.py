from fastapi import APIRouter

router = APIRouter()

@router.post("/")
async def create_user(user: User):
    return await user_service.create_user(user)