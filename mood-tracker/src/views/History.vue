<template>
  <div class="dashboard">
    <nav class="navbar">
      <div class="nav-content">
        <button @click="router.back()" class="btn btn-secondary">← 返回</button>
        <h1 class="nav-title">历史记录</h1>
        <div></div>
      </div>
    </nav>
    
    <div class="container">
      <div class="card">
        <div class="filter-section">
          <div class="input-group">
            <label>筛选日期</label>
            <div class="date-filter">
              <input v-model="filterStartDate" type="date" />
              <span>至</span>
              <input v-model="filterEndDate" type="date" />
            </div>
          </div>
          <div class="input-group">
            <label>筛选心情</label>
            <select v-model="filterMood">
              <option value="">全部</option>
              <option value="1">😢 很糟糕</option>
              <option value="2">😔 不太好</option>
              <option value="3">😐 一般</option>
              <option value="4">😊 不错</option>
              <option value="5">😄 很棒</option>
            </select>
          </div>
        </div>
        
        <div v-if="loading" class="loading">
          <div class="spinner"></div>
        </div>
        
        <div v-else-if="filteredRecords.length === 0" class="empty-state">
          <p>没有找到记录</p>
        </div>
        
        <div v-else class="records-list">
          <div v-for="record in filteredRecords" :key="record.id" class="record-card">
            <div class="record-header">
              <div class="record-date">{{ formatDate(record.date) }}</div>
              <div class="record-actions">
                <button @click="deleteRecord(record.id)" class="btn-icon" title="删除">
                  🗑️
                </button>
              </div>
            </div>
            <div class="record-mood-display">
              <span class="mood-emoji-large">{{ getMoodEmoji(record.mood_level) }}</span>
              <span class="mood-label">{{ getMoodLabel(record.mood_level) }}</span>
            </div>
            <div v-if="record.mood_text" class="record-text">
              <strong>{{ record.mood_text }}</strong>
            </div>
            <div v-if="record.content" class="record-content">
              {{ record.content }}
            </div>
            <div v-if="record.audio_data" class="record-audio">
              <audio :src="record.audio_data" controls></audio>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { api } from '../services/api'

const router = useRouter()

const records = ref([])
const loading = ref(false)
const filterStartDate = ref('')
const filterEndDate = ref('')
const filterMood = ref('')

const moods = [
  { level: 1, emoji: '😢', label: '很糟糕' },
  { level: 2, emoji: '😔', label: '不太好' },
  { level: 3, emoji: '😐', label: '一般' },
  { level: 4, emoji: '😊', label: '不错' },
  { level: 5, emoji: '😄', label: '很棒' }
]

const filteredRecords = computed(() => {
  return records.value.filter(record => {
    let pass = true
    
    if (filterStartDate.value && record.date < filterStartDate.value) {
      pass = false
    }
    if (filterEndDate.value && record.date > filterEndDate.value) {
      pass = false
    }
    if (filterMood.value && record.mood_level !== parseInt(filterMood.value)) {
      pass = false
    }
    
    return pass
  })
})

const loadRecords = async () => {
  loading.value = true
  try {
    records.value = await api.getMoodRecords()
  } catch (error) {
    console.error('加载记录失败:', error)
  } finally {
    loading.value = false
  }
}

const deleteRecord = async (id) => {
  if (!confirm('确定要删除这条记录吗？')) return
  
  try {
    await api.deleteMoodRecord(id)
    records.value = records.value.filter(r => r.id !== id)
  } catch (error) {
    alert('删除失败：' + error.message)
  }
}

const formatDate = (date) => {
  const d = new Date(date)
  return `${d.getFullYear()}年${d.getMonth() + 1}月${d.getDate()}日`
}

const getMoodEmoji = (level) => {
  return moods.find(m => m.level === level)?.emoji || '😐'
}

const getMoodLabel = (level) => {
  return moods.find(m => m.level === level)?.label || '一般'
}

onMounted(() => {
  loadRecords()
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

.filter-section {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 20px;
  margin-bottom: 24px;
  padding-bottom: 24px;
  border-bottom: 1px solid #e0e0e0;
}

.date-filter {
  display: flex;
  align-items: center;
  gap: 12px;
}

.date-filter span {
  color: #666;
}

.records-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.record-card {
  background: #f9f9f9;
  border-radius: 12px;
  padding: 20px;
  border-left: 4px solid #667eea;
}

.record-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.record-date {
  font-size: 14px;
  color: #999;
}

.record-actions {
  display: flex;
  gap: 8px;
}

.btn-icon {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 18px;
  padding: 4px;
  opacity: 0.6;
  transition: opacity 0.2s;
}

.btn-icon:hover {
  opacity: 1;
}

.record-mood-display {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
}

.mood-emoji-large {
  font-size: 40px;
}

.mood-label {
  font-size: 18px;
  font-weight: 600;
  color: #333;
}

.record-text {
  font-size: 16px;
  color: #333;
  margin-bottom: 8px;
}

.record-content {
  font-size: 14px;
  color: #666;
  line-height: 1.6;
  margin-bottom: 12px;
}

.record-audio {
  margin-top: 12px;
}

.record-audio audio {
  width: 100%;
  max-width: 400px;
}

@media (max-width: 768px) {
  .filter-section {
    grid-template-columns: 1fr;
  }
}
</style>
