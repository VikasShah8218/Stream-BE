from pydantic import BaseModel

class UserForm(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool

    # class Config:
    #     orm_mode = True
