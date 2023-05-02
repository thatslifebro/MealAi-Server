from pydantic import BaseModel, EmailStr
from enum import Enum


class GenderEnum(str, Enum):
    M = "M"
    F = "F"


class GoalEnum(str, Enum):
    balance = "balance"
    diet = "diet"
    muscle = "muscle"
    lchf = "lchf"


class CreateUserResponse(BaseModel):
    email: EmailStr
    nickname: str


class GetUserInfoResponse(BaseModel):
    email: EmailStr
    gender: GenderEnum
    age_group: int
    nickname: str
    goal: GoalEnum


class EditUserInfoResponse(BaseModel):
    gender: GenderEnum
    age_group: int
    nickname: str
    goal: GoalEnum
