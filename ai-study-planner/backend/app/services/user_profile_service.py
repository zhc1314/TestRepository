from sqlalchemy.orm import Session
from datetime import datetime
from ..models.user_profile import UserProfile
from ..schemas.user_profile import UserProfileCreate, UserProfileUpdate
from typing import Optional


class UserProfileService:
    """用户画像服务"""
    
    @staticmethod
    def create_profile(db: Session, profile_data: UserProfileCreate) -> UserProfile:
        """创建用户画像"""
        # 计算剩余备考天数
        remaining_days = None
        if profile_data.exam_date and profile_data.study_start_date:
            remaining_days = (profile_data.exam_date - profile_data.study_start_date).days
        
        db_profile = UserProfile(
            **profile_data.model_dump(),
            remaining_days=remaining_days
        )
        db.add(db_profile)
        db.commit()
        db.refresh(db_profile)
        return db_profile
    
    @staticmethod
    def get_profile_by_user_id(db: Session, user_id: str) -> Optional[UserProfile]:
        """根据用户ID获取画像"""
        return db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
    
    @staticmethod
    def get_profile_by_id(db: Session, profile_id: int) -> Optional[UserProfile]:
        """根据画像ID获取"""
        return db.query(UserProfile).filter(UserProfile.id == profile_id).first()
    
    @staticmethod
    def update_profile(db: Session, user_id: str, profile_data: UserProfileUpdate) -> Optional[UserProfile]:
        """更新用户画像"""
        db_profile = UserProfileService.get_profile_by_user_id(db, user_id)
        if not db_profile:
            return None
        
        # 更新字段
        update_data = profile_data.model_dump(exclude_unset=True)
        
        # 重新计算剩余备考天数
        if 'exam_date' in update_data or 'study_start_date' in update_data:
            exam_date = update_data.get('exam_date', db_profile.exam_date)
            study_start_date = update_data.get('study_start_date', db_profile.study_start_date)
            if exam_date and study_start_date:
                update_data['remaining_days'] = (exam_date - study_start_date).days
        
        for field, value in update_data.items():
            setattr(db_profile, field, value)
        
        db.commit()
        db.refresh(db_profile)
        return db_profile
    
    @staticmethod
    def delete_profile(db: Session, user_id: str) -> bool:
        """删除用户画像"""
        db_profile = UserProfileService.get_profile_by_user_id(db, user_id)
        if not db_profile:
            return False
        
        db.delete(db_profile)
        db.commit()
        return True