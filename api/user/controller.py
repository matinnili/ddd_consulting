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

router = APIRouter()


router = APIRouter(prefix="/api/v1/employer")

@router.post("/add_employee", response_model=str)
async def add_employee(new_employee: dict, current_user: dict = Depends(UserService().login)):
    """
    Endpoint to add a new employee.
    Only users with access_level 1 are allowed to add employees.
    The new employee's company_name is set to the current user's company_name.
    """
    if current_user.get("access_level", 0) != 1:
        raise HTTPException(status_code=403, detail="Insufficient permissions to add an employee.")

    try:
        employee_data = new_employee

        # Add await for username check
        if await exist_username(employee_data.get("username")):
            return JSONResponse(status_code=400, content={"detail": "the username already exist"})
        
        employee_data["company_name"] = current_user.get("company_name", "")
        
        password = get_password_hash(employee_data.get("password"))
        employee_data["password"] = password
        
        employee_data["access_level"] = employee_data.get("access_level", 3)
        employee_data["disabled"] = False

        # Keep resume_detail as object (dict) for MongoDB - no conversion needed
        # If it's a dict, it will be stored as a nested document in MongoDB
        
        # Keep personality_test as object (list) for MongoDB - no conversion needed
        # If it's a list, it will be stored as an array in MongoDB
        
        # Initialize empty fields if not provided
        if not new_employee.get("resume_detail"):
             employee_data["resume_detail"] = ResumeDetail().model_dump()
        if new_employee.get("cognitivetest_result"):
             print(f"this new_employee cognitivetest_result: {new_employee.get('cognitivetest_result')}")
             employee_data["cognitivetest_result"] = str(new_employee.get("cognitivetest_result"))
             print(f"this is json.dumps cognitivetest_result: {employee_data['cognitivetest_result']}")
        if new_employee.get("courses"):
            print(f"this new_employee courses: {new_employee.get('courses')}")
            employee_data["courses"] = str(new_employee.get("courses"))
            print(f"this is json.dumps courses: {employee_data['courses']}")
        for key in ["cv", "characteristics", "email", "courses"]:
            if key not in employee_data or not employee_data[key]:
                employee_data[key] = ""

        # Add await for MongoDB insert operation
        await person_collection.insert_one(employee_data)
        
        return "با موفقیت ثبت شد"
