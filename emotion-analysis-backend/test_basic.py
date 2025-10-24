#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
基础测试脚本：验证代码语法和导入
"""

import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_imports():
    """测试核心模块导入"""
    print("=" * 50)
    print("AI情绪分析系统 - 基础功能测试")
    print("=" * 50)
    
    tests = [
        ("配置模块", lambda: __import__('app.core.config')),
        ("数据库模块", lambda: __import__('app.core.database')),
        ("数据模型", lambda: __import__('app.models.emotion')),
        ("数据传输对象", lambda: __import__('app.schemas.emotion')),
        ("AI服务", lambda: __import__('app.services.ai_service')),
        ("情绪服务", lambda: __import__('app.services.emotion_service')),
        ("API路由", lambda: __import__('app.api.emotion_routes')),
        ("主应用", lambda: __import__('app.main')),
    ]
    
    print("\n检查模块导入...\n")
    
    passed = 0
    failed = 0
    
    for name, test_func in tests:
        try:
            test_func()
            print(f"✓ {name}")
            passed += 1
        except Exception as e:
            print(f"✗ {name}: {str(e)}")
            failed += 1
    
    print("\n" + "=" * 50)
    print(f"测试结果: {passed} 通过, {failed} 失败")
    
    if failed == 0:
        print("\n✓ 所有模块导入成功！")
        print("\n项目代码结构正确，可以进行下一步：")
        print("1. 安装依赖: python quick_install.py")
        print("2. 配置数据库: 修改 .env 文件中的数据库配置")
        print("3. 初始化数据库: mysql -u root -p < init.sql")
        print("4. 启动服务: cd app && python -m uvicorn main:app --reload")
    else:
        print("\n✗ 部分模块导入失败")
        print("提示: 请先安装依赖包")
        print("运行: python quick_install.py")
    
    print("=" * 50)
    
    return failed == 0

if __name__ == "__main__":
    try:
        success = test_imports()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)