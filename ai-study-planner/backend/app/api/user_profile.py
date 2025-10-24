from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..schemas.user_profile import UserProfileCreate, UserProfileUpdate, UserProfileResponse
from ..services.user_profile_service import UserProfileService

router = APIRouter(
    prefix="/api/user-profile",
    tags=["用户画像"]
)


@router.post("/", response_model=UserProfileResponse, status_code=status.HTTP_201_CREATED)
def create_user_profile(
    profile_data: UserProfileCreate,
    db: Session = Depends(get_db)
):
    """创建用户画像"""
    # 检查用户是否已存在
    existing_profile = UserProfileService.get_profile_by_user_id(db, profile_data.user_id)
    if existing_profile:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="该用户画像已存在"
        )
    
    profile = UserProfileService.create_profile(db, profile_data)
    return profile


@router.get("/{user_id}", response_model=UserProfileResponse)
def get_user_profile(
    user_id: str,
    db: Session = Depends(get_db)
):
    """获取用户画像"""
    profile = UserProfileService.get_profile_by_user_id(db, user_id)
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户画像不存在"
        )
    return profile


@router.put("/{user_id}", response_model=UserProfileResponse)
def update_user_profile(
    user_id: str,
    profile_data: UserProfileUpdate,
    db: Session = Depends(get_db)
):
    """更新用户画像"""
    profile = UserProfileService.update_profile(db, user_id, profile_data)
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户画像不存在"
        )
    return profile


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_profile(
    user_id: str,
    db: Session = Depends(get_db)
):
    """删除用户画像"""
    success = UserProfileService.delete_profile(db, user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户画像不存在"
        )
    return None