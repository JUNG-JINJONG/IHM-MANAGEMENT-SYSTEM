<template>
  <div class="app-layout">
    <Navbar />
    <Sidebar v-if="isAuthenticated" />
    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import Navbar from './Navbar.vue'
import Sidebar from './Sidebar.vue'

const authStore = useAuthStore()
const isAuthenticated = computed(() => authStore.isAuthenticated)
</script>

<style scoped>
.app-layout {
  min-height: 100vh;
  background-color: #f5f5f5;
  padding-top: 60px;
}

.main-content {
  padding: 2rem;
  min-height: calc(100vh - 60px);
}

@media (max-width: 768px) {
  .main-content {
    padding: 1rem;
  }
}
</style>
