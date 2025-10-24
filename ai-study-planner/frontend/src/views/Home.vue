<template>
  <div class="home-container">
    <el-container>
      <!-- 侧边栏 -->
      <el-aside width="280px" class="sidebar">
        <div class="user-info">
          <el-avatar :size="60" :src="avatarUrl">
            <img src="https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png" />
          </el-avatar>
          <h3>{{ userStore.userProfile?.nickname || '考研学子' }}</h3>
          <p class="university">{{ userStore.userProfile?.target_university }}</p>
          <p class="major">{{ userStore.userProfile?.target_major }}</p>
        </div>
        
        <el-divider />
        
        <div class="study-info">
          <div class="info-item">
            <span class="label">剩余备考天数</span>
            <span class="value">{{ userStore.userProfile?.remaining_days || 0 }}天</span>
          </div>
          <div class="info-item">
            <span class="label">目标总分</span>
            <span class="value">{{ userStore.userProfile?.target_total_score || 0 }}分</span>
          </div>
        </div>
        
        <el-divider />
        
        <el-menu default-active="chat" class="sidebar-menu">
          <el-menu-item index="chat">
            <el-icon><ChatDotRound /></el-icon>
            <span>AI对话</span>
          </el-menu-item>
          <el-menu-item index="plan">
            <el-icon><Calendar /></el-icon>
            <span>学习规划</span>
          </el-menu-item>
          <el-menu-item index="profile">
            <el-icon><User /></el-icon>
            <span>个人信息</span>
          </el-menu-item>
        </el-menu>
      </el-aside>

      <!-- 主内容区 -->
      <el-main class="main-content">
        <div class="chat-container">
          <div class="chat-header">
            <h2>AI学习助手</h2>
            <p>我可以帮助您制定学习计划、解答疑问</p>
          </div>

          <!-- 聊天消息区 -->
          <div class="chat-messages" ref="messagesContainer">
            <div
              v-for="(msg, index) in messages"
              :key="index"
              :class="['message-item', msg.role]"
            >
              <div class="message-avatar">
                <el-avatar v-if="msg.role === 'user'" :size="36">
                  <el-icon><User /></el-icon>
                </el-avatar>
                <el-avatar v-else :size="36" style="background: #409eff">
                  <el-icon><Cpu /></el-icon>
                </el-avatar>
              </div>
              <div class="message-content">
                <div class="message-text">{{ msg.content }}</div>
                <div class="message-time">{{ formatTime(msg.timestamp) }}</div>
              </div>
            </div>
            
            <!-- 加载中提示 -->
            <div v-if="isLoading" class="message-item assistant">
              <div class="message-avatar">
                <el-avatar :size="36" style="background: #409eff">
                  <el-icon><Cpu /></el-icon>
                </el-avatar>
              </div>
              <div class="message-content">
                <div class="message-text loading">
                  <span class="dot"></span>
                  <span class="dot"></span>
                  <span class="dot"></span>
                </div>
              </div>
            </div>
          </div>

          <!-- 输入区 -->
          <div class="chat-input">
            <el-input
              v-model="inputMessage"
              type="textarea"
              :rows="3"
              placeholder="输入您的问题，例如：帮我制定一个数学复习计划..."
              @keydown.enter.exact="handleSend"
            />
            <div class="input-actions">
              <el-button type="primary" @click="handleSend" :loading="isLoading">
                发送
              </el-button>
              <el-button @click="clearMessages">清空</el-button>
            </div>
          </div>
        </div>
      </el-main>
    </el-container>
  </div>
</template>

<script setup lang="ts">
import { ref, nextTick, onMounted } from 'vue'
import { ChatDotRound, Calendar, User, Cpu } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/store/user'
import { sendChatMessage, type ChatMessage } from '@/api/chat'

const userStore = useUserStore()
const messagesContainer = ref<HTMLElement>()
const inputMessage = ref('')
const isLoading = ref(false)
const avatarUrl = ref('')

interface Message extends ChatMessage {
  timestamp: Date
}

const messages = ref<Message[]>([
  {
    role: 'assistant',
    content: '同学你好！我是你的考研专属智能助手～\n\n为了给你定制更贴合的备考方案，麻烦告诉我这 3 个关键信息呀：\n① 你考的是学硕还是专硕？目标院校/专业是什么？\n② 目前处于备考的哪个阶段（基础/强化/冲刺）？英语/数学/政治/专业课的基础如何？\n③ 距离考研还有多久？每天大概能投入多少时间备考？\n\n😊',
    timestamp: new Date()
  }
])

const formatTime = (date: Date) => {
  return date.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
}

