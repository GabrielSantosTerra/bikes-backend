from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    name: str
    password: str
    cpf: str
    birth_date: str
    phone: str
    email: EmailStr

class UserLogin(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    name: str
    cpf: str
    birth_date: str
    phone: str
    email: EmailStr
