import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/store/user'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: '/profile'
    },
    {
      path: '/profile',
      name: 'UserProfile',
      component: () => import('@/views/UserProfile.vue'),
      meta: { title: '用户信息采集' }
    },
    {
      path: '/home',
      name: 'Home',
      component: () => import('@/views/Home.vue'),
      meta: { title: '首页', requiresProfile: true }
    }
  ]
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const userStore = useUserStore()
  
  // 设置页面标题
  if (to.meta.title) {
    document.title = `${to.meta.title} - AI学习规划智能体`
  }
  
  // 检查是否需要完成用户画像
  if (to.meta.requiresProfile && !userStore.isProfileCompleted) {
    next('/profile')
  } else {
    next()
  }
})

export default router