from pydantic import BaseModel, EmailStr
from enum import Enum


class GenderEnum(str, Enum):
    M = "M"
    F = "F"


class PurposeEnum(str, Enum):
    balance = "balance"
    diet = "diet"
    muscle = "muscle"
    lchf = "lchf"


class CreateUserResponse(BaseModel):
    email: EmailStr
    gender: GenderEnum
    age_group: int
    nickname: str
    purpose: PurposeEnum


class GetUserInfoResponse(BaseModel):
    email: EmailStr
    gender: GenderEnum
    age_group: int
    nickname: str
    purpose: PurposeEnum


class EditUserInfoResponse(BaseModel):
    gender: GenderEnum
    age_group: int
    nickname: str
    purpose: PurposeEnum
