from pydantic import BaseModel, Field
from typing import List
from enum import Enum


class MealTime(str, Enum):
    Breakfast: "B"
    Lunch: "L"
    Dinner: "D"
    Snack: "S"


class Food(BaseModel):
    food_id: int = Field(title="음식 id")
    image_url: str = Field(title="음식 별 사진 URL")
    weight: float = Field(title="음식의 양")


class PostFeed(BaseModel):
    image_url: str = Field(title="전체 이미지 URL")
    meal_time: MealTime = Field(title="식사 종류", description="B,L,D,S")
    date: str = Field(title="식사 날짜")
    foods: List[Food] = Field(title="먹은 음식")
    open: int = Field(title="공개 여부", description="0 or 1")

    # class Config:
    #     schema_extra: {
    #         "example": {
    #             "image_url": "www.abcd",
    #             "meal_time": "L",
    #             "date": "2023-04-26",
    #             "foods": [{"food_id": 123, "image_url": "www.aacd", "weight": 200}],
    #             "open": 1,
    #         }
    #     }


class PatchFeedData(BaseModel):
    meal_time: MealTime = Field(title="식사 종류", description="B,L,D,S")
    date: str = Field(title="식사 날짜")
    foods: List[Food] = Field(title="먹은 음식들")
    open: int = Field(title="공개 여부", description="0 or 1")
