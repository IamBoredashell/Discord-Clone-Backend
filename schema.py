import pydantic

#Login route
class LoginRequest(pydantic.BaseModel):
    email: pydantic.EmailStr
    password: str

class LoginResponse(pydantic.BaseModel):
    token: str

#admin route
class AddUserRequest(pydantic.BaseModel):
    email: pydantic.EmailStr
    username: str
    password: str


class AddUserResponse(pydantic.BaseModel):
    
