import datetime

import bcrypt
from pydantic import BaseModel, Field, EmailStr, validator


class UserIn(BaseModel):
    first_name: str = Field(..., min_length=2, max_length=24)
    last_name: str = Field(..., min_length=2, max_length=24)
    birth_date: datetime.date = Field(format='%Y-%m-%d')
    address: str = Field(min_length=5)
    email: EmailStr = Field(..., max_length=64)
    password: str = Field(..., min_length=8)

    @validator('password')
    def hash_password(cls, value):
        return bcrypt.hashpw(value.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


class User(UserIn):
    user_id: int
