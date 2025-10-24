from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from ..core.database import get_db
from ..models.user_profile import UserProfile
from ..services.ai_service import AIService

router = APIRouter(
    prefix="/api/chat",
    tags=["AI对话"]
)


class ChatMessage(BaseModel):
    """聊天消息模型"""
    role: str  # user or assistant
    content: str


class ChatRequest(BaseModel):
    """聊天请求模型"""
    user_id: str
    message: str
    history: Optional[List[ChatMessage]] = []


class ChatResponse(BaseModel):
    """聊天响应模型"""
    message: str
    timestamp: str


@router.post("/", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    db: Session = Depends(get_db)
):
    """AI对话接口"""
    try:
        # 获取用户画像信息
        user_profile = None
        if request.user_id:
            user_profile = db.query(UserProfile).filter(
                UserProfile.user_id == request.user_id
            ).first()
        
        # 构建消息历史
        messages = []
        if request.history:
            for msg in request.history:
                messages.append({
                    "role": msg.role,
                    "content": msg.content
                })
        
        # 添加当前用户消息
        messages.append({
            "role": "user",
            "content": request.message
        })
        
        # 调用AI服务(传递数据库会话以启用知识库检索)
        ai_service = AIService(db)
        response_content = await ai_service.chat(
            messages=messages,
            user_profile=user_profile,
            user_id=request.user_id,
            enable_knowledge_base=True
        )
        
        return ChatResponse(
            message=response_content,
            timestamp=datetime.now().isoformat()
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"对话处理失败: {str(e)}")


@router.get("/history/{user_id}")
async def get_chat_history(
    user_id: str,
    db: Session = Depends(get_db)
):
    """获取用户的聊天历史
    
    注意: 当前版本暂未实现历史存储,返回空列表
    TODO: 后续可考虑将对话历史存储到数据库
    """
    # 临时返回空历史
    return {"user_id": user_id, "history": []}