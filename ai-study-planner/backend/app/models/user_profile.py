from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Boolean, JSON
from sqlalchemy.sql import func
from ..core.database import Base


class UserProfile(Base):
    """用户画像模型"""
    __tablename__ = "user_profiles"
    
    id = Column(Integer, primary_key=True, index=True, comment="主键ID")
    
    # 基本信息
    user_id = Column(String(50), unique=True, index=True, nullable=False, comment="用户ID")
    nickname = Column(String(50), comment="昵称")
    
    # 目标院校/专业信息
    target_university = Column(String(100), comment="目标院校")
    target_major = Column(String(100), comment="目标专业")
    is_cross_major = Column(Boolean, default=False, comment="是否跨考")
    major_subjects = Column(JSON, comment="专业课科目列表")
    
    # 目标分数
    target_total_score = Column(Integer, comment="目标总分")
    target_politics_score = Column(Integer, comment="政治目标分数")
    target_english_score = Column(Integer, comment="英语目标分数")
    target_math_score = Column(Integer, comment="数学目标分数(如适用)")
    target_major_score = Column(Integer, comment="专业课目标分数")
    
    # 备考时间规划
    study_start_date = Column(DateTime, comment="备考开始时间")
    exam_date = Column(DateTime, comment="考试日期")
    weekday_study_hours = Column(Float, comment="工作日每日学习时长(小时)")
    weekend_study_hours = Column(Float, comment="周末每日学习时长(小时)")
    remaining_days = Column(Integer, comment="剩余备考天数")
    
    # 现有基础评估
    politics_level = Column(String(20), comment="政治基础等级(优秀/良好/一般/较差)")
    english_level = Column(String(20), comment="英语基础等级")
    math_level = Column(String(20), comment="数学基础等级(如适用)")
    major_knowledge_score = Column(Integer, comment="专业课入门测试分数")
    major_knowledge_detail = Column(JSON, comment="专业课知识点掌握详情")
    
    # 学习偏好
    study_time_preference = Column(String(20), comment="学习时间偏好(早起/熬夜/正常)")
    study_method_preference = Column(String(20), comment="学习方法偏好(视频课/刷题/看书)")
    weak_subject_priority = Column(JSON, comment="薄弱科目优先级列表")
    other_preferences = Column(Text, comment="其他学习偏好说明")
    
    # 时间戳
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间")
    
    def __repr__(self):
        return f"<UserProfile(user_id={self.user_id}, target_university={self.target_university})>"