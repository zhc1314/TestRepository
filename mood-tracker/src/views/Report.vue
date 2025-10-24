<template>
  <div class="dashboard">
    <nav class="navbar">
      <div class="nav-content">
        <button @click="router.back()" class="btn btn-secondary">← 返回</button>
        <h1 class="nav-title">分析报告</h1>
        <div></div>
      </div>
    </nav>
    
    <div class="container">
      <div v-if="loading" class="loading">
        <div class="spinner"></div>
      </div>
      
      <div v-else-if="!stats" class="empty-state">
        <p>暂无数据，快去记录心情吧！</p>
      </div>
      
      <div v-else>
        <div class="card">
          <h2>心情趋势</h2>
          <canvas ref="chartCanvas" style="max-height: 400px;"></canvas>
        </div>
        
        <div class="stats-grid">
          <div class="stat-card">
            <div class="stat-icon">📊</div>
            <div class="stat-label">平均心情</div>
            <div class="stat-value">{{ stats.averageMood.toFixed(1) }}</div>
          </div>
          <div class="stat-card">
            <div class="stat-icon">📝</div>
            <div class="stat-label">总记录数</div>
            <div class="stat-value">{{ stats.totalRecords }}</div>
          </div>
          <div class="stat-card">
            <div class="stat-icon">😄</div>
            <div class="stat-label">开心天数</div>
            <div class="stat-value">{{ stats.happyDays }}</div>
          </div>
          <div class="stat-card">
            <div class="stat-icon">😔</div>
            <div class="stat-label">低落天数</div>
            <div class="stat-value">{{ stats.sadDays }}</div>
          </div>
        </div>
        
        <div class="card" v-if="goodThings.length > 0">
          <h2>✨ 让你开心的事情</h2>
          <p class="subtitle">这些事情让你心情愉悦，建议多做：</p>
          <ul class="suggestions-list">
            <li v-for="(thing, index) in goodThings" :key="index">
              <span class="suggestion-icon">✅</span>
              <span>{{ thing }}</span>
            </li>
          </ul>
        </div>
        
        <div class="card" v-if="badThings.length > 0">
          <h2>⚠️ 让你不开心的事情</h2>
          <p class="subtitle">这些事情影响了你的心情，建议减少或避免：</p>
          <ul class="suggestions-list">
            <li v-for="(thing, index) in badThings" :key="index">
              <span class="suggestion-icon">⚠️</span>
              <span>{{ thing }}</span>
            </li>
          </ul>
        </div>
        
        <div class="card">
          <h2>💡 个性化建议</h2>
          <div class="recommendations">
            <div v-for="(rec, index) in recommendations" :key="index" class="recommendation-item">
              <span class="rec-icon">{{ rec.icon }}</span>
              <div class="rec-content">
                <h3>{{ rec.title }}</h3>
                <p>{{ rec.description }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { api } from '../services/api'

const router = useRouter()

const loading = ref(false)
const stats = ref(null)
const records = ref([])
const chartCanvas = ref(null)
const goodThings = ref([])
const badThings = ref([])
const recommendations = ref([])

const loadData = async () => {
  loading.value = true
  try {
    const [statsData, recordsData] = await Promise.all([
      api.getMoodStats(),
      api.getMoodRecords()
    ])
    
    stats.value = statsData
    records.value = recordsData
    
    await nextTick()
    drawChart()
    analyzeContent()
    generateRecommendations()
  } catch (error) {
    console.error('加载数据失败:', error)
  } finally {
    loading.value = false
  }
}

const drawChart = () => {
  if (!chartCanvas.value || !records.value.length) return
  
  const ctx = chartCanvas.value.getContext('2d')
  const canvas = chartCanvas.value
  
  const width = canvas.width = canvas.offsetWidth
  const height = canvas.height = 400
  
  const data = records.value.slice(-30).map(r => ({
    date: new Date(r.date),
    mood: r.mood_level
  }))
  
  if (data.length === 0) return
  
  const padding = 40
  const chartWidth = width - padding * 2
  const chartHeight = height - padding * 2
  
  ctx.clearRect(0, 0, width, height)
  
  ctx.strokeStyle = '#e0e0e0'
  ctx.lineWidth = 1
  for (let i = 0; i <= 5; i++) {
    const y = padding + (chartHeight / 5) * i
    ctx.beginPath()
    ctx.moveTo(padding, y)
    ctx.lineTo(width - padding, y)
    ctx.stroke()
    
    ctx.fillStyle = '#999'
    ctx.font = '12px sans-serif'
    ctx.textAlign = 'right'
    ctx.fillText(5 - i, padding - 10, y + 4)
  }
  
  ctx.strokeStyle = '#667eea'
  ctx.lineWidth = 3
  ctx.lineJoin = 'round'
  ctx.lineCap = 'round'
  
  ctx.beginPath()
  data.forEach((point, index) => {
    const x = padding + (chartWidth / (data.length - 1)) * index
    const y = padding + chartHeight - ((point.mood - 1) / 4) * chartHeight
    
    if (index === 0) {
      ctx.moveTo(x, y)
    } else {
      ctx.lineTo(x, y)
    }
  })
  ctx.stroke()
  
  data.forEach((point, index) => {
    const x = padding + (chartWidth / (data.length - 1)) * index
    const y = padding + chartHeight - ((point.mood - 1) / 4) * chartHeight
    
    ctx.fillStyle = '#667eea'
    ctx.beginPath()
    ctx.arc(x, y, 5, 0, Math.PI * 2)
    ctx.fill()
    
    if (index % Math.ceil(data.length / 7) === 0 || index === data.length - 1) {
      ctx.fillStyle = '#666'
      ctx.font = '11px sans-serif'
      ctx.textAlign = 'center'
      const dateStr = `${point.date.getMonth() + 1}/${point.date.getDate()}`
      ctx.fillText(dateStr, x, height - 10)
    }
  })
}

const analyzeContent = () => {
  const happyRecords = records.value.filter(r => r.mood_level >= 4)
  const sadRecords = records.value.filter(r => r.mood_level <= 2)
  
  const extractKeywords = (text) => {
    if (!text) return []
    const words = text.split(/[,。;；!！?？\s]+/)
    return words.filter(w => w.length >= 2 && w.length <= 10)
  }
  
  const happyKeywords = new Map()
  happyRecords.forEach(r => {
    const text = (r.mood_text || '') + ' ' + (r.content || '')
    extractKeywords(text).forEach(word => {
      happyKeywords.set(word, (happyKeywords.get(word) || 0) + 1)
    })
  })
  
  const sadKeywords = new Map()
  sadRecords.forEach(r => {
    const text = (r.mood_text || '') + ' ' + (r.content || '')
    extractKeywords(text).forEach(word => {
      sadKeywords.set(word, (sadKeywords.get(word) || 0) + 1)
    })
  })
  
  goodThings.value = Array.from(happyKeywords.entries())
    .sort((a, b) => b[1] - a[1])
    .slice(0, 5)
    .map(([word]) => word)
  
  badThings.value = Array.from(sadKeywords.entries())
    .sort((a, b) => b[1] - a[1])
    .slice(0, 5)
    .map(([word]) => word)
}

const generateRecommendations = () => {
  const recs = []
  
  if (stats.value.averageMood < 3) {
    recs.push({
      icon: '🌱',
      title: '关注心理健康',
      description: '最近的平均心情偏低，建议多参加户外活动，与朋友交流，或寻求专业心理咨询帮助。'
    })
  }
  
  if (stats.value.happyDays > stats.value.sadDays * 2) {
    recs.push({
      icon: '🎉',
      title: '保持积极状态',
      description: '你的生活状态很不错！继续保持当前的生活方式和习惯。'
    })
  }
  
  if (records.value.length >= 7) {
    const recent = records.value.slice(-7)
    const trend = recent[recent.length - 1].mood_level - recent[0].mood_level
    
    if (trend > 1) {
      recs.push({
        icon: '📈',
        title: '心情持续改善',
        description: '最近一周心情呈上升趋势，这是个好兆头！继续保持。'
      })
    } else if (trend < -1) {
      recs.push({
        icon: '📉',
        title: '关注情绪波动',
        description: '最近一周心情有所下降，建议找出原因并做出调整。'
      })
    }
  }
  
  recs.push({
    icon: '✍️',
    title: '坚持记录',
    description: '持续记录心情有助于更好地了解自己，发现生活规律和情绪模式。'
  })
  
  recommendations.value = recs
}

onMounted(() => {
  loadData()
})
</script>

<style scoped>
.dashboard {
  min-height: 100vh;
  background: #f5f7fa;
}

.navbar {
  background: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  padding: 16px 0;
}

.nav-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  align-items: center;
}

