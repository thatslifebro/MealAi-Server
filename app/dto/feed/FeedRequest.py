from pydantic import BaseModel, Field
from typing import List
from enum import Enum


class GoalEnum(str, Enum):
    balance = "balance"
    diet = "diet"
    muscle = "muscle"
    lchf = "lchf"


class MealTimeEnum(str, Enum):
    breakfast = "breakfast"
    lunch = "lunch"
    dinner = "dinner"
    snack = "snack"


class FilterEnum(str, Enum):
    popularity = "popularity"
    newest = "newest"


class Food(BaseModel):
    food_id: int = Field(..., title="음식 id")
    image_url: str = Field(..., title="음식 별 사진 URL")
    weight: float = Field(..., title="음식의 양")


class PostFeed(BaseModel):
    image_url: str = Field(..., title="전체 이미지 URL")
    meal_time: MealTimeEnum = Field(..., title="식사 종류", description="B,L,D,S")
    date: str = Field(..., title="식사 날짜")
    foods: List[Food] = Field(..., title="먹은 음식")
    open: bool = Field(..., title="공개 여부", description="True or False")


class PatchFeedData(BaseModel):
    meal_time: MealTimeEnum = Field(..., title="식사 종류", description="B,L,D,S")
    date: str = Field(..., title="식사 날짜")
    foods: List[Food] = Field(..., title="먹은 음식들")
    open: bool = Field(..., title="공개 여부", description="True or False")
