#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速安装脚本：使用国内镜像源安装依赖
"""

import subprocess
import sys

def install_packages():
    """使用清华镜像源安装依赖包"""
    print("=" * 50)
    print("开始安装依赖包...")
    print("使用清华大学镜像源加速下载")
    print("=" * 50)
    
    packages = [
        "fastapi==0.104.1",
        "uvicorn[standard]==0.24.0",
        "python-multipart==0.0.6",
        "SQLAlchemy==2.0.23",
        "PyMySQL==1.1.0",
        "cryptography==41.0.7",
        "pydantic==2.5.0",
        "pydantic-settings==2.1.0",
        "httpx==0.25.2",
        "aiofiles==23.2.1",
        "python-dotenv==1.0.0",
        "loguru==0.7.2",
        "python-jose[cryptography]==3.3.0",
        "passlib[bcrypt]==1.7.4"
    ]
    
    # 使用清华镜像源
    pip_index = "https://pypi.tuna.tsinghua.edu.cn/simple"
    
    for i, package in enumerate(packages, 1):
        print(f"\n[{i}/{len(packages)}] 正在安装 {package}...")
        try:
            subprocess.run(
                [sys.executable, "-m", "pip", "install", package, "-i", pip_index],
                check=True,
                capture_output=False
            )
            print(f"✓ {package} 安装成功")
        except subprocess.CalledProcessError as e:
            print(f"✗ {package} 安装失败: {e}")
            print("提示：如果安装失败，可以手动运行:")
            print(f"  pip install {package} -i {pip_index}")
            continue
    
    print("\n" + "=" * 50)
    print("依赖安装完成！")
    print("\n后续步骤：")
    print("1. 配置环境变量: 复制 .env.example 为 .env")
    print("2. 初始化数据库: mysql -u root -p < init.sql")
    print("3. 启动服务: cd app && python -m uvicorn main:app --reload")
    print("=" * 50)

if __name__ == "__main__":
    try:
        install_packages()
    except KeyboardInterrupt:
        print("\n\n安装已取消")
        sys.exit(1)
    except Exception as e:
        print(f"\n错误: {e}")
        sys.exit(1)