.nav-title {
  font-size: 20px;
  font-weight: 700;
  color: #333;
  text-align: center;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin: 20px 0;
}

.stat-card {
  background: white;
  border-radius: 12px;
  padding: 24px;
  text-align: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.stat-icon {
  font-size: 36px;
  margin-bottom: 12px;
}

.stat-label {
  font-size: 14px;
  color: #999;
  margin-bottom: 8px;
}

.stat-value {
  font-size: 32px;
  font-weight: 700;
  color: #333;
}

.subtitle {
  color: #666;
  margin-bottom: 16px;
}

.suggestions-list {
  list-style: none;
  padding: 0;
}

.suggestions-list li {
  display: flex;
  align-items: center;
  padding: 12px;
  background: #f9f9f9;
  border-radius: 8px;
  margin-bottom: 8px;
  gap: 12px;
}

.suggestion-icon {
  font-size: 20px;
}

.recommendations {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.recommendation-item {
  display: flex;
  gap: 16px;
  padding: 20px;
  background: #f9f9f9;
  border-radius: 12px;
  align-items: flex-start;
}

.rec-icon {
  font-size: 32px;
  flex-shrink: 0;
}

.rec-content h3 {
  font-size: 18px;
  margin-bottom: 8px;
  color: #333;
}

.rec-content p {
  font-size: 14px;
  color: #666;
  line-height: 1.6;
}
</style>
