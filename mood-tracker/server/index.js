import express from 'express';
import cors from 'cors';
import Database from 'better-sqlite3';
import bcrypt from 'bcryptjs';
import jwt from 'jsonwebtoken';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';
import fs from 'fs';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const app = express();
const PORT = 3001;
const JWT_SECRET = 'mood-tracker-secret-key-2024';

app.use(cors());
app.use(express.json({ limit: '50mb' }));

// 确保数据库目录存在
const dbDir = join(__dirname, 'data');
if (!fs.existsSync(dbDir)) {
  fs.mkdirSync(dbDir, { recursive: true });
}

// 初始化数据库
const db = new Database(join(dbDir, 'mood.db'));

// 创建表
db.exec(`
  CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
  );

  CREATE TABLE IF NOT EXISTS mood_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    date DATE NOT NULL,
    mood_level INTEGER NOT NULL,
    mood_text TEXT,
    content TEXT,
    audio_data TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
  );

  CREATE INDEX IF NOT EXISTS idx_user_date ON mood_records(user_id, date);
`);

// 认证中间件
const authMiddleware = (req, res, next) => {
  const token = req.headers.authorization?.replace('Bearer ', '');
  if (!token) {
    return res.status(401).json({ error: '未授权访问' });
  }
  try {
    const decoded = jwt.verify(token, JWT_SECRET);
    req.userId = decoded.userId;
    next();
  } catch (error) {
    res.status(401).json({ error: '令牌无效' });
  }
};

// 用户注册
app.post('/api/register', async (req, res) => {
  try {
    const { username, password } = req.body;
    if (!username || !password) {
      return res.status(400).json({ error: '用户名和密码不能为空' });
    }
    const hashedPassword = await bcrypt.hash(password, 10);
    const stmt = db.prepare('INSERT INTO users (username, password) VALUES (?, ?)');
    const result = stmt.run(username, hashedPassword);
    const token = jwt.sign({ userId: result.lastInsertRowid }, JWT_SECRET);
    res.json({ token, username });
  } catch (error) {
    if (error.message.includes('UNIQUE')) {
      res.status(400).json({ error: '用户名已存在' });
    } else {
      res.status(500).json({ error: '注册失败' });
    }
  }
});

// 用户登录
app.post('/api/login', async (req, res) => {
  try {
    const { username, password } = req.body;
    const user = db.prepare('SELECT * FROM users WHERE username = ?').get(username);
    if (!user || !(await bcrypt.compare(password, user.password))) {
      return res.status(401).json({ error: '用户名或密码错误' });
    }
    const token = jwt.sign({ userId: user.id }, JWT_SECRET);
    res.json({ token, username });
  } catch (error) {
    res.status(500).json({ error: '登录失败' });
  }
});

// 添加心情记录
app.post('/api/mood', authMiddleware, (req, res) => {
  try {
    const { date, moodLevel, moodText, content, audioData } = req.body;
    const stmt = db.prepare(
      'INSERT INTO mood_records (user_id, date, mood_level, mood_text, content, audio_data) VALUES (?, ?, ?, ?, ?, ?)'
    );
    const result = stmt.run(req.userId, date, moodLevel, moodText, content, audioData);
    res.json({ id: result.lastInsertRowid, message: '记录成功' });
  } catch (error) {
    res.status(500).json({ error: '记录失败' });
  }
});

// 获取心情记录列表
app.get('/api/mood', authMiddleware, (req, res) => {
  try {
    const { startDate, endDate } = req.query;
    let query = 'SELECT * FROM mood_records WHERE user_id = ?';
    const params = [req.userId];
    
    if (startDate && endDate) {
      query += ' AND date BETWEEN ? AND ?';
      params.push(startDate, endDate);
    }
    
    query += ' ORDER BY date DESC';
    const records = db.prepare(query).all(...params);
    res.json(records);
  } catch (error) {
    res.status(500).json({ error: '获取记录失败' });
  }
});

// 获取统计数据
app.get('/api/mood/stats', authMiddleware, (req, res) => {
  try {
    const { days = 30 } = req.query;
    const records = db.prepare(
      `SELECT date, mood_level, mood_text, content 
       FROM mood_records 
       WHERE user_id = ? AND date >= date('now', '-' || ? || ' days')
       ORDER BY date DESC`
    ).all(req.userId, days);

    // 计算平均心情
    const avgMood = records.length > 0
      ? (records.reduce((sum, r) => sum + r.mood_level, 0) / records.length).toFixed(1)
      : 0;

    // 统计心情分布
    const moodDistribution = records.reduce((acc, r) => {
      acc[r.mood_level] = (acc[r.mood_level] || 0) + 1;
      return acc;
    }, {});

    // 提取积极和消极事件
    const positiveEvents = records
      .filter(r => r.mood_level >= 4)
      .map(r => r.content || r.mood_text)
      .filter(Boolean)
      .slice(0, 10);

    const negativeEvents = records
      .filter(r => r.mood_level <= 2)
      .map(r => r.content || r.mood_text)
      .filter(Boolean)
      .slice(0, 10);

    res.json({
      totalRecords: records.length,
      avgMood,
      moodDistribution,
      positiveEvents,
      negativeEvents,
      records
    });
  } catch (error) {
    res.status(500).json({ error: '获取统计数据失败' });
  }
});

// 删除记录
app.delete('/api/mood/:id', authMiddleware, (req, res) => {
  try {
    const stmt = db.prepare('DELETE FROM mood_records WHERE id = ? AND user_id = ?');
    stmt.run(req.params.id, req.userId);
    res.json({ message: '删除成功' });
  } catch (error) {
    res.status(500).json({ error: '删除失败' });
  }
});

app.listen(PORT, () => {
  console.log(`🚀 服务器运行在 http://localhost:${PORT}`);
});
