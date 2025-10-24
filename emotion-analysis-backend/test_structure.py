#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试脚本：验证项目结构和配置
"""

import os
import sys
from pathlib import Path

def test_project_structure():
    """测试项目结构是否完整"""
    print("=" * 50)
    print("AI情绪分析系统 - 项目结构测试")
    print("=" * 50)
    
    base_dir = Path(__file__).parent
    
    # 必需的文件和目录
    required_items = [
        "app",
        "app/__init__.py",
        "app/main.py",
        "app/core",
        "app/core/__init__.py",
        "app/core/config.py",
        "app/core/database.py",
        "app/models",
        "app/models/__init__.py",
        "app/models/emotion.py",
        "app/schemas",
        "app/schemas/__init__.py",
        "app/schemas/emotion.py",
        "app/services",
        "app/services/__init__.py",
        "app/services/ai_service.py",
        "app/services/emotion_service.py",
        "app/api",
        "app/api/__init__.py",
        "app/api/emotion_routes.py",
        "requirements.txt",
        ".env.example",
        "init.sql",
        "README.md"
    ]
    
    print("\n检查项目文件和目录...\n")
    
    all_exists = True
    for item in required_items:
        item_path = base_dir / item
        exists = item_path.exists()
        status = "✓" if exists else "✗"
        print(f"{status} {item}")
        if not exists:
            all_exists = False
    
    print("\n" + "=" * 50)
    if all_exists:
        print("✓ 项目结构完整！")
        print("\n下一步操作：")
        print("1. 安装依赖: pip install -r requirements.txt")
        print("2. 配置环境变量: 复制 .env.example 为 .env 并填写配置")
        print("3. 初始化数据库: mysql -u root -p < init.sql")
        print("4. 启动服务: cd app && python -m uvicorn main:app --reload")
    else:
        print("✗ 项目结构不完整，请检查缺失的文件")
    
    print("=" * 50)
    
    return all_exists

if __name__ == "__main__":
    try:
        success = test_project_structure()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n错误: {e}")
        sys.exit(1)