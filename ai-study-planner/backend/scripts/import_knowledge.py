#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
知识库导入脚本

用于将预置的知识库内容导入到数据库中
使用方法: python scripts/import_knowledge.py
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from sqlalchemy.orm import Session
from app.core.database import engine, SessionLocal
from app.models.knowledge_base import KnowledgeDocument
from app.services.knowledge_service import KnowledgeService
import asyncio


# ==================== 知识库内容定义 ====================
# 在这里定义你的知识库内容

KNOWLEDGE_DATA = [
    {
        "title": "考研品牌介绍-高顿考研特色",
        "content": """高顿考研是国内领先的考研培训机构,专注于为考研学子提供专业、高效的备考服务。

我们的核心特色包括:
1. 个性化学习方案:根据每位学员的基础、目标和时间安排,量身定制专属学习计划
2. 全程陪伴式服务:从择校择专到考试结束,提供全流程的指导和支持
3. 优质教学资源:汇集考研名师,提供高质量的课程和资料
4. 智能化学习工具:AI助手、学习进度跟踪、模拟测试等科技赋能学习
5. 贴心的学习氛围:建立学习社群,与志同道合的研友共同进步""",
        "category": "考研品牌",
        "keywords": ["品牌介绍", "特色服务", "高顿考研"],
        "source": "高顿考研官方"
    },
    {
        "title": "考研品牌介绍-高顿考研师资力量",
        "content": """高顿考研拥有一支经验丰富、实力雄厚的师资团队:

1. 政治团队:由多位资深考研政治名师组成,深谙命题规律,擅长化繁为简
2. 英语团队:英语名师团队,多年教学经验,帮助学员突破英语瓶颈
3. 数学团队:数学名师精通各类题型,善于总结方法技巧
4. 专业课团队:覆盖热门专业,由各领域专家和高分学长学姐组成

所有老师均经过严格筛选,具有:
- 深厚的学科功底
- 丰富的教学经验
- 对考研命题的深刻理解
- 强烈的责任心和耐心""",
        "category": "考研品牌",
        "keywords": ["师资力量", "教师团队", "名师"],
        "source": "高顿考研官方"
    },
    {
        "title": "学习规划-经济学专业备考方案",
        "content": """经济学专业考研学习时间表(以一年备考为例):

**基础阶段(3-6月,4个月)**
- 英语:每天2小时,背单词+长难句分析
- 数学:每天3小时,教材精读+基础习题
- 政治:每天1小时,马原+史纲框架梳理
- 专业课:每天2小时,教材通读+笔记整理

**强化阶段(7-9月,3个月)**
- 英语:每天2小时,真题精练+作文积累
- 数学:每天3小时,习题强化+真题训练
- 政治:每天1.5小时,知识点记忆+1000题
- 专业课:每天2.5小时,重点突破+真题研究

**冲刺阶段(10-12月,3个月)**
- 英语:每天1.5小时,模拟训练+查漏补缺
- 数学:每天2.5小时,真题模拟+错题回顾
- 政治:每天2小时,时政热点+模拟题
- 专业课:每天2.5小时,背诵记忆+模拟答题

**考前一周**
保持状态,调整作息,回顾错题和重点知识。""",
        "category": "学习规划",
        "sub_category": "经济学",
        "keywords": ["经济学", "时间规划", "备考方案", "学习计划"],
        "applicable_stage": "全程"
    },
    {
        "title": "学习规划-计算机专业备考方案",
        "content": """计算机专业考研学习时间表(以一年备考为例):

**基础阶段(3-6月,4个月)**
- 英语:每天2小时,词汇积累+阅读训练
- 数学:每天3小时,高数+线代+概率基础
- 政治:每天1小时,基础知识框架构建
- 专业课(408):每天2小时,数据结构+计算机组成原理教材通读

**强化阶段(7-9月,3个月)**
- 英语:每天2小时,真题精讲+翻译写作
- 数学:每天3小时,习题强化+知识点巩固
- 政治:每天1.5小时,选择题专项训练
- 专业课:每天3小时,操作系统+计算机网络深入学习+真题训练

**冲刺阶段(10-12月,3个月)**
- 英语:每天1.5小时,模拟测试+作文模板
- 数学:每天2.5小时,真题套题+易错点整理
- 政治:每天2小时,大题背诵+时事政治
- 专业课:每天3小时,四门课综合复习+模拟题训练

**考前一周**
全科回顾,保持手感,调整心态。""",
        "category": "学习规划",
        "sub_category": "计算机",
        "keywords": ["计算机", "408", "时间规划", "学习计划"],
        "applicable_stage": "全程"
    },
    {
        "title": "常见问题-考研报名时间和流程",
        "content": """考研报名时间和流程说明:

**预报名**
- 时间:每年9月下旬(约9月24日-27日)
- 对象:应届本科毕业生
- 说明:预报名与正式报名同样有效,信息可修改

**正式报名**
- 时间:每年10月中旬至月底(约10月10日-31日)
- 对象:所有考生
- 网址:中国研究生招生信息网(研招网)

**网上确认(现场确认)**
- 时间:每年11月初
- 要求:上传证件照、核对报名信息、缴纳报名费

**打印准考证**
- 时间:考前10天左右(约12月中旬)
- 网址:研招网

**注意事项**
1. 报名时需准确填写个人信息和报考信息
2. 选择报考点需根据自身情况(应届生、往届生要求不同)
3. 报名费一般在100-200元之间,各省标准不同
4. 报名后务必记住报名号和密码""",
        "category": "常见问题",
        "keywords": ["报名", "流程", "时间节点"],
        "source": "考研官方信息"
    },
    {
        "title": "常见问题-考研科目和分数构成",
        "content": """考研初试科目和分数说明:

**学硕(大部分专业)**
- 政治:100分
- 英语:100分(英语一)
- 专业课一:150分(数学或专业基础课)
- 专业课二:150分
- 总分:500分

**专硕(管理类联考除外)**
- 政治:100分
- 英语:100分(英语二,部分专业考英语一)
- 专业课一:150分
- 专业课二:150分
- 总分:500分

**管理类联考(MBA、MPA、会计专硕等)**
- 管理类联考综合:200分(数学75分+逻辑60分+写作65分)
- 英语二:100分
- 总分:300分

**各科考试时间**
- 第一天上午:政治(8:30-11:30)
- 第一天下午:外语(14:00-17:00)
- 第二天上午:专业课一(8:30-11:30)
- 第二天下午:专业课二(14:00-17:00)

**注意**
部分专业课考试时间超过3小时(如建筑学),会安排在第三天进行。""",
        "category": "常见问题",
        "keywords": ["考试科目", "分数", "考试时间"],
        "source": "考研官方信息"
    }
]


