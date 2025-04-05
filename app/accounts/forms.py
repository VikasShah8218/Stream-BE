from pydantic import BaseModel, EmailStr, constr

class UserRegisterForm(BaseModel):
    username: str
    email: EmailStr
    password: str


class LoginRequestForm(BaseModel):
    username: str
    password: str