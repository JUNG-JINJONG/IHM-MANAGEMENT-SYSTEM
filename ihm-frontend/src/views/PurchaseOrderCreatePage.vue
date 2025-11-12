<template>
  <div class="page-container">
    <div class="page-header">
      <div>
        <h1>신고 요청서 생성</h1>
        <p class="subtitle">선박 부품/자재에 대한 유해물질 신고 요청</p>
      </div>
    </div>

    <div class="form-card">
      <form @submit.prevent="submitForm">
        <div class="form-section">
          <h3 class="section-title">주문 정보</h3>
          <div class="form-grid">
            <FormInput
              v-model="form.order_number"
              type="text"
              label="주문번호"
              placeholder="자동생성"
              required
              :error="errors.order_number"
              :disabled="true"
            />
            
            <FormInput
              v-model="form.order_date"
              type="date"
              label="주문일"
              required
              :error="errors.order_date"
              :disabled="true"
            />

            <FormInput
              v-model="form.title"
              type="text"
              label="제목"
              placeholder="신고 요청서 제목 입력"
              required
              :error="errors.title"
            />

            <FormInput
              v-model="form.ship"
              type="select"
              label="선박"
              placeholder="선박 선택"
              :options="ships"
              option-value="id"
              option-label="ship_name"
              required
              :error="errors.ship"
            />
          </div>
        </div>

        <div class="form-section">
          <h3 class="section-title">요청 내용</h3>
          <div class="form-grid">
            <FormInput
              v-model="form.description"
              type="textarea"
              label="설명"
              placeholder="신고 요청 내용을 상세히 입력하세요&#10;예: 엔진 부품에 대한 유해물질 신고서 요청"
              :error="errors.description"
              rows="5"
            />
          </div>
          <p class="help-text">* 품목 상세 정보는 공급업체가 신고서 작성 시 입력합니다.</p>
        </div>

        <div class="form-actions">
          <button type="button" @click="router.back()" class="btn btn-secondary">
            취소
          </button>
          <button type="submit" class="btn btn-primary" :disabled="submitting">
            {{ submitting ? '생성 중...' : '신고 요청서 생성' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import api from '@/services/api'
import FormInput from '@/components/FormInput.vue'

const router = useRouter()
const authStore = useAuthStore()

const ships = ref([])
const submitting = ref(false)

// 주문번호 자동생성
const generatePONumber = () => {
  const now = new Date()
  const year = now.getFullYear()
  const random = Math.floor(Math.random() * 10000).toString().padStart(4, '0')
  return `PO-${year}-${random}`
}

const form = reactive({
  order_number: generatePONumber(),
  ship: '',
  order_date: new Date().toISOString().split('T')[0],
  title: '',
  description: '',
  status: 'pending'
})

const errors = reactive({
  order_number: '',
  ship: '',
  order_date: '',
  title: '',
  description: ''
})

const statusOptions = ['Pending', 'Processing', 'Completed', 'Cancelled']

const loadShips = async () => {
  try {
    const response = await api.get('/ships/')
    ships.value = response.data.results || response.data
  } catch (error) {
    console.error('Failed to load ships:', error)
  }
}

const validateForm = () => {
  let isValid = true
  
  // Reset errors
  Object.keys(errors).forEach(key => errors[key] = '')

  if (!form.order_number) {
    errors.order_number = '주문번호는 필수입니다'
    isValid = false
  }

  if (!form.ship) {
    errors.ship = '선박은 필수입니다'
    isValid = false
  }

  if (!form.order_date) {
    errors.order_date = '주문일은 필수입니다'
    isValid = false
  }

  if (!form.title) {
    errors.title = '제목은 필수입니다'
    isValid = false
  }

  return isValid
}

const submitForm = async () => {
  if (!validateForm()) {
    return
  }

  submitting.value = true
  try {
    await api.post('/purchase-orders/', {
      order_number: form.order_number,
      ship: form.ship,
      order_date: form.order_date,
      title: form.title,
      description: form.description,
      status: form.status
    })

    alert('신고 요청서가 생성되었습니다')
    router.push('/purchase-orders')
  } catch (error) {
    console.error('Failed to create purchase order:', error)
    
    if (error.response?.data) {
      Object.keys(error.response.data).forEach(key => {
        if (errors.hasOwnProperty(key)) {
          errors[key] = Array.isArray(error.response.data[key]) 
            ? error.response.data[key][0] 
            : error.response.data[key]
        }
      })
    } else {
      alert('신고 요청서 생성에 실패했습니다. 다시 시도해주세요.')
    }
  } finally {
    submitting.value = false
  }
}

onMounted(() => {
  loadShips()
})
</script>

<style scoped>
.page-container {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  margin-bottom: 2rem;
}

.page-header h1 {
  font-size: 1.875rem;
  font-weight: 700;
  color: #111827;
  margin: 0 0 0.5rem 0;
}

.subtitle {
  color: #6b7280;
  font-size: 0.875rem;
  margin: 0;
}

.form-card {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.form-section {
  margin-bottom: 2rem;
  padding-bottom: 2rem;
  border-bottom: 1px solid #e5e7eb;
}

.form-section:last-of-type {
  border-bottom: none;
}

.section-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: #111827;
  margin: 0 0 1.5rem 0;
}

.help-text {
  margin-top: 1rem;
  font-size: 0.875rem;
  color: #6b7280;
  font-style: italic;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  padding-top: 1.5rem;
}

.btn {
  padding: 0.625rem 1.5rem;
  font-size: 0.875rem;
  font-weight: 500;
  border-radius: 6px;
  border: none;
  cursor: pointer;
  transition: all 0.2s;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-primary {
  background-color: #2563eb;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background-color: #1d4ed8;
}

.btn-secondary {
  background-color: white;
  color: #374151;
  border: 1px solid #d1d5db;
}

.btn-secondary:hover {
  background-color: #f9fafb;
}
</style>
