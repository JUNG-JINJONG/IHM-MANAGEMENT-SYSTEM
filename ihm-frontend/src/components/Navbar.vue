<template>
  <nav class="navbar">
    <div class="navbar-container">
      <div class="navbar-brand">
        <router-link to="/" class="logo">
          <h1>이 웹페이지는 테스트 및 시연 목적입니다.
상업적 사용, 변경, 재배포는 허용되지 않습니다.</h1>
        </router-link>
      </div>

      <div class="navbar-menu">
        <div v-if="isAuthenticated" class="navbar-user">
          <span class="user-info">
            {{ user?.username }} ({{ userTypeLabel }})
          </span>
          <button @click="handleLogout" class="btn btn-logout">로그아웃</button>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const isAuthenticated = computed(() => authStore.isAuthenticated)
const user = computed(() => authStore.user)

const userTypeLabel = computed(() => {
  const types = {
    'operator': '운영자',
    'supplier': '공급업체',
    'customer': '고객사'
  }
  return types[authStore.userType] || ''
})

const handleLogout = () => {
  authStore.logout()
  router.push('/login')
}
</script>

<style scoped>
.navbar {
  background-color: #2c3e50;
  color: white;
  padding: 1rem 0;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.navbar-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.navbar-brand .logo {
  text-decoration: none;
  color: white;
}

.navbar-brand h1 {
  margin: 0;
  font-size: 0.85rem;
  font-weight: 500;
  line-height: 1.4;
}

.navbar-menu {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.navbar-user {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.user-info {
  font-size: 0.9rem;
  padding: 0.5rem 1rem;
  background-color: rgba(255,255,255,0.1);
  border-radius: 4px;
}

.navbar-auth {
  display: flex;
  gap: 0.5rem;
}

.btn {
  padding: 0.5rem 1rem;
  border-radius: 4px;
  text-decoration: none;
  font-size: 0.9rem;
  cursor: pointer;
  border: none;
  transition: all 0.3s;
}

.btn-login {
  background-color: transparent;
  color: white;
  border: 1px solid white;
}

.btn-login:hover {
  background-color: rgba(255,255,255,0.1);
}

.btn-register {
  background-color: #3498db;
  color: white;
}

.btn-register:hover {
  background-color: #2980b9;
}

.btn-logout {
  background-color: #e74c3c;
  color: white;
}

.btn-logout:hover {
  background-color: #c0392b;
}
</style>
