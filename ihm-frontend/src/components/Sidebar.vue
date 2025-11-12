<template>
  <aside class="sidebar">
    <nav class="sidebar-nav">
      <ul class="nav-list">
        <!-- 공통 메뉴 -->
        <li>
          <router-link to="/dashboard" class="nav-item">
            <span class="nav-icon">📊</span>
            <span class="nav-text">대시보드</span>
          </router-link>
        </li>

        <!-- 운영자 메뉴 -->
        <template v-if="isOperator">
          <li>
            <router-link to="/purchase-orders" class="nav-item">
              <span class="nav-icon">📋</span>
              <span class="nav-text">신고 요청서 관리</span>
            </router-link>
          </li>
          <li>
            <router-link to="/declarations" class="nav-item">
              <span class="nav-icon">📄</span>
              <span class="nav-text">신고서 검토</span>
            </router-link>
          </li>
          <li>
            <router-link to="/ships" class="nav-item">
              <span class="nav-icon">🚢</span>
              <span class="nav-text">선박 관리</span>
            </router-link>
          </li>
          <!-- <li>
            <router-link to="/users" class="nav-item">
              <span class="nav-icon">👥</span>
              <span class="nav-text">사용자 관리</span>
            </router-link>
          </li> -->
        </template>

        <!-- 공급업체 메뉴 -->
        <template v-if="isSupplier">
          <li>
            <router-link to="/purchase-orders" class="nav-item">
              <span class="nav-icon">📋</span>
              <span class="nav-text">신고 요청서</span>
            </router-link>
          </li>
          <li>
            <router-link to="/my-declarations" class="nav-item">
              <span class="nav-icon">📄</span>
              <span class="nav-text">내 신고서</span>
            </router-link>
          </li>
        </template>

        <!-- 고객사 메뉴 -->
        <template v-if="isCustomer">
          <li>
            <router-link to="/my-ships" class="nav-item">
              <span class="nav-icon">🚢</span>
              <span class="nav-text">내 선박</span>
            </router-link>
          </li>
          <li>
            <router-link to="/ship-declarations" class="nav-item">
              <span class="nav-icon">📄</span>
              <span class="nav-text">선박 신고서</span>
            </router-link>
          </li>
        </template>
      </ul>
    </nav>
  </aside>
</template>

<script setup>
import { computed } from 'vue'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()

const isOperator = computed(() => authStore.isOperator)
const isSupplier = computed(() => authStore.isSupplier)
const isCustomer = computed(() => authStore.isCustomer)
</script>

<style scoped>
.sidebar {
  width: 100%;
  background-color: #34495e;
  color: white;
  position: sticky;
  top: 60px;
  z-index: 100;
  box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}

.sidebar-nav {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 1rem;
}

.nav-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  align-items: center;
}

.nav-list li {
  flex-shrink: 0;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  color: #ecf0f1;
  text-decoration: none;
  transition: all 0.2s;
  border-radius: 4px;
  white-space: nowrap;
}

.nav-item:hover {
  background-color: #2c3e50;
}

.nav-item.router-link-active {
  background-color: #3498db;
  color: white;
}

.nav-icon {
  font-size: 1.1rem;
  flex-shrink: 0;
}

.nav-text {
  font-size: 0.9rem;
}

@media (max-width: 768px) {
  .nav-list {
    gap: 0.25rem;
  }
  
  .nav-item {
    padding: 0.6rem 0.8rem;
    font-size: 0.85rem;
  }
  
  .nav-text {
    font-size: 0.8rem;
  }
  
  .nav-icon {
    font-size: 1rem;
  }
}
</style>
