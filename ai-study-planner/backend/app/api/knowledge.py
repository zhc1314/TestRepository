from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from ..core.database import get_db
from ..services.knowledge_service import KnowledgeService
from ..models.knowledge_base import KnowledgeDocument

router = APIRouter(
    prefix="/api/knowledge",
    tags=["知识库管理"]
)


class DocumentCreate(BaseModel):
    """创建文档请求模型"""
    title: str
    content: str
    category: str
    tags: Optional[List[str]] = []
    is_active: bool = True


class DocumentUpdate(BaseModel):
    """更新文档请求模型"""
    title: Optional[str] = None
    content: Optional[str] = None
    category: Optional[str] = None
    tags: Optional[List[str]] = None
    is_active: Optional[bool] = None


class DocumentResponse(BaseModel):
    """文档响应模型"""
    id: str
    title: str
    category: str
    tags: List[str]
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class SearchRequest(BaseModel):
    """知识库搜索请求"""
    query: str
    top_k: int = 5
    category: Optional[str] = None


class SearchResultItem(BaseModel):
    """搜索结果项"""
    document_id: str
    document_title: str
    chunk_content: str
    relevance_score: float


class SearchResponse(BaseModel):
    """搜索响应"""
    results: List[SearchResultItem]
    total: int


@router.post("/documents/", response_model=DocumentResponse)
async def create_document(
    doc: DocumentCreate,
    db: Session = Depends(get_db)
):
    """创建知识库文档"""
    try:
        knowledge_service = KnowledgeService(db)
        document = await knowledge_service.add_document(
            title=doc.title,
            content=doc.content,
            category=doc.category,
            tags=doc.tags,
            is_active=doc.is_active
        )
        return document
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"创建文档失败: {str(e)}")


@router.get("/documents/", response_model=List[DocumentResponse])
async def list_documents(
    category: Optional[str] = None,
    is_active: Optional[bool] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """获取文档列表"""
    try:
        knowledge_service = KnowledgeService(db)
        documents = knowledge_service.get_documents(
            category=category,
            is_active=is_active,
            skip=skip,
            limit=limit
        )
        return documents
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取文档列表失败: {str(e)}")


@router.get("/documents/{document_id}", response_model=DocumentResponse)
async def get_document(
    document_id: str,
    db: Session = Depends(get_db)
):
    """获取单个文档详情"""
    try:
        knowledge_service = KnowledgeService(db)
        document = knowledge_service.get_document(document_id)
        if not document:
            raise HTTPException(status_code=404, detail="文档不存在")
        return document
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取文档失败: {str(e)}")


@router.put("/documents/{document_id}", response_model=DocumentResponse)
async def update_document(
    document_id: str,
    doc_update: DocumentUpdate,
    db: Session = Depends(get_db)
):
    """更新文档"""
    try:
        knowledge_service = KnowledgeService(db)
        document = await knowledge_service.update_document(
            document_id=document_id,
            **doc_update.model_dump(exclude_unset=True)
        )
        if not document:
            raise HTTPException(status_code=404, detail="文档不存在")
        return document
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"更新文档失败: {str(e)}")


@router.delete("/documents/{document_id}")
async def delete_document(
    document_id: str,
    db: Session = Depends(get_db)
):
    """删除文档"""
    try:
        knowledge_service = KnowledgeService(db)
        success = knowledge_service.delete_document(document_id)
        if not success:
            raise HTTPException(status_code=404, detail="文档不存在")
        return {"message": "文档删除成功"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"删除文档失败: {str(e)}")


@router.post("/search/", response_model=SearchResponse)
async def search_knowledge(
    search_req: SearchRequest,
    db: Session = Depends(get_db)
):
    """搜索知识库"""
    try:
        knowledge_service = KnowledgeService(db)
        results = await knowledge_service.search_knowledge(
            query=search_req.query,
            top_k=search_req.top_k,
            category=search_req.category
        )
        
        search_results = [
            SearchResultItem(
                document_id=r["document_id"],
                document_title=r["document_title"],
                chunk_content=r["chunk_content"],
                relevance_score=r["score"]
            )
            for r in results
        ]
        
        return SearchResponse(
            results=search_results,
            total=len(search_results)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"搜索失败: {str(e)}")


@router.post("/upload/")
async def upload_document(
    file: UploadFile = File(...),
    category: str = "general",
    tags: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """上传文档文件(文本文件)"""
    try:
        # 读取文件内容
        content = await file.read()
        content_str = content.decode('utf-8')
        
        # 解析tags
        tag_list = []
        if tags:
            tag_list = [t.strip() for t in tags.split(',')]
        
        # 创建文档
        knowledge_service = KnowledgeService(db)
        document = await knowledge_service.add_document(
            title=file.filename,
            content=content_str,
            category=category,
            tags=tag_list
        )
        
        return {
            "message": "文档上传成功",
            "document_id": document.id,
            "title": document.title
        }
    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="文件格式不支持,请上传UTF-8编码的文本文件")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"上传失败: {str(e)}")