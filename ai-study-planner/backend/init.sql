-- 创建数据库
CREATE DATABASE IF NOT EXISTS ai_study_planner CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE ai_study_planner;

-- 创建用户画像表
CREATE TABLE IF NOT EXISTS user_profiles (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    user_id VARCHAR(50) NOT NULL UNIQUE COMMENT '用户ID',
    nickname VARCHAR(100) COMMENT '昵称',
    
    -- 目标院校/专业
    target_university VARCHAR(200) COMMENT '目标院校',
    target_major VARCHAR(200) COMMENT '目标专业',
    is_cross_major BOOLEAN DEFAULT FALSE COMMENT '是否跨考',
    major_subjects JSON COMMENT '专业课科目列表',
    
    -- 目标分数
    target_total_score INT COMMENT '目标总分',
    target_politics_score INT COMMENT '政治目标分',
    target_english_score INT COMMENT '英语目标分',
    target_math_score INT COMMENT '数学目标分',
    target_major_score INT COMMENT '专业课目标分',
    
    -- 备考时间规划
    study_start_date DATE COMMENT '备考开始时间',
    exam_date DATE COMMENT '考试日期',
    weekday_study_hours DECIMAL(4,1) COMMENT '工作日每日学习时长',
    weekend_study_hours DECIMAL(4,1) COMMENT '周末每日学习时长',
    remaining_days INT COMMENT '剩余备考天数',
    
    -- 现有基础评估
    politics_level VARCHAR(20) COMMENT '政治基础水平',
    english_level VARCHAR(20) COMMENT '英语基础水平',
    math_level VARCHAR(20) COMMENT '数学基础水平',
    major_knowledge_score INT COMMENT '专业课知识掌握分数',
    major_knowledge_detail JSON COMMENT '专业课知识点详情',
    
    -- 学习偏好
    study_time_preference VARCHAR(50) COMMENT '学习时间偏好',
    study_method_preference VARCHAR(50) COMMENT '学习方法偏好',
    weak_subject_priority JSON COMMENT '薄弱科目优先级',
    other_preferences TEXT COMMENT '其他偏好说明',
    
    -- 时间戳
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    
    INDEX idx_user_id (user_id),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户画像表';

-- 创建聊天历史表（预留，后续可用于存储聊天记录）
CREATE TABLE IF NOT EXISTS chat_history (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    user_id VARCHAR(50) NOT NULL COMMENT '用户ID',
    role VARCHAR(20) NOT NULL COMMENT '角色：user/assistant',
    content TEXT NOT NULL COMMENT '消息内容',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    
    INDEX idx_user_id (user_id),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='聊天历史表';