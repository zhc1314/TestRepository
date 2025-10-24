# 知识库框架使用指南

## 概述

本项目已集成知识库框架，支持将考研相关知识内容存储到知识库中，AI在回答用户问题时会自动检索相关知识进行参考。

## 架构设计

### 数据模型

#### 1. KnowledgeDocument (知识文档)
- **用途**: 存储完整的知识文档
- **字段**:
  - `id`: 文档唯一标识
  - `title`: 文档标题
  - `content`: 文档完整内容
  - `category`: 分类(如: politics, english, math, major等)
  - `tags`: 标签列表(JSON格式)
  - `is_active`: 是否启用
  - `created_at`: 创建时间
  - `updated_at`: 更新时间

#### 2. KnowledgeChunk (知识切片)
- **用途**: 存储文档的分块内容，用于向量检索
- **字段**:
  - `id`: 切片唯一标识
  - `document_id`: 所属文档ID
  - `content`: 切片内容(通常500-1000字)
  - `chunk_index`: 在文档中的序号
  - `embedding`: 向量表示(预留字段，需配置向量数据库)
  - `metadata`: 额外元数据(JSON格式)

#### 3. SearchHistory (检索历史)
- **用途**: 记录用户的知识库检索历史
- **字段**:
  - `id`: 记录唯一标识
  - `user_id`: 用户ID
  - `query`: 检索查询
  - `results`: 检索结果(JSON格式)
  - `created_at`: 检索时间

### 服务层

#### KnowledgeService (知识库服务)

主要功能模块:

1. **文档管理**
   - `add_document()`: 添加新文档
   - `update_document()`: 更新文档
   - `delete_document()`: 删除文档
   - `get_document()`: 查询单个文档
   - `get_documents()`: 查询文档列表

2. **文档向量化** (预留接口)
   - `_chunk_text()`: 文本切分
   - `_generate_embeddings()`: 生成向量表示
   - `_store_embeddings()`: 存储向量

3. **知识检索**
   - `search_knowledge()`: 语义检索
   - `_record_search()`: 记录检索历史

4. **RAG集成**
   - `get_context_for_chat()`: 为对话获取知识上下文

### API接口

#### 知识库管理接口 (`/api/knowledge`)

1. **创建文档**
   ```http
   POST /api/knowledge/documents/
   Content-Type: application/json
   
   {
     "title": "考研政治马原知识点",
     "content": "文档内容...",
     "category": "politics",
     "tags": ["马原", "哲学"],
     "is_active": true
   }
   ```

2. **获取文档列表**
   ```http
   GET /api/knowledge/documents/?category=politics&is_active=true&skip=0&limit=10
   ```

3. **获取单个文档**
   ```http
   GET /api/knowledge/documents/{document_id}
   ```

4. **更新文档**
   ```http
   PUT /api/knowledge/documents/{document_id}
   Content-Type: application/json
   
   {
     "title": "更新后的标题",
     "content": "更新后的内容",
     "is_active": true
   }
   ```

5. **删除文档**
   ```http
   DELETE /api/knowledge/documents/{document_id}
   ```

6. **搜索知识库**
   ```http
   POST /api/knowledge/search/
   Content-Type: application/json
   
   {
     "query": "马克思主义哲学的核心概念",
     "top_k": 5,
     "category": "politics"
   }
   ```

7. **上传文档文件**
   ```http
   POST /api/knowledge/upload/
   Content-Type: multipart/form-data
   
   file: [选择文本文件]
   category: politics
   tags: 马原,哲学
   ```

## 集成说明

### AI对话集成

AI服务已自动集成知识库检索功能:

1. **自动检索**: 当用户发送消息时，系统会自动从知识库中检索相关内容
2. **上下文注入**: 检索到的知识会作为上下文注入到AI对话中
3. **可控开关**: 可通过`enable_knowledge_base`参数控制是否启用

```python
# 在chat.py中的使用示例
response_content = await ai_service.chat(
    messages=messages,
    user_profile=user_profile,
    user_id=request.user_id,
    enable_knowledge_base=True  # 启用知识库检索
)
```

### 知识库工作流程

1. **添加知识**
   ```
   用户上传/创建文档 → 文档存储到数据库 → 自动切分为chunks → 生成向量(预留) → 存储到向量数据库(预留)
   ```

2. **对话检索**
   ```
   用户提问 → 提取用户消息 → 向量检索相关chunks → 组装知识上下文 → 注入AI对话 → 生成回复
   ```

## 后续扩展

### 1. 向量数据库集成

当前框架已预留向量存储接口，推荐集成方案:

- **Pinecone**: 云端向量数据库
- **Weaviate**: 开源向量数据库
- **Milvus**: 高性能向量数据库
- **ChromaDB**: 轻量级向量数据库

