from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime


class UserProfileBase(BaseModel):
    """用户画像基础模型"""
    nickname: Optional[str] = Field(None, max_length=50, description="昵称")
    target_university: Optional[str] = Field(None, max_length=100, description="目标院校")
    target_major: Optional[str] = Field(None, max_length=100, description="目标专业")
    is_cross_major: Optional[bool] = Field(False, description="是否跨考")
    major_subjects: Optional[List[str]] = Field(None, description="专业课科目列表")
    
    target_total_score: Optional[int] = Field(None, ge=0, le=500, description="目标总分")
    target_politics_score: Optional[int] = Field(None, ge=0, le=100, description="政治目标分")
    target_english_score: Optional[int] = Field(None, ge=0, le=100, description="英语目标分")
    target_math_score: Optional[int] = Field(None, ge=0, le=150, description="数学目标分")
    target_major_score: Optional[int] = Field(None, ge=0, le=300, description="专业课目标分")
    
    study_start_date: Optional[datetime] = Field(None, description="备考开始时间")
    exam_date: Optional[datetime] = Field(None, description="考试日期")
    weekday_study_hours: Optional[float] = Field(None, ge=0, le=24, description="工作日学习时长")
    weekend_study_hours: Optional[float] = Field(None, ge=0, le=24, description="周末学习时长")
    
    politics_level: Optional[str] = Field(None, description="政治基础等级")
    english_level: Optional[str] = Field(None, description="英语基础等级")
    math_level: Optional[str] = Field(None, description="数学基础等级")
    major_knowledge_score: Optional[int] = Field(None, ge=0, le=100, description="专业课测试分")
    major_knowledge_detail: Optional[Dict] = Field(None, description="知识点掌握详情")
    
    study_time_preference: Optional[str] = Field(None, description="学习时间偏好")
    study_method_preference: Optional[str] = Field(None, description="学习方法偏好")
    weak_subject_priority: Optional[List[str]] = Field(None, description="薄弱科目优先级")
    other_preferences: Optional[str] = Field(None, description="其他偏好")


class UserProfileCreate(UserProfileBase):
    """创建用户画像请求模型"""
    user_id: str = Field(..., max_length=50, description="用户ID")


class UserProfileUpdate(UserProfileBase):
    """更新用户画像请求模型"""
    pass


class UserProfileResponse(UserProfileBase):
    """用户画像响应模型"""
    id: int
    user_id: str
    remaining_days: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True