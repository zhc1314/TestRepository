from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import emotion_routes
from app.core.config import settings
from app.core.database import init_db

print("="*50)
print("配置信息:")
print(f"API_KEY: {settings.BAILILIAN_API_KEY[:20] if settings.BAILILIAN_API_KEY else 'None'}...")
print(f"API_URL: {settings.BAILILIAN_API_URL}")
print(f"MODEL: {settings.BAILILIAN_MODEL}")
print("="*50)

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