需要实现的方法:
```python
async def _generate_embeddings(self, text: str) -> List[float]:
    """生成文本的向量表示"""
    # TODO: 调用embedding模型API
    # 推荐: OpenAI text-embedding-ada-002 或 阿里云text-embedding-v2
    pass

async def _store_embeddings(self, chunk_id: str, embedding: List[float]):
    """存储向量到向量数据库"""
    # TODO: 调用向量数据库API
    pass
```

### 2. 文本切分优化

当前使用简单的字符数切分，可优化为:
- 基于语义的智能切分
- 保留段落完整性
- 处理代码块和公式

### 3. 检索策略优化

- 混合检索(向量检索 + 关键词检索)
- 重排序(Reranking)
- 检索结果去重
- 根据用户画像调整检索权重

### 4. 知识更新机制

- 定时更新考研大纲变化
- 增量更新机制
- 版本控制

## 使用示例

### Python示例: 添加考研知识

```python
import httpx

# 创建政治知识文档
async def add_politics_knowledge():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/api/knowledge/documents/",
            json={
                "title": "马克思主义基本原理-唯物辩证法",
                "content": """
                唯物辩证法的核心内容:
                
                1. 三大规律:
                - 对立统一规律(矛盾规律):事物内部矛盾双方的对立统一推动事物发展
                - 质量互变规律:量变积累到一定程度必然引起质变
                - 否定之否定规律:事物发展是螺旋式上升的过程
                
                2. 五对范畴:
                - 原因和结果
                - 必然性和偶然性  
                - 可能性和现实性
                - 内容和形式
                - 本质和现象
                
                重点考点:
                - 矛盾的同一性和斗争性
                - 矛盾的普遍性和特殊性
                - 量变和质变的辩证关系
                """,
                "category": "politics",
                "tags": ["马原", "唯物辩证法", "哲学"],
                "is_active": True
            }
        )
        print(response.json())

# 搜索知识
async def search_politics():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/api/knowledge/search/",
            json={
                "query": "矛盾的普遍性和特殊性",
                "top_k": 3,
                "category": "politics"
            }
        )
        results = response.json()
        for item in results["results"]:
            print(f"文档: {item['document_title']}")
            print(f"内容: {item['chunk_content']}")
            print(f"相关度: {item['relevance_score']}")
            print("-" * 50)
```

### 前端示例: 上传知识文件

```javascript
// 上传考研资料文件
async function uploadKnowledgeFile(file, category) {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('category', category);
  formData.append('tags', '考研,重点');
  
  const response = await fetch('http://localhost:8000/api/knowledge/upload/', {
    method: 'POST',
    body: formData
  });
  
  const result = await response.json();
  console.log('上传成功:', result);
}
```

## 数据准备建议

### 知识库分类

1. **politics** (政治)
   - 马原、毛概、史纲、思修各部分知识点
   - 时政热点
   - 答题模板

2. **english** (英语)
   - 词汇记忆技巧
   - 语法知识点
   - 阅读理解方法
   - 写作模板

3. **math** (数学)
   - 高数公式定理
   - 线代知识点
   - 概率统计方法
   - 解题技巧

4. **major** (专业课)
   - 按具体专业分类
   - 核心概念
   - 历年真题分析

5. **strategy** (备考策略)
   - 时间规划
   - 复习方法
   - 心理调节
   - 经验分享

### 内容组织建议

1. **结构化**: 使用清晰的标题和列表
2. **重点标注**: 标记核心考点
3. **案例说明**: 添加例题和解析
4. **定期更新**: 跟随考研大纲变化

## 注意事项

1. **性能优化**: 大量文档需要考虑分页和缓存
2. **权限控制**: 后续可添加文档访问权限
3. **内容审核**: 确保知识库内容的准确性
4. **向量成本**: 向量生成和存储会产生API调用成本
5. **检索质量**: 需要持续优化检索策略和参数

## 常见问题

### Q1: 如何禁用某个文档?
A: 使用更新接口，设置`is_active: false`

### Q2: 知识库检索失败会影响AI对话吗?
A: 不会，检索失败时AI会继续基于系统提示词和用户画像进行回复

### Q3: 支持哪些文件格式?
A: 当前支持UTF-8编码的文本文件(.txt, .md等)，后续可扩展支持PDF、Word等

### Q4: 如何批量导入知识?
A: 可以编写脚本调用API批量创建文档，或使用上传接口逐个上传文件

## 总结

知识库框架已完成基础架构搭建，包括:
- ✅ 数据模型定义
- ✅ 服务层接口
- ✅ API接口
- ✅ AI对话集成
- 🔲 向量数据库集成(待扩展)
- 🔲 Embedding生成(待扩展)

您可以开始添加考研知识内容，系统会在用户提问时自动检索并参考这些知识进行回复。