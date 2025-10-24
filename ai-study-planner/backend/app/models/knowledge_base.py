from sqlalchemy import Column, Integer, String, Text, DateTime, Float, JSON, ForeignKey, Index
from sqlalchemy.sql import func
from ..core.database import Base


class KnowledgeDocument(Base):
    """知识库文档模型"""
    __tablename__ = "knowledge_documents"
    
    id = Column(Integer, primary_key=True, index=True, comment="主键ID")
    
    # 文档基本信息
    title = Column(String(200), nullable=False, comment="文档标题")
    category = Column(String(50), index=True, comment="文档分类(如:政治/英语/数学/专业课/备考方法等)")
    sub_category = Column(String(50), comment="子分类(如:政治-马原/英语-阅读技巧等)")
    
    # 文档内容
    content = Column(Text, nullable=False, comment="文档完整内容")
    summary = Column(Text, comment="文档摘要")
    keywords = Column(JSON, comment="关键词列表")
    
    # 元数据
    source = Column(String(100), comment="来源(如:官方考纲/真题解析/名师笔记等)")
    author = Column(String(100), comment="作者/来源机构")
    difficulty_level = Column(String(20), comment="难度等级(基础/中等/困难)")
    applicable_stage = Column(String(50), comment="适用备考阶段(基础期/强化期/冲刺期)")
    
    # 向量化标识
    is_vectorized = Column(Integer, default=0, comment="是否已向量化(0:未向量化 1:已向量化)")
    chunk_count = Column(Integer, default=0, comment="切分的chunk数量")
    
    # 时间戳
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间")
    
    def __repr__(self):
        return f"<KnowledgeDocument(id={self.id}, title={self.title}, category={self.category})>"


class KnowledgeChunk(Base):
    """知识库文档切片(用于向量检索)"""
    __tablename__ = "knowledge_chunks"
    
    id = Column(Integer, primary_key=True, index=True, comment="主键ID")
    
    # 关联文档
    document_id = Column(Integer, ForeignKey("knowledge_documents.id"), nullable=False, index=True, comment="所属文档ID")
    
    # 切片内容
    content = Column(Text, nullable=False, comment="切片内容")
    chunk_index = Column(Integer, nullable=False, comment="在原文档中的顺序")
    
    # 向量存储(预留字段,实际向量可能存储在专门的向量数据库中)
    embedding_model = Column(String(50), comment="使用的embedding模型名称")
    embedding_vector = Column(JSON, comment="向量表示(JSON格式存储,实际项目可能使用专门向量数据库)")
    
    # 元数据(继承自文档)
    category = Column(String(50), index=True, comment="文档分类")
    sub_category = Column(String(50), comment="子分类")
    difficulty_level = Column(String(20), comment="难度等级")
    
    # 时间戳
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    
    # 创建复合索引以优化检索性能
    __table_args__ = (
        Index('idx_category_difficulty', 'category', 'difficulty_level'),
    )
    
    def __repr__(self):
        return f"<KnowledgeChunk(id={self.id}, document_id={self.document_id}, chunk_index={self.chunk_index})>"


class SearchHistory(Base):
    """用户知识库检索历史"""
    __tablename__ = "search_history"
    
    id = Column(Integer, primary_key=True, index=True, comment="主键ID")
    
    # 用户信息
    user_id = Column(String(50), index=True, comment="用户ID")
    
    # 检索信息
    query = Column(Text, nullable=False, comment="用户查询内容")
    matched_chunks = Column(JSON, comment="匹配到的chunk ID列表")
    relevance_scores = Column(JSON, comment="各chunk的相关性得分")
    
    # 时间戳
    created_at = Column(DateTime, server_default=func.now(), comment="检索时间")
    
    def __repr__(self):
        return f"<SearchHistory(id={self.id}, user_id={self.user_id}, query={self.query[:50]})>"