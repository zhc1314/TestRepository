from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.models.emotion import EmotionType

class EmotionAnalysisRequest(BaseModel):
    """情绪分析请求模型"""
    user_id: int = Field(..., description="用户ID")
    text: str = Field(..., min_length=1, max_length=10000, description="待分析的文本内容")

class EmotionAnalysisResponse(BaseModel):
    """情绪分析响应模型"""
    id: int
    user_id: int
    emotion_type: Optional[EmotionType]
    emotion_score: Optional[float]
    analysis_result: Optional[str]
    suggestions: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True

class EmotionRecordResponse(BaseModel):
    """情绪记录响应模型"""
    id: int
    user_id: int
    input_text: str
    input_type: str
    emotion_type: Optional[EmotionType]
    emotion_score: Optional[float]
    analysis_result: Optional[str]
    suggestions: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True

class EmotionStatisticsResponse(BaseModel):
    """情绪统计响应模型"""
    total_records: int
    emotion_distribution: dict
    average_score: float
    days: int