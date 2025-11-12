<template>
  <div class="auth-page">
    <div class="disclaimer">
      이 웹페이지는 테스트 및 시연 목적입니다.<br>
      상업적 사용, 변경, 재배포는 허용되지 않습니다.
    </div>
    <div class="auth-card register-card">
      <h2>회원가입</h2>
      <form @submit.prevent="handleRegister">
        <div class="form-group">
          <label for="username">사용자명 *</label>
          <input
            id="username"
            v-model="form.username"
            type="text"
            required
            placeholder="사용자명 (로그인 ID)"
          />
        </div>

        <div class="form-group">
          <label for="email">이메일 *</label>
          <input
            id="email"
            v-model="form.email"
            type="email"
            required
            placeholder="이메일 주소"
          />
        </div>

        <div class="form-row">
          <div class="form-group">
            <label for="first_name">이름</label>
            <input
              id="first_name"
              v-model="form.first_name"
              type="text"
              placeholder="이름"
            />
          </div>

          <div class="form-group">
            <label for="last_name">성</label>
            <input
              id="last_name"
              v-model="form.last_name"
              type="text"
              placeholder="성"
            />
          </div>
        </div>

        <div class="form-group">
          <label for="user_type">사용자 유형 *</label>
          <select id="user_type" v-model="form.user_type" required>
            <option value="">선택하세요</option>
            <option value="operator">운영자</option>
            <option value="supplier">공급업체</option>
            <option value="customer">고객사</option>
          </select>
        </div>

        <div class="form-group">
          <label for="company_name">회사명</label>
          <input
            id="company_name"
            v-model="form.company_name"
            type="text"
            placeholder="회사명"
          />
        </div>

        <div class="form-group">
          <label for="contact_phone">연락처</label>
          <input
            id="contact_phone"
            v-model="form.contact_phone"
            type="tel"
            placeholder="010-1234-5678"
          />
        </div>

        <div class="form-group">
          <label for="password">비밀번호 *</label>
          <input
            id="password"
            v-model="form.password"
            type="password"
            required
            placeholder="최소 8자 이상"
          />
        </div>

        <div class="form-group">
          <label for="password_confirm">비밀번호 확인 *</label>
          <input
            id="password_confirm"
            v-model="form.password_confirm"
            type="password"
            required
            placeholder="비밀번호 재입력"
          />
        </div>

        <div v-if="error" class="error-message">
          <div v-if="typeof error === 'string'">{{ error }}</div>
          <ul v-else>
            <li v-for="(msgs, field) in error" :key="field">
              <strong>{{ field }}:</strong> {{ Array.isArray(msgs) ? msgs.join(', ') : msgs }}
            </li>
          </ul>
        </div>

        <div v-if="success" class="success-message">
          회원가입이 완료되었습니다! 로그인 페이지로 이동합니다...
        </div>

        <button type="submit" class="btn btn-primary" :disabled="loading">
          {{ loading ? '가입 중...' : '회원가입' }}
        </button>
      </form>

      <div class="auth-footer">
        <p>이미 계정이 있으신가요? <router-link to="/login">로그인</router-link></p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const form = ref({
  username: '',
  email: '',
  first_name: '',
  last_name: '',
  user_type: '',
  company_name: '',
  contact_phone: '',
  password: '',
  password_confirm: ''
})

const loading = ref(false)
const error = ref(null)
const success = ref(false)

const handleRegister = async () => {
  loading.value = true
  error.value = null
  success.value = false

  const result = await authStore.register(form.value)

  loading.value = false

  if (result.success) {
    success.value = true
    setTimeout(() => {
      router.push('/login')
    }, 2000)
  } else {
    error.value = result.error
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

.register-card {
  max-width: 500px;
}

.auth-card {
  background: white;
  padding: 3rem;
  border-radius: 12px;
  box-shadow: 0 10px 40px rgba(0,0,0,0.2);
  width: 100%;
}

.auth-card h2 {
  margin: 0 0 2rem 0;
  text-align: center;
  color: #2c3e50;
  font-size: 2rem;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: #2c3e50;
  font-weight: 600;
}

.form-group input,
.form-group select {
  width: 100%;
  padding: 0.75rem;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.3s;
}

.form-group input:focus,
.form-group select:focus {
  outline: none;
  border-color: #667eea;
}

.error-message {
  background-color: #fee;
  color: #c33;
  padding: 0.75rem;
  border-radius: 8px;
  margin-bottom: 1rem;
}

.error-message ul {
  margin: 0.5rem 0 0 1.5rem;
  padding: 0;
}

.success-message {
  background-color: #efe;
  color: #3c3;
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
