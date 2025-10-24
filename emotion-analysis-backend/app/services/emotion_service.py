from sqlalchemy.orm import Session
from typing import Dict, List, Optional
from app.models.emotion import EmotionRecord, EmotionType
from app.services.ai_service import ai_service
from datetime import datetime, timedelta

class EmotionService:
    """情绪分析服务"""
    
    async def analyze_text_emotion(self, db: Session, user_id: int, text: str) -> EmotionRecord:
        """
        分析文本情绪并保存记录
        
        Args:
            db: 数据库会话
            user_id: 用户ID
            text: 待分析的文本
            
        Returns:
            情绪记录对象
        """
        # 调用AI服务分析情绪
        ai_result = await ai_service.analyze_emotion(text)
        
        # 创建情绪记录
        emotion_record = EmotionRecord(
            user_id=user_id,
            input_text=text,
            input_type="text",
            emotion_type=EmotionType(ai_result.get("emotion_type", "neutral")),
            emotion_score=ai_result.get("emotion_score", 0.5),
            analysis_result=ai_result.get("analysis", ""),
            suggestions=ai_result.get("suggestions", "")
        )
        
        # 保存到数据库
        db.add(emotion_record)
        db.commit()
        db.refresh(emotion_record)
        
        return emotion_record
    
    async def analyze_file_emotion(self, db: Session, user_id: int, file_content: str, file_path: str) -> EmotionRecord:
        """
        分析文件中的情绪内容
        
        Args:
            db: 数据库会话
            user_id: 用户ID
            file_content: 文件内容
            file_path: 文件路径
            
        Returns:
            情绪记录对象
        """
        # 调用AI服务分析情绪
        ai_result = await ai_service.analyze_emotion(file_content)
        
        # 创建情绪记录
        emotion_record = EmotionRecord(
            user_id=user_id,
            input_text=file_content,
            input_type="file",
            file_path=file_path,
            emotion_type=EmotionType(ai_result.get("emotion_type", "neutral")),
            emotion_score=ai_result.get("emotion_score", 0.5),
            analysis_result=ai_result.get("analysis", ""),
            suggestions=ai_result.get("suggestions", "")
        )
        
        # 保存到数据库
        db.add(emotion_record)
        db.commit()
        db.refresh(emotion_record)
        
        return emotion_record
    
    def get_user_emotion_history(self, db: Session, user_id: int, limit: int = 10) -> List[EmotionRecord]:
        """
        获取用户的情绪历史记录
        
        Args:
            db: 数据库会话
            user_id: 用户ID
            limit: 返回记录数量
            
        Returns:
            情绪记录列表
        """
        return db.query(EmotionRecord).filter(
            EmotionRecord.user_id == user_id
        ).order_by(
            EmotionRecord.created_at.desc()
        ).limit(limit).all()
    
    def get_emotion_statistics(self, db: Session, user_id: int, days: int = 7) -> Dict:
        """
        获取用户的情绪统计数据
        
        Args:
            db: 数据库会话
            user_id: 用户ID
            days: 统计天数
            
        Returns:
            统计数据字典
        """
        start_date = datetime.now() - timedelta(days=days)
        
        records = db.query(EmotionRecord).filter(
            EmotionRecord.user_id == user_id,
            EmotionRecord.created_at >= start_date
        ).all()
        
        if not records:
            return {
                "total_records": 0,
                "emotion_distribution": {},
                "average_score": 0.0
            }
        
        # 统计情绪分布
        emotion_count = {}
        total_score = 0.0
        
        for record in records:
            emotion_type = record.emotion_type.value if record.emotion_type else "neutral"
            emotion_count[emotion_type] = emotion_count.get(emotion_type, 0) + 1
            total_score += record.emotion_score or 0.0
        
        return {
            "total_records": len(records),
            "emotion_distribution": emotion_count,
            "average_score": total_score / len(records) if records else 0.0,
            "days": days
        }

# 单例模式
emotion_service = EmotionService()