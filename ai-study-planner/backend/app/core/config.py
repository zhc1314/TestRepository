from pydantic_settings import BaseSettings
from pydantic import Field
from typing import List


class Settings(BaseSettings):
    """应用配置"""
    
    # 应用基础配置
    APP_NAME: str = "AI学习规划智能体"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # 数据库配置
    DATABASE_URL: str = "mysql+pymysql://root:password@localhost:3306/ai_study_planner"
    
    # 跨域配置
    CORS_ORIGINS: str = "http://localhost:5173,http://localhost:3000"
    
    # JWT配置
    SECRET_KEY: str = "your-secret-key-here-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # AI模型配置
    AI_API_KEY: str = Field(default="your-api-key-here", env="AI_API_KEY")
    AI_ENDPOINT: str = Field(default="https://api.openai.com/v1", env="AI_ENDPOINT")
    AI_MODEL_NAME: str = Field(default="gpt-3.5-turbo", env="AI_MODEL_NAME")
    AI_MAX_TOKENS: int = Field(default=2000, env="AI_MAX_TOKENS")
    AI_TEMPERATURE: float = Field(default=0.7, env="AI_TEMPERATURE")
    
    @property
    def cors_origins_list(self) -> List[str]:
        """将CORS_ORIGINS字符串转换为列表"""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()