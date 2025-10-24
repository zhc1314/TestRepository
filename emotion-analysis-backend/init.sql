-- 创建数据库
CREATE DATABASE IF NOT EXISTS emotion_analysis DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE emotion_analysis;

-- 创建用户表（预留）
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '用户ID',
    username VARCHAR(50) NOT NULL UNIQUE COMMENT '用户名',
    email VARCHAR(100) NOT NULL UNIQUE COMMENT '邮箱',
    hashed_password VARCHAR(255) NOT NULL COMMENT '加密密码',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_username (username),
    INDEX idx_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户表';

-- 创建情绪记录表
CREATE TABLE IF NOT EXISTS emotion_records (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '记录ID',
    user_id INT NOT NULL COMMENT '用户ID',
    input_text TEXT NOT NULL COMMENT '用户输入的文本或日记内容',
    input_type VARCHAR(20) DEFAULT 'text' COMMENT '输入类型：text/file',
    file_path VARCHAR(500) DEFAULT NULL COMMENT '上传文件路径（如有）',
    emotion_type ENUM('HAPPY', 'SAD', 'ANGRY', 'ANXIOUS', 'CALM', 'EXCITED', 'DEPRESSED', 'NEUTRAL') DEFAULT NULL COMMENT '识别的主要情绪类型',
    emotion_score FLOAT DEFAULT NULL COMMENT '情绪强度评分(0-1)',
    analysis_result TEXT DEFAULT NULL COMMENT 'AI分析的详细结果',
    suggestions TEXT DEFAULT NULL COMMENT 'AI给出的建议',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_user_id (user_id),
    INDEX idx_created_at (created_at),
    INDEX idx_emotion_type (emotion_type),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='情绪记录表';

-- 插入测试用户（可选）
INSERT INTO users (username, email, hashed_password) VALUES 
('test_user', 'test@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYqVdL0R8w6');
-- 默认密码: test123