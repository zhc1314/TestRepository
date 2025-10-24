<template>
  <div id="app">
    <router-view />
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from './stores/auth'

const router = useRouter()
const authStore = useAuthStore()

onMounted(() => {
  if (authStore.token) {
    router.push('/dashboard')
  }
})
</script>

<style>
#app {
  min-height: 100vh;
}
</style>
