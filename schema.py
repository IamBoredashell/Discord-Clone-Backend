import pydantic

#Token 
class TokenPayload(pydantic.BaseModel):
    sub: str
    username: str
    exp: int 


#Login route
class LoginRequest(pydantic.BaseModel):
    email: pydantic.EmailStr
    password: pydantic.constr(min_length=8,max_length=64) 

class LoginResponse(pydantic.BaseModel):
    token: pydantic.constr(min_length=4,max_length=64)

#admin route
class AddUserRequest(pydantic.BaseModel):
    email: pydantic.EmailStr
    username: pydantic.constr(min_length=4,max_length=64)
    password: pydantic.constr(min_length=4,max_length=64)
    role:   str

