<template>
  <div class="dashboard">
    <nav class="navbar">
      <div class="nav-content">
        <button @click="router.back()" class="btn btn-secondary">← 返回</button>
        <h1 class="nav-title">记录心情</h1>
        <div></div>
      </div>
    </nav>
    
    <div class="container">
      <div class="card">
        <h2 style="margin-bottom: 24px;">今天的心情如何？</h2>
        
        <div class="input-group">
          <label>日期</label>
          <input v-model="formData.date" type="date" :max="today" />
        </div>
        
        <div class="input-group">
          <label>心情评分</label>
          <div class="mood-selector">
            <div 
              v-for="mood in moods" 
              :key="mood.level"
              class="mood-option"
              :class="{ active: formData.moodLevel === mood.level }"
              @click="formData.moodLevel = mood.level"
            >
              <span class="mood-emoji">{{ mood.emoji }}</span>
              <span class="mood-label">{{ mood.label }}</span>
            </div>
          </div>
        </div>
        
        <div class="input-group">
          <label>简短描述（可选）</label>
          <input 
            v-model="formData.moodText" 
            type="text" 
            placeholder="例如：今天很开心"
            maxlength="50"
          />
        </div>
        
        <div class="input-group">
          <label>详细内容（可选）</label>
          <textarea 
            v-model="formData.content" 
            rows="5" 
            placeholder="记录今天发生的事情、感受和想法..."
          ></textarea>
        </div>
        
        <div class="input-group">
          <label>语音记录（可选）</label>
          <div class="audio-controls">
            <button 
              v-if="!isRecording && !audioData"
              @click="startRecording" 
              class="btn btn-primary"
              type="button"
            >
              🎤 开始录音
            </button>
            <button 
              v-if="isRecording"
              @click="stopRecording" 
              class="btn btn-secondary"
              type="button"
            >
              ⏹️ 停止录音
            </button>
            <div v-if="audioData" class="audio-preview">
              <audio :src="audioData" controls></audio>
              <button @click="clearAudio" class="btn btn-secondary" type="button">删除</button>
            </div>
          </div>
          <p v-if="isRecording" class="recording-indicator">🔴 录音中...</p>
        </div>
        
        <div class="button-group">
          <button @click="handleSubmit" class="btn btn-primary" :disabled="loading || !formData.moodLevel">
            {{ loading ? '保存中...' : '保存记录' }}
          </button>
        </div>
        
        <p v-if="error" class="error-message">{{ error }}</p>
        <p v-if="success" class="success-message">{{ success }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { api } from '../services/api'

const router = useRouter()

const today = new Date().toISOString().split('T')[0]

const formData = reactive({
  date: today,
  moodLevel: null,
  moodText: '',
  content: ''
})

const moods = [
  { level: 1, emoji: '😢', label: '很糟糕' },
  { level: 2, emoji: '😔', label: '不太好' },
  { level: 3, emoji: '😐', label: '一般' },
  { level: 4, emoji: '😊', label: '不错' },
  { level: 5, emoji: '😄', label: '很棒' }
]

const loading = ref(false)
const error = ref('')
const success = ref('')
const isRecording = ref(false)
const audioData = ref('')
const mediaRecorder = ref(null)
const audioChunks = ref([])

const startRecording = async () => {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
    mediaRecorder.value = new MediaRecorder(stream)
    audioChunks.value = []
    
    mediaRecorder.value.ondataavailable = (event) => {
      audioChunks.value.push(event.data)
    }
    
    mediaRecorder.value.onstop = () => {
      const audioBlob = new Blob(audioChunks.value, { type: 'audio/webm' })
      const reader = new FileReader()
      reader.readAsDataURL(audioBlob)
      reader.onloadend = () => {
        audioData.value = reader.result
      }
      stream.getTracks().forEach(track => track.stop())
    }
    
    mediaRecorder.value.start()
    isRecording.value = true
  } catch (err) {
    error.value = '无法访问麦克风，请检查权限设置'
  }
}

const stopRecording = () => {
  if (mediaRecorder.value && isRecording.value) {
    mediaRecorder.value.stop()
    isRecording.value = false
  }
}

const clearAudio = () => {
  audioData.value = ''
}

const handleSubmit = async () => {
  error.value = ''
  success.value = ''
  
  if (!formData.moodLevel) {
    error.value = '请选择心情评分'
    return
  }
  
  loading.value = true
  
  try {
    await api.addMoodRecord({
      date: formData.date,
      moodLevel: formData.moodLevel,
      moodText: formData.moodText,
      content: formData.content,
      audioData: audioData.value
    })
    
    success.value = '记录成功！'
    
    setTimeout(() => {
      router.push('/dashboard')
    }, 1500)
  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}
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

.button-group {
  display: flex;
  gap: 12px;
  margin-top: 24px;
}

.audio-controls {
  display: flex;
  gap: 12px;
  align-items: center;
}

.audio-preview {
  display: flex;
  gap: 12px;
  align-items: center;
  flex: 1;
}

.audio-preview audio {
  flex: 1;
  max-width: 300px;
}

.recording-indicator {
  color: #f44336;
  font-size: 14px;
  margin-top: 8px;
  animation: pulse 1.5s infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}
</style>
