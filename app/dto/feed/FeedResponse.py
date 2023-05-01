from pydantic import BaseModel, Field
from typing import List
from app.dto.feed.FeedRequest import Food, MealTimeEnum, GoalEnum


class FeedData(BaseModel):
    feed_id: int = Field(..., title="피드 ID")
    user_id: int = Field(..., title="작성자 ID")
    image_url: str = Field(..., title="전체 이미지 URL")
    user_name: str = Field(..., title="작성자 이름")
    meal_time: MealTimeEnum = Field(..., title="식사 종류", description="B,L,D,S")
    date: str = Field(..., title="식사 날짜")
    likes: int = Field(..., title="좋아요 수")
    kcal: float = Field(..., title="전체 열량")
    carbohydrate: float = Field(..., title="전체 탄수화물")
    protein: float = Field(..., title="전체 단백질")
    fat: float = Field(..., title="전체 지방")
    foods: List[Food] = Field(..., title="먹은 음식들")
    created_at: str = Field(..., title="생성 일자")
    updated_at: str = Field(..., title="수정 일자")
    open: bool = Field(..., title="공개 여부", description="True or False")
    goal: GoalEnum = Field(..., title="피드 카테고리")
    my_like: bool = Field(..., title="좋아요 여부", description="True or False")

    class Config:
        orm_mode = True
