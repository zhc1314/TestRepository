import json
import httpx
from typing import Dict, Optional
from app.core.config import settings

class BaiLianAIService:
    """百炼大模型调用服务"""
    
    def __init__(self):
        self.api_key = settings.BAILILIAN_API_KEY
        self.api_url = settings.BAILILIAN_API_URL
        self.model = settings.BAILILIAN_MODEL
    
    async def analyze_emotion(self, text: str) -> Dict:
        """
        调用百炼大模型分析用户情绪
        
        Args:
            text: 用户输入的文本内容
            
        Returns:
            包含情绪分析结果的字典
        """
        if not self.api_key:
            return {
                "error": "API_KEY未配置",
                "emotion_type": "neutral",
                "emotion_score": 0.5,
                "analysis": "请在.env文件中配置BAILILIAN_API_KEY"
            }
        
        # 构建提示词
        prompt = self._build_emotion_analysis_prompt(text)
        
        try:
            # 调用百炼大模型API
            async with httpx.AsyncClient() as client:
                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                }
                
                payload = {
                    "model": self.model,
                    "input": {
                        "messages": [
                            {
                                "role": "system",
                                "content": "你是一个专业的心理咨询师和情绪分析专家，擅长分析用户的情绪状态并给出建议。"
                            },
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ]
                    },
                    "parameters": {
                        "result_format": "message"
                    }
                }
                
                response = await client.post(
                    self.api_url,
                    headers=headers,
                    json=payload,
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    result = response.json()
                    return self._parse_ai_response(result)
                else:
                    return {
                        "error": f"API调用失败: {response.status_code}",
                        "emotion_type": "neutral",
                        "emotion_score": 0.5,
                        "analysis": "情绪分析服务暂时不可用"
                    }
                    
        except Exception as e:
            return {
                "error": str(e),
                "emotion_type": "neutral",
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
    
    def _parse_ai_response(self, response: Dict) -> Dict:
        """解析AI返回的响应"""
        try:
            # 从百炼API响应中提取内容
            if "output" in response and "choices" in response["output"]:
                content = response["output"]["choices"][0]["message"]["content"]
                
                # 尝试解析JSON
                # 提取JSON部分（可能被```json包裹）
                if "```json" in content:
                    content = content.split("```json")[1].split("```")[0].strip()
                elif "```" in content:
                    content = content.split("```")[1].split("```")[0].strip()
                
                result = json.loads(content)
                return result
            else:
                return {
                    "error": "无法解析AI响应",
                    "emotion_type": "neutral",
                    "emotion_score": 0.5,
                    "analysis": "响应格式异常"
                }
        except json.JSONDecodeError:
            return {
                "error": "JSON解析失败",
                "emotion_type": "neutral",
                "emotion_score": 0.5,
                "analysis": "AI返回的内容无法解析"
            }
        except Exception as e:
            return {
                "error": str(e),
                "emotion_type": "neutral",
                "emotion_score": 0.5,
                "analysis": "解析过程出错"
            }

# 单例模式
ai_service = BaiLianAIService()