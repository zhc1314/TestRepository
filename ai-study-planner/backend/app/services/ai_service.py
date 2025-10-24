import httpx
from typing import List, Dict, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from ..core.config import settings
from ..models.user_profile import UserProfile


class AIService:
    """AI对话服务"""
    
    def __init__(self, db: Optional[Session] = None):
        self.api_key = settings.AI_API_KEY
        self.endpoint = settings.AI_ENDPOINT
        self.model = settings.AI_MODEL_NAME
        self.max_tokens = settings.AI_MAX_TOKENS
        self.temperature = settings.AI_TEMPERATURE
        self.db = db
        # 延迟导入KnowledgeService以避免循环依赖
        self.knowledge_service = None
        if db:
            from .knowledge_service import KnowledgeService
            self.knowledge_service = KnowledgeService(db)
    
    def build_system_prompt(self, user_profile: Optional[UserProfile] = None, knowledge_context: str = "") -> str:
        """构建考研助手的系统提示词"""
        
        base_prompt = """# 角色
你是一个考研学习规划老师,能够以精简的语言回复用户问题,精准收集用户身份、考试时间等关键信息,为用户量身打造专属学习方案,针对不同人群特点制定有效的学习策略及院校专业推荐。

# 语气
以一个和蔼可亲,平易近人的老师的口吻进行回复,表达专业严谨,又不失委婉。

## 目标:
1. 对用户提出的问题做出内容精简的回复。
2. 收集用户信息:当前院校及专业、公开课备考状态、需要重点攻克的科目、目标院校及专业。
3. 输出用户专属学习方案。

## 技能
### 技能 1: 回复用户问题
1. 当用户提出问题时,参考知识库内容(如有提供),精简处理后简单回复用户。当遇到知识库中没有的问题时,回复用户"这个问题可以咨询助教老师哦~助教老师联系方式为123456"。

### 技能 2: 制定专属学习方案
1. 根据收集到的用户信息,结合不同人群的学习特点和需求,制定全面且个性化的学习方案。
2. 学习方案格式为:
--------------------------------
# 📚 个性化学习方案
## 学习目标
## 一、高顿考研特色
[参考知识库中的考研品牌信息]
## 二、高顿考研师资力量
[参考知识库中的考研品牌信息]
## 三、学习计划时间表
根据用户的目标专业,参考知识库中的学习规划方案规则内容输出。

## 四、课程推荐
{优先判断用户的目标院校及专业是否确认,若已确认,则根据用户的考试时间推荐课程,例如,26考研的用户给推荐《26考研系统班体验课》;若未确认,则给用户推荐课程《考研第一课:择校择专》。若用户的目标院校及专业及考试时间均未确定,则给用户推荐课程《考研第一课:择校择专》}
------------------------------
学习方案整体字数不超过500字。

### 技能3:给用户推荐院校及专业
1. 当用户需要我们给推荐院校及专业时,进一步询问用户信息,给用户推荐院校及专业。
2. 用户目标专业未确认时,询问用户的目标院校、是否跨考、是否想考数学、英语能力(四六级是否通过)、目标专业大类,根据以上信息给用户推荐3个专业。
3. 用户目标院校未确认时,询问用户的目标城市、目标院校层次,根据以上信息给用户推荐4个院校,1个可冲刺,2个较核心,1个保底。
4. 当用户目标专业和院校均未确认时,询问用户的目标城市、目标院校层次、是否跨考、是否想考数学、英语能力(四六级是否通过)、目标专业大类,根据以上信息,给用户推荐1个可冲刺,2个较核心,1个保底的院校及3个专业。

## 规则
1. 每次用户回复后都需要有回答和抛出1个问题。收集完目标中"当前院校及专业、公开课备考状态、需要重点攻克的科目、目标院校及专业"后,不再进行任何提问。
2. 如果需要提问,参考上下文中已收集的用户信息(如备考状态、考试时间等),禁止重复询问已获知的内容;
3. 即使用户对问题的回答没有提供有效信息(如没有计划、不清楚)也计做"已获知该问题的回答",不再重复询问该问题,当所有问题都"已获知"后,直接给用户输出学习方案。
4. 根据当前的时间判断用户输入的时间是多少。
5. 当用户咨询优惠、团报优惠、近期优惠等优惠信息时,回复用户每个课程是否优惠及优惠程度均不同,您可以留一个您的联系方式,我让助教老师联系您,或者您联系助教老师(4006008011)获取优惠信息。
6. 跟用户最多沟通6轮,6轮后回复用户"我只能陪你到这个阶段啦,更多问题助教老师可以给您更好的回答哦~助教微信123456"

## 特别注意
1. 26考研是考生和机构对2026级研究生招考的简称。用户回复26考研代表考试时间为2025年12月。以此类推,27考研代表考试时间为2026年12月,28考研代表考试时间为2027年12月。

## 限制
- 仅围绕学习规划相关内容进行回复,拒绝回答与学习规划无关的话题。
- 回复需简洁,避免不必要的冗长叙述。
- 所制定的学习方案和策略必须基于收集到的用户信息,确保针对性和可行性。
- 输出内容应清晰有条理,便于用户阅读和理解。
- 禁止用户咨询厌世辱国相关的言论"""
        
        # 如果有知识库上下文,添加到提示词中
        if knowledge_context:
            base_prompt += f"\n\n# 知识库内容\n以下是可供参考的知识库内容,请在回答时适当引用:\n{knowledge_context}"
        
        # 如果有用户画像信息,则添加用户上下文
        if user_profile:
            context = self._build_user_context(user_profile)
            base_prompt += f"\n\n# 当前用户信息\n{context}"
        
        return base_prompt
        
        # 如果有用户画像信息,则添加用户上下文
        if user_profile:
            context = self._build_user_context(user_profile)
            return f"{base_prompt}\n\n四、当前用户信息\n{context}"
        
        return base_prompt
    
    def _build_user_context(self, user_profile: UserProfile) -> str:
        """构建用户上下文信息"""
        context_parts = []
        
        # 基本信息
        if user_profile.nickname:
            context_parts.append(f"用户昵称: {user_profile.nickname}")
        
        # 目标信息
        if user_profile.target_university and user_profile.target_major:
            context_parts.append(f"目标院校/专业: {user_profile.target_university} - {user_profile.target_major}")
            if user_profile.is_cross_major:
                context_parts.append("备注: 跨专业考研")
        
        # 目标分数
        if user_profile.target_total_score:
            score_info = f"目标总分: {user_profile.target_total_score}分"
            score_details = []
            if user_profile.target_politics_score:
                score_details.append(f"政治{user_profile.target_politics_score}分")
            if user_profile.target_english_score:
                score_details.append(f"英语{user_profile.target_english_score}分")
            if user_profile.target_math_score:
                score_details.append(f"数学{user_profile.target_math_score}分")
            if user_profile.target_major_score:
                score_details.append(f"专业课{user_profile.target_major_score}分")
            if score_details:
                score_info += f" (分科目标: {', '.join(score_details)})"
            context_parts.append(score_info)
        
        # 备考时间
        if user_profile.remaining_days:
            context_parts.append(f"剩余备考时间: {user_profile.remaining_days}天")
        if user_profile.exam_date:
            context_parts.append(f"考试日期: {user_profile.exam_date.strftime('%Y年%m月%d日')}")
        
        # 每日学习时长
        study_time_info = []
        if user_profile.weekday_study_hours:
            study_time_info.append(f"工作日{user_profile.weekday_study_hours}小时")
        if user_profile.weekend_study_hours:
            study_time_info.append(f"周末{user_profile.weekend_study_hours}小时")
        if study_time_info:
            context_parts.append(f"每日学习时长: {', '.join(study_time_info)}")
        
        # 基础水平
        level_info = []
        if user_profile.politics_level:
            level_info.append(f"政治基础: {user_profile.politics_level}")
        if user_profile.english_level:
            level_info.append(f"英语基础: {user_profile.english_level}")
        if user_profile.math_level:
            level_info.append(f"数学基础: {user_profile.math_level}")
        if level_info:
            context_parts.append(f"基础水平: {', '.join(level_info)}")
        
        # 学习偏好
        if user_profile.study_time_preference:
            context_parts.append(f"学习时间偏好: {user_profile.study_time_preference}")
        if user_profile.study_method_preference:
            context_parts.append(f"学习方法偏好: {user_profile.study_method_preference}")
        
        # 薄弱科目
        if user_profile.weak_subject_priority:
            weak_subjects = ', '.join(user_profile.weak_subject_priority)
            context_parts.append(f"薄弱科目(优先级从高到低): {weak_subjects}")
        
        return "\n".join(context_parts)
    
    async def chat(
        self, 
        messages: List[Dict[str, str]], 
        user_profile: Optional[UserProfile] = None,
        user_id: Optional[str] = None,
        enable_knowledge_base: bool = True
    ) -> str:
        """调用AI模型进行对话
        
        Args:
            messages: 对话消息列表
            user_profile: 用户画像
            user_id: 用户ID(用于知识库检索记录)
            enable_knowledge_base: 是否启用知识库检索
        
        Returns:
            AI回复内容
        """
        try:
            # 获取知识库上下文(如果启用)
            knowledge_context = ""
            if enable_knowledge_base and user_id and self.knowledge_service:
                knowledge_context = await self.knowledge_service.get_context_for_chat(
                    user_message=messages[-1]["content"] if messages else "",
                    user_id=str(user_id)
                )
            
            # 构建完整的消息列表
            full_messages = []
            
            # 添加系统提示词(包含用户画像信息和知识库上下文)
            system_prompt = self.build_system_prompt(user_profile, knowledge_context)
            full_messages.append({"role": "system", "content": system_prompt})
            
            # 添加对话历史
            full_messages.extend(messages)
            
            # 调用OpenAI兼容的API
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    f"{self.endpoint}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": self.model,
                        "messages": full_messages,
                        "max_tokens": self.max_tokens,
                        "temperature": self.temperature
                    }
                )
                
                if response.status_code != 200:
                    raise Exception(f"API调用失败: {response.status_code} - {response.text}")
                
                result = response.json()
                return result["choices"][0]["message"]["content"]
        
        except Exception as e:
            raise Exception(f"AI对话服务异常: {str(e)}")