# AI学习规划智能体 - 考研助手

## 项目简介
基于AI的考研学习规划系统，通过用户画像采集和智能对话，为考研学生提供个性化学习规划建议。

## 技术栈

### 后端
- Python 3.9+
- FastAPI (Web框架)
- SQLAlchemy (ORM)
- MySQL 8.0+
- Pydantic (数据验证)
- python-dotenv (环境变量管理)

### 前端
- Vue 3
- TypeScript
- Element Plus (UI组件库)
- Axios (HTTP客户端)
- Vue Router (路由管理)
- Pinia (状态管理)

## 项目结构

```
ai-study-planner/
├── backend/              # 后端服务
│   ├── app/
│   │   ├── api/         # API路由
│   │   ├── core/        # 核心配置
│   │   ├── models/      # 数据库模型
│   │   ├── schemas/     # Pydantic模型
│   │   ├── services/    # 业务逻辑
│   │   └── main.py      # 应用入口
│   ├── requirements.txt
│   └── .env.example
├── frontend/            # 前端应用
│   ├── src/
│   │   ├── components/  # 组件
│   │   ├── views/       # 页面视图
│   │   ├── router/      # 路由配置
│   │   ├── store/       # 状态管理
│   │   ├── api/         # API接口
│   │   └── App.vue
│   └── package.json
└── README.md
```

## 核心功能模块

### 1. 用户画像与基础信息采集
- 目标院校/专业信息
- 备考时间规划
- 基础能力评估
- 学习偏好设置

### 2. AI对话交互（框架预留）
- 智能对话界面
- 学习规划咨询
- 个性化建议生成

## 快速开始

### 后端启动
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### 前端启动
```bash
cd frontend
npm install
npm run dev
```

## 数据库设计

### 用户画像表 (user_profiles)
- 基本信息
- 目标设置
- 备考计划
- 基础评估
- 学习偏好

## AI集成（待实现）
- 大模型API调用接口预留
- 智能体工作流框架
- 提示词工程模块