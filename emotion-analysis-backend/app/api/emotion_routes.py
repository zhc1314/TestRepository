from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.emotion import (
    EmotionAnalysisRequest,
    EmotionAnalysisResponse,
    EmotionRecordResponse,
    EmotionStatisticsResponse
)
from app.services.emotion_service import emotion_service
import aiofiles
import os
from pathlib import Path

router = APIRouter()

@router.post("/emotion/analyze", response_model=EmotionAnalysisResponse)
async def analyze_emotion(
    request: EmotionAnalysisRequest,
    db: Session = Depends(get_db)
):
    """
    分析文本情绪
    
    - **user_id**: 用户ID
    - **text**: 待分析的文本内容
    """
    try:
        result = await emotion_service.analyze_text_emotion(
            db=db,
            user_id=request.user_id,
            text=request.text
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"情绪分析失败: {str(e)}")

@router.post("/emotion/analyze-file", response_model=EmotionAnalysisResponse)
async def analyze_emotion_from_file(
    user_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    分析上传文件中的情绪
    
    - **user_id**: 用户ID
    - **file**: 上传的文本文件（支持txt, doc, docx, pdf）
    """
    # 检查文件类型
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in [".txt", ".doc", ".docx", ".pdf"]:
        raise HTTPException(status_code=400, detail="不支持的文件格式")
    
    try:
        # 读取文件内容
        content = await file.read()
        
        # 简单处理：只处理txt文件
        if file_ext == ".txt":
            text_content = content.decode("utf-8")
        else:
            # 其他格式需要额外的库处理，这里先提示
            raise HTTPException(
                status_code=400,
                detail="目前仅支持.txt文件，其他格式需要安装额外依赖"
            )
        
        # 保存文件（可选）
        upload_dir = Path("uploads")
        upload_dir.mkdir(exist_ok=True)
        file_path = upload_dir / f"{user_id}_{file.filename}"
        
        async with aiofiles.open(file_path, "wb") as f:
            await f.write(content)
        
        # 分析情绪
        result = await emotion_service.analyze_file_emotion(
            db=db,
            user_id=user_id,
            file_content=text_content,
            file_path=str(file_path)
        )
        
        return result
    
    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="文件编码错误，请使用UTF-8编码")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"文件处理失败: {str(e)}")

@router.get("/emotion/history/{user_id}", response_model=List[EmotionRecordResponse])
def get_emotion_history(
    user_id: int,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """
    获取用户的情绪历史记录
    
    - **user_id**: 用户ID
    - **limit**: 返回记录数量（默认10条）
    """
    try:
        records = emotion_service.get_user_emotion_history(
            db=db,
            user_id=user_id,
            limit=limit
        )
        return records
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取历史记录失败: {str(e)}")

@router.get("/emotion/statistics/{user_id}", response_model=EmotionStatisticsResponse)
def get_emotion_statistics(
    user_id: int,
    days: int = 7,
    db: Session = Depends(get_db)
):
    """
    获取用户的情绪统计数据
    
    - **user_id**: 用户ID
    - **days**: 统计天数（默认7天）
    """
    try:
        stats = emotion_service.get_emotion_statistics(
            db=db,
            user_id=user_id,
            days=days
        )
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取统计数据失败: {str(e)}")