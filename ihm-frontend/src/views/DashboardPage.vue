<template>
  <div class="dashboard">
    <h1 class="page-title">대시보드</h1>
    
    <div class="welcome-card">
      <h2>환영합니다, {{ user?.username }}님!</h2>
      <p class="user-role">{{ userRoleLabel }}</p>
    </div>

    <!-- 운영자 대시보드 -->
    <div v-if="isOperator" class="dashboard-content">
      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-icon">📋</div>
          <div class="stat-info">
            <h3>신고 요청서</h3>
            <p class="stat-number">{{ stats.purchaseOrders || 0 }}</p>
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-icon">📨</div>
          <div class="stat-info">
            <h3>대기중 요청</h3>
            <p class="stat-number">{{ stats.pendingRequests || 0 }}</p>
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-icon">📄</div>
          <div class="stat-info">
            <h3>검토 대기</h3>
            <p class="stat-number">{{ stats.pendingDeclarations || 0 }}</p>
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-icon">✅</div>
          <div class="stat-info">
            <h3>승인 완료</h3>
            <p class="stat-number">{{ stats.approvedDeclarations || 0 }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- 공급업체 대시보드 -->
    <div v-if="isSupplier" class="dashboard-content">
      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-icon">📋</div>
          <div class="stat-info">
            <h3>내 주문</h3>
            <p class="stat-number">{{ stats.myOrders || 0 }}</p>
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-icon">📨</div>
          <div class="stat-info">
            <h3>신고서 요청</h3>
            <p class="stat-number">{{ stats.pendingRequests || 0 }}</p>
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-icon">📄</div>
          <div class="stat-info">
            <h3>제출한 신고서</h3>
            <p class="stat-number">{{ stats.myDeclarations || 0 }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- 고객사 대시보드 -->
    <div v-if="isCustomer" class="dashboard-content">
      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-icon">🚢</div>
          <div class="stat-info">
            <h3>내 선박</h3>
            <p class="stat-number">{{ stats.myShips || 0 }}</p>
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-icon">📄</div>
          <div class="stat-info">
            <h3>선박 신고서</h3>
            <p class="stat-number">{{ stats.shipDeclarations || 0 }}</p>
          </div>
        </div>
      </div>
    </div>

    <div class="quick-actions">
      <h2>빠른 작업</h2>
      <div class="action-buttons">
        <button 
          v-if="isOperator" 
          @click="router.push('/purchase-orders/new')" 
          class="action-btn"
        >
          ➕ 신고 요청서 생성
        </button>
        <router-link 
          v-if="isSupplier" 
          to="/my-declaration-requests" 
          class="action-btn"
        >
          📨 신고서 요청 확인
        </router-link>
        <router-link 
          v-if="isCustomer" 
          to="/my-ships" 
          class="action-btn"
        >
          🚢 내 선박 보기
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()
const user = computed(() => authStore.user)
const isOperator = computed(() => authStore.isOperator)
const isSupplier = computed(() => authStore.isSupplier)
const isCustomer = computed(() => authStore.isCustomer)

const userRoleLabel = computed(() => {
  const roles = {
    'operator': '운영자',
    'supplier': '공급업체',
    'customer': '고객사'
  }
  return roles[authStore.userType] || ''
})

const stats = ref({})

onMounted(async () => {
  // TODO: API에서 통계 데이터 가져오기
  stats.value = {
    purchaseOrders: 70,
    pendingRequests: 15,
    pendingDeclarations: 8,
    approvedDeclarations: 45,
    myOrders: 12,
    myDeclarations: 20,
    myShips: 5,
    shipDeclarations: 30
  }
})
</script>

<style scoped>
.dashboard {
  max-width: 1200px;
}

.page-title {
  font-size: 2rem;
  margin-bottom: 2rem;
  color: #2c3e50;
}

.welcome-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 2rem;
  border-radius: 12px;
  margin-bottom: 2rem;
}

.welcome-card h2 {
  margin: 0 0 0.5rem 0;
  font-size: 1.8rem;
}

.user-role {
  margin: 0;
  font-size: 1.1rem;
  opacity: 0.9;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  display: flex;
  align-items: center;
  gap: 1rem;
}

.stat-icon {
  font-size: 2.5rem;
}

.stat-info h3 {
  margin: 0 0 0.5rem 0;
  font-size: 0.9rem;
  color: #7f8c8d;
  font-weight: 500;
}

.stat-number {
  margin: 0;
  font-size: 2rem;
  font-weight: 700;
  color: #2c3e50;
}

.quick-actions {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.quick-actions h2 {
  margin: 0 0 1.5rem 0;
  font-size: 1.3rem;
  color: #2c3e50;
}

.action-buttons {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.action-btn {
  padding: 0.75rem 1.5rem;
  background-color: #3498db;
  color: white;
  text-decoration: none;
  border-radius: 8px;
  font-weight: 600;
  transition: all 0.3s;
}

.action-btn:hover {
  background-color: #2980b9;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(52, 152, 219, 0.3);
}
</style>
