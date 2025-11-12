<template>
  <div class="home-page">
    <div class="disclaimer">
      이 웹페이지는 테스트 및 시연 목적입니다.<br>
      상업적 사용, 변경, 재배포는 허용되지 않습니다.
    </div>
    
    <div class="hero">
      <h1>IHM 관리 시스템에 오신 것을 환영합니다</h1>
      <p>선박 유해물질 신고서 관리를 위한 통합 플랫폼</p>
      
      <div v-if="!isAuthenticated" class="login-section">
        <h2>샘플 계정으로 로그인</h2>
        <p class="subtitle">아래 버튼을 클릭하여 각 역할로 로그인하세요</p>

        <div v-if="error" class="error-message">
          {{ error }}
        </div>

        <div class="login-buttons">
          <button 
            @click="quickLogin('operator')" 
            class="btn-role btn-operator"
            :disabled="loading"
          >
            <div class="role-icon">👨‍💼</div>
            <div class="role-info">
              <div class="role-name">operator</div>
              <div class="role-label">운영자</div>
            </div>
          </button>

          <button 
            @click="quickLogin('supplier')" 
            class="btn-role btn-supplier"
            :disabled="loading"
          >
            <div class="role-icon">🏭</div>
            <div class="role-info">
              <div class="role-name">supplier1</div>
              <div class="role-label">공급업체</div>
            </div>
          </button>

          <button 
            @click="quickLogin('customer')" 
            class="btn-role btn-customer"
            :disabled="loading"
          >
            <div class="role-icon">🚢</div>
            <div class="role-info">
              <div class="role-name">customer1</div>
              <div class="role-label">고객사</div>
            </div>
          </button>
        </div>

        <div v-if="loading" class="loading-text">로그인 중...</div>
      </div>
      <div v-else class="cta-buttons">
        <router-link to="/dashboard" class="btn btn-primary">대시보드로 이동</router-link>
      </div>
    </div>

    <div class="features">
      <div class="feature-card">
        <div class="feature-icon">📋</div>
        <h3>신고 요청서 관리</h3>
        <p>선박 부품 및 자재에 대한 유해물질 신고 요청을 관리합니다</p>
      </div>
      <div class="feature-card">
        <div class="feature-icon">📄</div>
        <h3>신고서 작성</h3>
        <p>MD/SDoC 신고서를 쉽고 빠르게 작성하고 제출합니다</p>
      </div>
      <div class="feature-card">
        <div class="feature-icon">✅</div>
        <h3>신고서 검토</h3>
        <p>제출된 신고서를 검토하고 승인/거절 처리합니다</p>
      </div>
      <div class="feature-card">
        <div class="feature-icon">🚢</div>
        <h3>선박 정보 관리</h3>
        <p>선박 정보와 관련 신고서를 통합 관리합니다</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()
const isAuthenticated = computed(() => authStore.isAuthenticated)

const loading = ref(false)
const error = ref('')

const quickLogin = async (userType) => {
  loading.value = true
  error.value = ''

  // 각 사용자 유형별 기본 계정
  const accounts = {
    operator: { username: 'operator', password: 'password123' },
    supplier: { username: 'supplier1', password: 'password123' },
    customer: { username: 'customer1', password: 'password123' }
  }

  const account = accounts[userType]
  const result = await authStore.login(account.username, account.password)

  loading.value = false

  if (result.success) {
    router.push('/dashboard')
  } else {
    error.value = result.error || '로그인 실패. 계정이 존재하지 않습니다.'
  }
}
</script>

<style scoped>
.home-page {
  max-width: 1200px;
  margin: 0 auto;
  position: relative;
  padding-top: 5rem;
}

.disclaimer {
  position: absolute;
  top: 1rem;
  left: 50%;
  transform: translateX(-50%);
  text-align: center;
  color: #2c3e50;
  font-size: 0.85rem;
  font-weight: 500;
  background: #fff3cd;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  border: 1px solid #ffc107;
  line-height: 1.6;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  z-index: 10;
}

.hero {
  text-align: center;
  padding: 4rem 2rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 12px;
  margin-bottom: 3rem;
}

.hero h1 {
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

.hero p {
  font-size: 1.2rem;
  margin-bottom: 2rem;
  opacity: 0.9;
}

.login-section {
  max-width: 500px;
  margin: 0 auto;
  background: white;
  padding: 2.5rem;
  border-radius: 12px;
  box-shadow: 0 10px 40px rgba(0,0,0,0.2);
}

.login-section h2 {
  margin: 0 0 0.5rem 0;
  color: #2c3e50;
  font-size: 1.75rem;
}

.subtitle {
  text-align: center;
  color: #7f8c8d;
  margin: 0 0 1.5rem 0;
  font-size: 0.95rem;
}

.login-buttons {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.btn-role {
  display: flex;
  align-items: center;
  padding: 1.25rem 1.5rem;
  border: 2px solid #e0e0e0;
  border-radius: 12px;
  background: white;
  cursor: pointer;
  transition: all 0.3s;
  text-align: left;
}

.btn-role:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0,0,0,0.15);
}

.btn-role:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-operator:hover:not(:disabled) {
  border-color: #3498db;
  background: #ecf6fd;
}

.btn-supplier:hover:not(:disabled) {
  border-color: #2ecc71;
  background: #eafaf1;
}

.btn-customer:hover:not(:disabled) {
  border-color: #9b59b6;
  background: #f4ecf7;
}

.role-icon {
  font-size: 2.5rem;
  margin-right: 1.25rem;
}

.role-info {
  flex: 1;
}

.role-name {
  font-size: 1.1rem;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 0.25rem;
}

.role-label {
  font-size: 0.9rem;
  color: #7f8c8d;
}

.loading-text {
  text-align: center;
  color: #667eea;
  font-weight: 500;
  margin: 1rem 0;
}

.error-message {
  background-color: #fee;
  color: #c33;
  padding: 0.75rem;
  border-radius: 8px;
  margin-bottom: 1rem;
  text-align: center;
}

.auth-footer {
  text-align: center;
  color: #7f8c8d;
  margin-top: 1.5rem;
}

.auth-footer a {
  color: #667eea;
  text-decoration: none;
  font-weight: 600;
}

.auth-footer a:hover {
  text-decoration: underline;
}

.cta-buttons {
  display: flex;
  gap: 1rem;
  justify-content: center;
}

.btn {
  padding: 0.75rem 2rem;
  border-radius: 8px;
  text-decoration: none;
  font-weight: 600;
  font-size: 1rem;
  transition: all 0.3s;
}

.btn-primary {
  background-color: white;
  color: #667eea;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.2);
}

.btn-secondary {
  background-color: transparent;
  color: white;
  border: 2px solid white;
}

.btn-secondary:hover {
  background-color: rgba(255,255,255,0.1);
}

.features {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
  padding: 0 2rem;
}

.feature-card {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  text-align: center;
  transition: transform 0.3s;
}

.feature-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 16px rgba(0,0,0,0.15);
}

.feature-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.feature-card h3 {
  margin-bottom: 0.5rem;
  color: #2c3e50;
}

.feature-card p {
  color: #7f8c8d;
  line-height: 1.6;
}
</style>
