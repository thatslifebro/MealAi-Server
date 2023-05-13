import datetime

from pydantic import BaseModel, Field
from typing import List, Union
from app.dto.feed.FeedRequest import Food, MealTimeEnum, GoalEnum


class ReportData(BaseModel):
    feed_id: int = Field(..., title="피드 ID")
    user_id: int = Field(..., title="작성자 ID")
    image_url: Union[str, None] = Field(..., title="전체 이미지 URL")
    user_name: str = Field(..., title="작성자 이름")
    meal_time: MealTimeEnum = Field(
        ..., title="식사 종류", description="balance,lunch,dinner,snack"
    )
    date: datetime.date = Field(..., title="식사 날짜")
    likes: int = Field(..., title="좋아요 수")
    kcal: float = Field(..., title="전체 열량")
    carbohydrate: float = Field(..., title="전체 탄수화물")
    protein: float = Field(..., title="전체 단백질")
    fat: float = Field(..., title="전체 지방")
    created_at: datetime.datetime = Field(..., title="생성 일자")
    updated_at: datetime.datetime = Field(..., title="수정 일자")
    open: bool = Field(..., title="공개 여부", description="True or False")
    goal: GoalEnum = Field(..., title="피드 카테고리")
    my_like: bool = Field(..., title="좋아요 여부", description="True or False")

    class Config:
        orm_mode = True


class ReportGoal(BaseModel):
    kcal: float = Field(..., title="전체 열량")
    carbohydrate: float = Field(..., title="전체 탄수화물")
    protein: float = Field(..., title="전체 단백질")
    fat: float = Field(..., title="전체 지방")

    class Config:
        orm_mode = True


class ReportHistoryResponse(BaseModel):
    goal: ReportGoal = Field(..., title="유저의 하루 목표치")
    nutrient: List[ReportGoal] = Field(..., title="유저의 요일별 총 영양소")
    data: List[List[ReportData]] = Field(..., title="월화수목금토일 유저의 데이터")


class ReportResponse(BaseModel):
    goal: GoalEnum = Field(..., title="유저의 식단 목표")
    weekly_goal: ReportGoal = Field(..., title="유저의 주간 목표치")
    weekly_nutrient: ReportGoal = Field(..., title="유저의 주간 총 영양소")
    daily_goal: ReportGoal = Field(..., title="유저의 하루 목표치")
    daily_nutrient: List[ReportGoal] = Field(..., title="유저의 요일별 총 영양소")
    start_of_week: str
    end_of_week: str
