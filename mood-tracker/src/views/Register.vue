<template>
  <div class="auth-container">
    <div class="auth-card">
      <h1 class="auth-title">✨ 创建账户</h1>
      <p class="auth-subtitle">开始记录你的心情旅程</p>
      
      <form @submit.prevent="handleRegister" class="auth-form">
        <div class="input-group">
          <label>用户名</label>
          <input 
            v-model="username" 
            type="text" 
            placeholder="请输入用户名（至少3个字符）"
            required
            minlength="3"
          />
        </div>
        
        <div class="input-group">
          <label>密码</label>
          <input 
            v-model="password" 
            type="password" 
            placeholder="请输入密码（至少6个字符）"
            required
            minlength="6"
          />
        </div>
        
        <div class="input-group">
          <label>确认密码</label>
          <input 
            v-model="confirmPassword" 
            type="password" 
            placeholder="请再次输入密码"
            required
          />
        </div>
        
        <button type="submit" class="btn btn-primary btn-block" :disabled="loading">
          {{ loading ? '注册中...' : '注册' }}
        </button>
        
        <p v-if="error" class="error-message">{{ error }}</p>
      </form>
      
      <p class="auth-link">
        已有账户？
        <router-link to="/login">立即登录</router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { api } from '../services/api'

const router = useRouter()
const authStore = useAuthStore()

const username = ref('')
const password = ref('')
const confirmPassword = ref('')
const loading = ref(false)
const error = ref('')

const handleRegister = async () => {
  error.value = ''
  
  if (password.value !== confirmPassword.value) {
    error.value = '两次输入的密码不一致'
    return
  }
  
  loading.value = true
  
  try {
    const data = await api.register(username.value, password.value)
    authStore.setAuth(data.token, data.username)
    router.push('/dashboard')
  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.auth-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
}

.auth-card {
  background: white;
  border-radius: 20px;
  padding: 40px;
  width: 100%;
  max-width: 400px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
}

.auth-title {
  font-size: 28px;
  font-weight: 700;
  text-align: center;
  margin-bottom: 8px;
  color: #333;
}

.auth-subtitle {
  text-align: center;
  color: #666;
  margin-bottom: 32px;
  font-size: 14px;
}

.auth-form {
  margin-bottom: 20px;
}

.btn-block {
  width: 100%;
  margin-top: 8px;
}

.auth-link {
  text-align: center;
  font-size: 14px;
  color: #666;
}

.auth-link a {
  color: #667eea;
  text-decoration: none;
  font-weight: 600;
}

.auth-link a:hover {
  text-decoration: underline;
}
</style>
