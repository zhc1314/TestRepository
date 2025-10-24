import json
import os
from typing import Dict, Optional
from openai import OpenAI
from app.core.config import settings

class BaiLianAIService:
    """百炼大模型调用服务"""
    
    def __init__(self):
        self.api_key = settings.BAILILIAN_API_KEY
        self.api_url = settings.BAILILIAN_API_URL
        self.model = settings.BAILILIAN_MODEL
        # 初始化OpenAI客户端
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.api_url
        )
    
    async def analyze_emotion(self, text: str) -> Dict:
        """
        调用百炼大模型分析用户情绪
        
        Args:
            text: 用户输入的文本内容
            
        Returns:
            包含情绪分析结果的字典
        """
        print(f"\n{'='*50}")
        print(f"AI服务调用开始")
        print(f"API_KEY: {self.api_key[:20] if self.api_key else 'None'}...")
        print(f"API_URL: {self.api_url}")
        print(f"MODEL: {self.model}")
        print(f"输入文本: {text}")
        print(f"{'='*50}\n")
        
        if not self.api_key:
            print("错误: API_KEY未配置")
            return {
                "error": "API_KEY未配置",
                "emotion_type": "NEUTRAL",
                "emotion_score": 0.5,
                "analysis": "请在.env文件中配置BAILILIAN_API_KEY"
            }
        
        # 构建提示词
        prompt = self._build_emotion_analysis_prompt(text)
        
        try:
            # 使用OpenAI兼容模式调用
            messages = [
                {
                    "role": "system",
                    "content": "你是一个专业的心理咨询师和情绪分析专家,擅长分析用户的情绪状态并给出建议。"
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
            
            print(f"开始调用OpenAI兼容API...")
            print(f"Messages: {messages}")
            
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                stream=False  # 不使用流式输出,直接获取完整响应
            )
            
            print(f"API调用成功,收到响应")
            print(f"Response: {completion}")
            
            # 提取响应内容
            if completion.choices and len(completion.choices) > 0:
                content = completion.choices[0].message.content
                print(f"AI返回内容: {content}")
                return self._parse_ai_content(content)
            else:
                return {
                    "error": "API返回空响应",
                    "emotion_type": "NEUTRAL",
                    "emotion_score": 0.5,
                    "analysis": "情绪分析服务暂时不可用"
                }
                    
        except Exception as e:
            return {
                "error": str(e),
                "emotion_type": "NEUTRAL",
                "emotion_score": 0.5,
                "analysis": f"分析过程中出现错误: {str(e)}"
            }
    
    def _build_emotion_analysis_prompt(self, text: str) -> str:
        """构建情绪分析的提示词"""
        return f"""请分析以下文本中表达的情绪状态，并以JSON格式返回结果：

文本内容：
{text}

请返回以下格式的JSON：
{{
    "emotion_type": "主要情绪类型(happy/sad/angry/anxious/calm/excited/depressed/neutral)",
    "emotion_score": "情绪强度评分(0-1之间的浮点数)",
    "analysis": "详细的情绪分析说明",
    "suggestions": "针对当前情绪状态的建议"
}}
"""
    
    def _parse_ai_content(self, content: str) -> Dict:
        """解析AI返回的内容"""
        try:
            # 尝试解析JSON
            # 提取JSON部分（可能被```json包裹）
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
            
            result = json.loads(content)
            # 将emotion_type转换为大写以匹配枚举
            if "emotion_type" in result and result["emotion_type"]:
                result["emotion_type"] = result["emotion_type"].upper()
            return result
        except json.JSONDecodeError:
            return {
                "error": "JSON解析失败",
                "emotion_type": "NEUTRAL",
                "emotion_score": 0.5,
                "analysis": "AI返回的内容无法解析"
            }
        except Exception as e:
            return {
                "error": str(e),
                "emotion_type": "NEUTRAL",
                "emotion_score": 0.5,
                "analysis": "解析过程出错"
            }

# 延迟初始化,确保在导入时不会立即实例化
class _LazyAIService:
    """延迟初始化的AI服务包装器"""
    _instance = None
    
    def _get_instance(self):
        if self._instance is None:
            self._instance = BaiLianAIService()
        return self._instance
    
    async def analyze_emotion(self, text: str):
        """代理analyze_emotion方法"""
        return await self._get_instance().analyze_emotion(text)

ai_service = _LazyAIService()