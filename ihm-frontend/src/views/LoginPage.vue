<template>
  <div class="auth-page">
    <div class="disclaimer">
      이 웹페이지는 테스트 및 시연 목적입니다.<br>
      상업적 사용, 변경, 재배포는 허용되지 않습니다.
    </div>
    <div class="auth-card">
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

      <!-- <div class="auth-footer">
        <p>또는 <router-link to="/register">새 계정 만들기</router-link></p>
      </div> -->
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const loading = ref(false)
const error = ref('')

const quickLogin = async (userType) => {
  loading.value = true
  error.value = ''

  // 브라우저 캐시 클리어
  if ('caches' in window) {
    const cacheNames = await caches.keys()
    await Promise.all(cacheNames.map(name => caches.delete(name)))
  }

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
    // 페이지 강제 새로고침으로 리다이렉트
    window.location.href = '/dashboard'
  } else {
    error.value = result.error || '로그인 실패. 계정이 존재하지 않습니다.'
  }
}
</script>

<style scoped>
.auth-page {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 2rem;
  position: relative;
}

.disclaimer {
  position: absolute;
  top: 2rem;
  text-align: center;
  color: white;
  font-size: 0.9rem;
  font-weight: 500;
  background: rgba(0, 0, 0, 0.3);
  padding: 1rem 2rem;
  border-radius: 8px;
  backdrop-filter: blur(10px);
  line-height: 1.6;
}

.auth-card {
  background: white;
  padding: 3rem;
  border-radius: 12px;
  box-shadow: 0 10px 40px rgba(0,0,0,0.2);
  width: 100%;
  max-width: 400px;
}

.auth-card h2 {
  margin: 0 0 0.5rem 0;
  text-align: center;
  color: #2c3e50;
  font-size: 2rem;
}

.subtitle {
  text-align: center;
  color: #7f8c8d;
  margin: 0 0 2rem 0;
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

.btn {
  width: 100%;
  padding: 0.875rem;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-primary {
  background-color: #667eea;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background-color: #5568d3;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.auth-footer {
  margin-top: 2rem;
  text-align: center;
  color: #7f8c8d;
}

.auth-footer a {
  color: #667eea;
  text-decoration: none;
  font-weight: 600;
}

.auth-footer a:hover {
  text-decoration: underline;
}
</style>
