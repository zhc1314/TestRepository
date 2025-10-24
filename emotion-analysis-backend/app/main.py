from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import emotion_routes
from app.core.config import settings
from app.core.database import init_db

app = FastAPI(
    title="AI情绪分析系统",
    description="基于百炼大模型的情绪分析后端API",
    version="1.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(emotion_routes.router, prefix="/api/v1", tags=["情绪分析"])

@app.get("/")
async def root():
    return {"message": "AI情绪分析系统API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}