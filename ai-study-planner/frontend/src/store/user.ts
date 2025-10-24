import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { UserProfile } from '@/api/userProfile'

export const useUserStore = defineStore('user', () => {
  const userId = ref<string>('')
  const userProfile = ref<UserProfile | null>(null)
  const isProfileCompleted = ref(false)

  /**
   * 设置用户ID
   */
  const setUserId = (id: string) => {
    userId.value = id
    localStorage.setItem('userId', id)
  }

  /**
   * 设置用户画像
   */
  const setUserProfile = (profile: UserProfile) => {
    userProfile.value = profile
    isProfileCompleted.value = true
  }

  /**
   * 清除用户信息
   */
  const clearUser = () => {
    userId.value = ''
    userProfile.value = null
    isProfileCompleted.value = false
    localStorage.removeItem('userId')
  }

  /**
   * 初始化用户信息（从本地存储恢复）
   */
  const initUser = () => {
    const storedUserId = localStorage.getItem('userId')
    if (storedUserId) {
      userId.value = storedUserId
    }
  }

  return {
    userId,
    userProfile,
    isProfileCompleted,
    setUserId,
    setUserProfile,
    clearUser,
    initUser
  }
})