async def import_knowledge_base():
    """执行知识库导入"""
    db = SessionLocal()
    try:
        print("开始导入知识库...")
        knowledge_service = KnowledgeService(db)
        
        # 批量导入
        document_ids = await knowledge_service.batch_import_documents(KNOWLEDGE_DATA)
        
        print(f"\n导入完成!共导入 {len(document_ids)} 条知识库记录")
        print("\n导入的文档ID列表:")
        for doc_id in document_ids:
            print(f"  - 文档ID: {doc_id}")
        
        # 显示导入的文档列表
        print("\n已导入的知识库内容:")
        documents = db.query(KnowledgeDocument).filter(
            KnowledgeDocument.id.in_(document_ids)
        ).all()
        
        for doc in documents:
            print(f"\n  [{doc.category}] {doc.title}")
            if hasattr(doc, 'sub_category') and doc.sub_category:
                print(f"    - 子分类: {doc.sub_category}")
            if hasattr(doc, 'keywords') and doc.keywords:
                print(f"    - 关键词: {', '.join(doc.keywords)}")
            print(f"    - 内容长度: {len(doc.content)} 字符")
            if hasattr(doc, 'source') and doc.source:
                print(f"    - 来源: {doc.source}")
        
    except Exception as e:
        print(f"导入失败: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    print("="*60)
    print("考研AI助手 - 知识库导入工具")
    print("="*60)
    print()
    
    # 运行导入
    asyncio.run(import_knowledge_base())
    
    print("\n" + "="*60)
    print("导入流程结束")
    print("="*60)