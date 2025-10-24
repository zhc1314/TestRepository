<template>
  <div class="dashboard">
    <nav class="navbar">
      <div class="nav-content">
        <h1 class="nav-title">🌈 心情记录器</h1>
        <div class="nav-user">
          <span>{{ authStore.username }}</span>
          <button @click="handleLogout" class="btn btn-secondary">退出</button>
        </div>
      </div>
    </nav>
    
    <div class="container">
      <div class="welcome-section">
        <h2>你好，{{ authStore.username }}！👋</h2>
        <p>今天感觉如何？记录下这一刻的心情吧</p>
      </div>
      
      <div class="action-cards">
        <router-link to="/record" class="action-card">
          <div class="card-icon">📝</div>
          <h3>记录心情</h3>
          <p>记录今天的感受</p>
        </router-link>
        
        <router-link to="/history" class="action-card">
          <div class="card-icon">📅</div>
          <h3>历史记录</h3>
          <p>查看过往心情</p>
        </router-link>
        
        <router-link to="/report" class="action-card">
          <div class="card-icon">📊</div>
          <h3>分析报告</h3>
          <p>查看心情趋势</p>
        </router-link>
      </div>
      
      <div class="recent-section">
        <h3>最近记录</h3>
        <div v-if="loading" class="loading">
          <div class="spinner"></div>
        </div>
        <div v-else-if="recentRecords.length === 0" class="empty-state">
          <p>还没有记录，快去记录你的第一条心情吧！</p>
        </div>
        <div v-else class="records-grid">
          <div v-for="record in recentRecords" :key="record.id" class="record-item">
            <div class="record-date">{{ formatDate(record.date) }}</div>
            <div class="record-mood">{{ getMoodEmoji(record.mood_level) }}</div>
            <div class="record-text">{{ record.mood_text || record.content || '无描述' }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { api } from '../services/api'

const router = useRouter()
const authStore = useAuthStore()

const recentRecords = ref([])
const loading = ref(false)

const handleLogout = () => {
  authStore.logout()
  router.push('/login')
}

const loadRecentRecords = async () => {
  loading.value = true
  try {
    const records = await api.getMoodRecords()
    recentRecords.value = records.slice(0, 6)
  } catch (error) {
    console.error('加载记录失败:', error)
  } finally {
    loading.value = false
  }
}

const formatDate = (date) => {
  const d = new Date(date)
  return `${d.getMonth() + 1}月${d.getDate()}日`
}

const getMoodEmoji = (level) => {
  const emojis = ['😢', '😔', '😐', '😊', '😄']
  return emojis[level - 1] || '😐'
}

onMounted(() => {
  loadRecentRecords()
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
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.nav-title {
  font-size: 20px;
  font-weight: 700;
  color: #333;
}

.nav-user {
  display: flex;
  align-items: center;
  gap: 16px;
}

.nav-user span {
  font-weight: 500;
  color: #666;
}

.welcome-section {
  margin: 40px 0;
  text-align: center;
}

.welcome-section h2 {
  font-size: 32px;
  margin-bottom: 8px;
  color: #333;
}

.welcome-section p {
  color: #666;
  font-size: 16px;
}

.action-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-bottom: 40px;
}

.action-card {
  background: white;
  border-radius: 16px;
  padding: 32px;
  text-align: center;
  text-decoration: none;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.action-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
}

.card-icon {
  font-size: 48px;
  margin-bottom: 16px;
}

.action-card h3 {
  font-size: 20px;
  margin-bottom: 8px;
  color: #333;
}

.action-card p {
  color: #666;
  font-size: 14px;
}

.recent-section h3 {
  font-size: 24px;
  margin-bottom: 20px;
  color: #333;
}

.records-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 16px;
}

.record-item {
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.record-date {
  font-size: 12px;
  color: #999;
  margin-bottom: 8px;
}

.record-mood {
  font-size: 32px;
  margin-bottom: 8px;
}

.record-text {
  font-size: 14px;
  color: #666;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: #999;
}
</style>