const scrollToBottom = () => {
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
    }
  })
}

const handleSend = async () => {
  if (!inputMessage.value.trim()) {
    return
  }

  const userMessage: Message = {
    role: 'user',
    content: inputMessage.value,
    timestamp: new Date()
  }
  
  messages.value.push(userMessage)
  const messageText = inputMessage.value
  inputMessage.value = ''
  scrollToBottom()

  try {
    isLoading.value = true
    
    // 准备聊天历史
    const history = messages.value.slice(0, -1).map(msg => ({
      role: msg.role,
      content: msg.content
    }))

    const response = await sendChatMessage({
      user_id: userStore.userId,
      message: messageText,
      history
    })

    const assistantMessage: Message = {
      role: 'assistant',
      content: response.message,
      timestamp: new Date(response.timestamp)
    }
    
    messages.value.push(assistantMessage)
    scrollToBottom()
  } catch (error) {
    console.error('发送消息失败:', error)
    ElMessage.error('发送消息失败，请稍后重试')
  } finally {
    isLoading.value = false
  }
}

const clearMessages = () => {
  messages.value = [
    {
      role: 'assistant',
      content: '同学你好！我是你的考研专属智能助手～\n\n为了给你定制更贴合的备考方案，麻烦告诉我这 3 个关键信息呀：\n① 你考的是学硕还是专硕？目标院校/专业是什么？\n② 目前处于备考的哪个阶段（基础/强化/冲刺）？英语/数学/政治/专业课的基础如何？\n③ 距离考研还有多久？每天大概能投入多少时间备考？\n\n😊',
      timestamp: new Date()
    }
  ]
}

onMounted(() => {
  userStore.initUser()
})
</script>

<style scoped>
.home-container {
  height: 100vh;
  background: #f5f7fa;
}

.el-container {
  height: 100%;
}

.sidebar {
  background: #fff;
  box-shadow: 2px 0 8px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
}

.user-info {
  padding: 30px 20px;
  text-align: center;
}

.user-info h3 {
  margin: 15px 0 5px;
  font-size: 18px;
  color: #303133;
}

.university {
  margin: 5px 0;
  color: #606266;
  font-size: 14px;
}

.major {
  margin: 0;
  color: #909399;
  font-size: 13px;
}

.study-info {
  padding: 0 20px;
}

.info-item {
  display: flex;
  justify-content: space-between;
  margin: 12px 0;
  font-size: 14px;
}

.info-item .label {
  color: #606266;
}

.info-item .value {
  color: #409eff;
  font-weight: bold;
}

.sidebar-menu {
  flex: 1;
  border: none;
}

.main-content {
  padding: 0;
  display: flex;
  flex-direction: column;
}

.chat-container {
  height: 100%;
  display: flex;
  flex-direction: column;
  background: #fff;
  margin: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.chat-header {
  padding: 20px 30px;
  border-bottom: 1px solid #ebeef5;
}

.chat-header h2 {
  margin: 0 0 5px;
  font-size: 20px;
  color: #303133;
}

.chat-header p {
  margin: 0;
  color: #909399;
  font-size: 14px;
}

.chat-messages {
  flex: 1;
  padding: 20px 30px;
  overflow-y: auto;
}

.message-item {
  display: flex;
  margin-bottom: 20px;
}

.message-item.user {
  flex-direction: row-reverse;
}

.message-avatar {
  flex-shrink: 0;
}

.message-item.user .message-avatar {
  margin-left: 12px;
}

.message-item.assistant .message-avatar {
  margin-right: 12px;
}

.message-content {
  max-width: 70%;
}

.message-text {
  padding: 12px 16px;
  border-radius: 8px;
  line-height: 1.6;
  word-break: break-word;
}

.message-item.user .message-text {
  background: #409eff;
  color: #fff;
}

.message-item.assistant .message-text {
  background: #f4f4f5;
  color: #303133;
}

.message-time {
  margin-top: 5px;
  font-size: 12px;
  color: #c0c4cc;
}

.message-item.user .message-time {
  text-align: right;
}

.message-text.loading {
  display: flex;
  gap: 5px;
  padding: 16px;
}

.dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #909399;
  animation: bounce 1.4s infinite ease-in-out both;
}

.dot:nth-child(1) {
  animation-delay: -0.32s;
}

.dot:nth-child(2) {
  animation-delay: -0.16s;
}

@keyframes bounce {
  0%, 80%, 100% {
    transform: scale(0);
  }
  40% {
    transform: scale(1);
  }
}

.chat-input {
  padding: 20px 30px;
  border-top: 1px solid #ebeef5;
}

.input-actions {
  margin-top: 10px;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style>