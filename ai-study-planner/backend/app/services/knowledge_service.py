from typing import List, Dict, Optional, Tuple, Any
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
import json
from datetime import datetime

from ..models.knowledge_base import KnowledgeDocument, KnowledgeChunk, SearchHistory


class KnowledgeService:
    """知识库服务 - 处理文档管理、向量检索和RAG集成"""
    
    def __init__(self, db: Session):
        self.db = db
        # TODO: 后续集成向量数据库客户端(如Milvus、Qdrant、Chroma等)
        self.vector_db = None
        # TODO: 后续集成embedding模型(如OpenAI embeddings、本地模型等)
        self.embedding_model = None
    
    # ==================== 文档管理 ====================
    
    async def add_document(
        self,
        title: str,
        content: str,
        category: str,
        sub_category: Optional[str] = None,
        summary: Optional[str] = None,
        keywords: Optional[List[str]] = None,
        source: Optional[str] = None,
        author: Optional[str] = None,
        difficulty_level: Optional[str] = None,
        applicable_stage: Optional[str] = None
    ) -> KnowledgeDocument:
        """
        添加知识库文档
        
        Args:
            title: 文档标题
            content: 文档内容
            category: 文档分类(政治/英语/数学/专业课/备考方法等)
            sub_category: 子分类
            summary: 文档摘要
            keywords: 关键词列表
            source: 来源
            author: 作者
            difficulty_level: 难度等级(基础/中等/困难)
            applicable_stage: 适用备考阶段(基础期/强化期/冲刺期)
        
        Returns:
            创建的文档对象
        """
        document = KnowledgeDocument(
            title=title,
            content=content,
            category=category,
            sub_category=sub_category,
            summary=summary,
            keywords=keywords,
            source=source,
            author=author,
            difficulty_level=difficulty_level,
            applicable_stage=applicable_stage,
            is_vectorized=0
        )
        
        self.db.add(document)
        self.db.commit()
        self.db.refresh(document)
        
        # TODO: 异步触发文档向量化任务
        # await self._vectorize_document(document.id)
        
        return document
    
    async def update_document(
        self,
        document_id: int,
        **kwargs
    ) -> Optional[KnowledgeDocument]:
        """
        更新知识库文档
        
        Args:
            document_id: 文档ID
            **kwargs: 要更新的字段
        
        Returns:
            更新后的文档对象
        """
        document = self.db.query(KnowledgeDocument).filter(
            KnowledgeDocument.id == document_id
        ).first()
        
        if not document:
            return None
        
        for key, value in kwargs.items():
            if hasattr(document, key):
                setattr(document, key, value)
        
        # 如果内容发生变化,重新向量化
        if 'content' in kwargs:
            document.is_vectorized = 0
            # TODO: 异步触发文档重新向量化任务
            # await self._vectorize_document(document_id)
        
        self.db.commit()
        self.db.refresh(document)
        
        return document
    
    async def delete_document(self, document_id: int) -> bool:
        """
        删除知识库文档及其关联的chunks
        
        Args:
            document_id: 文档ID
        
        Returns:
            是否删除成功
        """
        document = self.db.query(KnowledgeDocument).filter(
            KnowledgeDocument.id == document_id
        ).first()
        
        if not document:
            return False
        
        # 删除关联的chunks
        self.db.query(KnowledgeChunk).filter(
            KnowledgeChunk.document_id == document_id
        ).delete()
        
        # TODO: 从向量数据库中删除向量
        # await self._delete_vectors(document_id)
        
        self.db.delete(document)
        self.db.commit()
        
        return True
    
    def get_document(self, document_id: int) -> Optional[KnowledgeDocument]:
        """获取文档详情"""
        return self.db.query(KnowledgeDocument).filter(
            KnowledgeDocument.id == document_id
        ).first()
    
    def list_documents(
        self,
        category: Optional[str] = None,
        difficulty_level: Optional[str] = None,
        applicable_stage: Optional[str] = None,
        skip: int = 0,
        limit: int = 50
    ) -> List[KnowledgeDocument]:
        """
        获取文档列表(支持筛选)
        
        Args:
            category: 按分类筛选
            difficulty_level: 按难度筛选
            applicable_stage: 按备考阶段筛选
            skip: 跳过记录数
            limit: 返回记录数
        
        Returns:
            文档列表
        """
        query = self.db.query(KnowledgeDocument)
        
        if category:
            query = query.filter(KnowledgeDocument.category == category)
        if difficulty_level:
            query = query.filter(KnowledgeDocument.difficulty_level == difficulty_level)
        if applicable_stage:
            query = query.filter(KnowledgeDocument.applicable_stage == applicable_stage)
        
        return query.offset(skip).limit(limit).all()
    
    # ==================== 文档向量化 ====================
    
    async def _vectorize_document(self, document_id: int):
        """
        将文档切分并向量化(私有方法)
        
        流程:
        1. 获取文档内容
        2. 文本切分(chunk)
        3. 为每个chunk生成embedding
        4. 存储到向量数据库
        5. 更新文档向量化状态
        
        TODO: 实现具体的向量化逻辑
        """
        document = self.get_document(document_id)
        if not document:
            return
        
        # TODO: 实现文本切分策略
        # chunks = self._split_text(document.content)
        
        # TODO: 为每个chunk生成embedding
        # embeddings = await self._generate_embeddings(chunks)
        
        # TODO: 存储到向量数据库
        # await self._store_vectors(document_id, chunks, embeddings)
        
        # 更新文档向量化状态
        document.is_vectorized = 1
        # document.chunk_count = len(chunks)
        self.db.commit()
    
    def _split_text(
        self,
        text: str,
        chunk_size: int = 500,
        chunk_overlap: int = 100
    ) -> List[str]:
        """
        文本切分策略
        
        Args:
            text: 待切分文本
            chunk_size: 每个chunk的字符数
            chunk_overlap: chunk之间的重叠字符数
        
        Returns:
            切分后的文本列表
        
        TODO: 实现更智能的切分策略(如按段落、句子边界切分)
        """
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end]
            chunks.append(chunk)
            start = end - chunk_overlap
        
        return chunks
    
    async def _generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        生成文本向量
        
        Args:
            texts: 文本列表
        
        Returns:
            向量列表
        
        TODO: 集成embedding模型(OpenAI/本地模型)
        """
        # 示例:使用OpenAI embeddings API
        # embeddings = []
        # for text in texts:
        #     response = await openai.Embeddings.create(
        #         model="text-embedding-ada-002",
        #         input=text
        #     )
        #     embeddings.append(response['data'][0]['embedding'])
        # return embeddings
        
        raise NotImplementedError("Embedding generation not implemented yet")
    
    async def _store_vectors(
        self,
        document_id: int,
        chunks: List[str],
        embeddings: List[List[float]]
    ):
        """
        存储向量到向量数据库
        
        Args:
            document_id: 文档ID
            chunks: 文本切片列表
            embeddings: 对应的向量列表
        
        TODO: 实现向量数据库存储逻辑
        """
        # 示例:存储到Chroma向量数据库
        # collection = self.vector_db.get_or_create_collection("knowledge_base")
        # collection.add(
        #     documents=chunks,
        #     embeddings=embeddings,
        #     metadatas=[{"document_id": document_id, "chunk_index": i} for i in range(len(chunks))],
        #     ids=[f"doc_{document_id}_chunk_{i}" for i in range(len(chunks))]
        # )
        
        raise NotImplementedError("Vector storage not implemented yet")
    
    # ==================== 知识库检索 ====================
    
    async def search(
        self,
        query: str,
        user_id: Optional[str] = None,
        category: Optional[str] = None,
        top_k: int = 5,
        min_score: float = 0.7
    ) -> List[Dict]:
        """
        知识库语义检索
        
        Args:
            query: 用户查询内容
            user_id: 用户ID(用于记录检索历史)
            category: 限定检索的分类
            top_k: 返回最相关的top_k个结果
            min_score: 最小相关性阈值
        
        Returns:
            检索结果列表,每个结果包含:
            {
                "chunk_id": chunk的ID,
                "document_id": 所属文档ID,
                "content": chunk内容,
                "score": 相关性得分,
                "metadata": 元数据(分类、难度等)
            }
        
        TODO: 实现向量检索逻辑
        """
        # TODO: 1. 将query转换为embedding
        # query_embedding = await self._generate_embeddings([query])
        
        # TODO: 2. 在向量数据库中检索最相似的chunks
        # results = await self.vector_db.search(
        #     query_embedding[0],
        #     top_k=top_k,
        #     filter={"category": category} if category else None
        # )
        
        # TODO: 3. 过滤低分结果
        # filtered_results = [r for r in results if r['score'] >= min_score]
        
        # 4. 记录检索历史
        if user_id:
            self._save_search_history(user_id, query, [], [])
        
        # TODO: 返回实际检索结果
        return []
    
    def _save_search_history(
        self,
        user_id: str,
        query: str,
        matched_chunks: List[int],
        scores: List[float]
    ):
        """保存检索历史"""
        history = SearchHistory(
            user_id=user_id,
            query=query,
            matched_chunks=matched_chunks,
            relevance_scores=scores
        )
        self.db.add(history)
        self.db.commit()
    
    # ==================== RAG集成 ====================
    
    async def get_context_for_chat(
        self,
        user_message: str,
        user_id: Optional[str] = None,
        max_context_length: int = 2000
    ) -> str:
        """
        为对话获取相关知识库上下文
        
        Args:
            user_message: 用户消息
            user_id: 用户ID
            max_context_length: 最大上下文长度(字符数)
        
        Returns:
            格式化的知识库上下文字符串
        """
        # 检索相关知识
        search_results = await self.search(
            query=user_message,
            user_id=user_id,
            top_k=3
        )
        
        if not search_results:
            return ""
        
        # 构建上下文字符串
        context_parts = ["【知识库参考】"]
        current_length = 0
        
        for i, result in enumerate(search_results, 1):
            chunk_text = f"\n参考{i}: {result['content']}"
            
            if current_length + len(chunk_text) > max_context_length:
                break
            
            context_parts.append(chunk_text)
            current_length += len(chunk_text)
        
        return "\n".join(context_parts)
    
    # ==================== 批量导入 ====================
    
    async def batch_import_documents(
        self,
        documents: List[Dict[str, Any]]
    ) -> List[str]:
        """
        批量导入文档
        
        Args:
            documents: 文档列表,每个文档包含title, content, category等字段
            
        Returns:
            创建的文档ID列表
        """
        document_ids = []
        
        for doc_data in documents:
            try:
                document = await self.add_document(
                    title=doc_data.get("title", "未命名文档"),
                    content=doc_data["content"],
                    category=doc_data.get("category"),
                    sub_category=doc_data.get("sub_category"),
                    summary=doc_data.get("summary"),
                    keywords=doc_data.get("keywords"),
                    source=doc_data.get("source"),
                    author=doc_data.get("author"),
                    difficulty_level=doc_data.get("difficulty_level"),
                    applicable_stage=doc_data.get("applicable_stage")
                )
                document_ids.append(document.id)
            except Exception as e:
                print(f"导入文档失败: {doc_data.get('title', 'unknown')}, 错误: {str(e)}")
                continue
        
        return document_ids