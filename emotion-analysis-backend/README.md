# AI情绪分析系统后端

基于FastAPI和百炼大模型的情绪分析系统后端服务。

## 功能特性

- ✅ 文本情绪分析
- ✅ 日记文件上传分析
- ✅ 情绪历史记录查询
- ✅ 情绪统计数据分析
- ✅ 集成阿里云百炼大模型
- ✅ MySQL数据持久化

## 项目结构

```
emotion-analysis-backend/
├── app/
│   ├── api/                    # API路由
│   │   └── emotion_routes.py   # 情绪分析相关路由
│   ├── core/                   # 核心配置
│   │   ├── config.py          # 应用配置
│   │   └── database.py        # 数据库配置
│   ├── models/                 # 数据模型
│   │   └── emotion.py         # 情绪记录模型
│   ├── schemas/                # 数据传输对象
│   │   └── emotion.py         # 请求/响应模型
│   ├── services/               # 业务逻辑
│   │   ├── ai_service.py      # AI大模型服务
│   │   └── emotion_service.py # 情绪分析服务
│   └── main.py                 # 应用入口
├── uploads/                    # 文件上传目录
├── .env.example                # 环境变量模板
├── init.sql                    # 数据库初始化脚本
├── requirements.txt            # Python依赖
└── README.md                   # 项目说明
```

## 快速开始

### 1. 环境准备

- Python 3.8+
- MySQL 5.7+
- 阿里云百炼大模型API Key

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置环境变量

复制`.env.example`为`.env`并填写配置：

```bash
cp .env.example .env
```

编辑`.env`文件：

```env
# 数据库配置
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=emotion_analysis

# 百炼大模型API Key（从阿里云百炼平台获取）
BAILILIAN_API_KEY=your_api_key_here
```

### 4. 初始化数据库

```bash
mysql -u root -p < init.sql
```

### 5. 启动服务

```bash
cd app
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

服务将在 http://localhost:8000 启动

### 6. 查看API文档

访问 http://localhost:8000/docs 查看Swagger API文档

## API接口说明

### 1. 分析文本情绪

**POST** `/api/v1/emotion/analyze`

```json
{
  "user_id": 1,
  "text": "今天心情很好，完成了很多工作"
}
```

### 2. 分析文件情绪

**POST** `/api/v1/emotion/analyze-file`

- 参数：`user_id` (int), `file` (上传的文本文件)
- 支持格式：.txt

### 3. 获取情绪历史

**GET** `/api/v1/emotion/history/{user_id}?limit=10`

### 4. 获取情绪统计

**GET** `/api/v1/emotion/statistics/{user_id}?days=7`

## 百炼大模型集成

本项目使用阿里云百炼大模型平台进行情绪分析。

### 获取API Key

1. 访问 [阿里云百炼平台](https://dashscope.aliyun.com/)
2. 注册/登录账号
3. 在控制台创建API Key
4. 将API Key配置到`.env`文件中

### 模型配置

默认使用`qwen-max`模型，可在`config.py`中修改：

```python
BAILILIAN_MODEL: str = "qwen-max"  # 可选: qwen-turbo, qwen-plus
```

## 数据库设计

### emotion_records 表

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INT | 主键 |
| user_id | INT | 用户ID |
| input_text | TEXT | 输入文本 |
| input_type | VARCHAR | 输入类型(text/file) |
| emotion_type | ENUM | 情绪类型 |
| emotion_score | FLOAT | 情绪评分(0-1) |
| analysis_result | TEXT | 分析结果 |
| suggestions | TEXT | AI建议 |
| created_at | DATETIME | 创建时间 |

## 开发说明

### 添加新的情绪类型

在`app/models/emotion.py`的`EmotionType`枚举中添加：

```python
class EmotionType(str, Enum):
    happy = "happy"
    sad = "sad"
    # 添加新类型
    your_new_emotion = "your_new_emotion"
```

### 自定义AI提示词

在`app/services/ai_service.py`的`_build_emotion_analysis_prompt`方法中修改提示词。

## 注意事项

1. **API Key安全**：不要将API Key提交到版本控制系统
2. **文件上传**：默认限制10MB，可在配置中修改
3. **数据库连接**：确保MySQL服务正常运行
4. **生产部署**：修改SECRET_KEY和其他敏感配置

## 许可证

MIT License