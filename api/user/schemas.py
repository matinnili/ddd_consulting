from pydantic import BaseModel, Field
from typing import Literal,Optional

class UserUpdateProfile(BaseModel):
    first_name: Optional[str] = Field(default=None, description="The first name of the user")
    last_name: Optional[str] = Field(default=None, description="The last name of the user")
    gender: Optional[Literal["male", "female"]] = Field(default=None, description="The gender of the user")



class UserFilter(BaseModel):
    username: Optional[str] = Field(default=None, description="The username of the user")
    first_name: Optional[str] = Field(default=None, description="The first name of the user")
    last_name: Optional[str] = Field(default=None, description="The last name of the user")
    gender: Optional[Literal["male", "female"]] = Field(default=None, description="The gender of the user")