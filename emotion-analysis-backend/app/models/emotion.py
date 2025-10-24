from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Enum
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum

Base = declarative_base()

class EmotionType(str, enum.Enum):
    """情绪类型枚举"""
    HAPPY = "HAPPY"  # 快乐
    SAD = "SAD"  # 悲伤
    ANGRY = "ANGRY"  # 愤怒
    ANXIOUS = "ANXIOUS"  # 焦虑
    CALM = "CALM"  # 平静
    EXCITED = "EXCITED"  # 兴奋
    DEPRESSED = "DEPRESSED"  # 抑郁
    NEUTRAL = "NEUTRAL"  # 中性

class EmotionRecord(Base):
    """情绪记录模型"""
    __tablename__ = "emotion_records"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, nullable=False, index=True, comment="用户ID")
    
    # 原始输入
    input_text = Column(Text, nullable=False, comment="用户输入的文本或日记内容")
    input_type = Column(String(20), default="text", comment="输入类型：text/file")
    file_path = Column(String(500), nullable=True, comment="上传文件路径（如有）")
    
    # AI分析结果
    emotion_type = Column(Enum(EmotionType), nullable=True, comment="识别的主要情绪类型")
    emotion_score = Column(Float, nullable=True, comment="情绪强度评分(0-1)")
    analysis_result = Column(Text, nullable=True, comment="AI分析的详细结果")
    suggestions = Column(Text, nullable=True, comment="AI给出的建议")
    
    # 元数据
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")
    
    def __repr__(self):
        return f"<EmotionRecord(id={self.id}, user_id={self.user_id}, emotion={self.emotion_type})>"