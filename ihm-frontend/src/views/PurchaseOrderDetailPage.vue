<template>
  <div class="page-container">
    <LoadingSpinner v-if="loading" size="large" message="Loading purchase order..." />
    
    <div v-else-if="purchaseOrder">
      <div class="page-header">
        <div>
          <div class="breadcrumb">
            <router-link to="/purchase-orders">신고 요청서</router-link>
            <span class="separator">/</span>
            <span>{{ purchaseOrder.order_number }}</span>
          </div>
          <h1>{{ purchaseOrder.order_number }}</h1>
          <span class="badge" :class="`badge-${purchaseOrder.status}`">
            {{ getStatusLabel(purchaseOrder.status) }}
          </span>
        </div>
        <div class="header-actions">
          <button 
            v-if="purchaseOrder.status === 'pending' && authStore.isOperator"
            @click="router.push('/purchase-orders')" 
            class="btn btn-secondary"
          >
            목록으로
          </button>
        </div>
      </div>

      <div class="content-grid">
        <!-- Details Card -->
        <div class="details-card">
          <h3 class="card-title">신고 요청서 상세</h3>
          
          <div class="details-view">
            <div class="detail-row">
              <span class="detail-label">주문번호:</span>
              <span class="detail-value">{{ purchaseOrder.order_number }}</span>
            </div>
            <div class="detail-row">
              <span class="detail-label">주문일:</span>
              <span class="detail-value">{{ formatDate(purchaseOrder.order_date) }}</span>
            </div>
            <div class="detail-row">
              <span class="detail-label">제목:</span>
              <span class="detail-value">{{ purchaseOrder.title }}</span>
            </div>
            <div class="detail-row">
              <span class="detail-label">선박:</span>
              <span class="detail-value">{{ purchaseOrder.ship_info?.ship_name || '-' }}</span>
            </div>
            <div class="detail-row full-width">
              <span class="detail-label">설명:</span>
              <span class="detail-value description-text">{{ purchaseOrder.description || '-' }}</span>
            </div>
          </div>
        </div>

        <!-- Declaration Status Card -->
        <div class="status-card">
          <h3 class="card-title">신고서 상태</h3>
          
          <div v-if="purchaseOrder.declaration_request" class="status-info">
            <div class="status-item">
              <svg class="status-icon status-icon-info" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              <div>
                <p class="status-label">신고서 요청됨</p>
                <p class="status-value">마감일: {{ formatDate(purchaseOrder.declaration_request.due_date) }}</p>
                <p class="status-meta">상태: {{ getRequestStatusLabel(purchaseOrder.declaration_request.status) }}</p>
              </div>
            </div>
          </div>

          <div v-else-if="purchaseOrder.declaration" class="status-info">
            <div class="status-item">
              <svg class="status-icon status-icon-success" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <div>
                <p class="status-label">신고서 제출됨</p>
                <p class="status-value">
                  <router-link :to="`/declarations/${purchaseOrder.declaration.id}`" class="link">
                    신고서 보기
                  </router-link>
                </p>
                <p class="status-meta">상태: {{ getDeclarationStatusLabel(purchaseOrder.declaration.status) }}</p>
              </div>
            </div>
          </div>

          <div v-else class="status-info">
            <div class="status-item">
              <svg class="status-icon status-icon-warning" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <div>
                <p class="status-label">신고서 없음</p>
                <p class="status-value">아직 신고서가 요청되지 않았습니다</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-else class="error-message">
      <p>신고 요청서를 찾을 수 없습니다</p>
      <button @click="router.push('/purchase-orders')" class="btn btn-primary">
        목록으로 돌아가기
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import api from '@/services/api'
import LoadingSpinner from '@/components/LoadingSpinner.vue'
import FormInput from '@/components/FormInput.vue'
import Modal from '@/components/Modal.vue'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const purchaseOrder = ref(null)
const loading = ref(true)

const formatDate = (dateString) => {
  if (!dateString) return '-'
  return new Date(dateString).toLocaleDateString('ko-KR')
}

const getStatusLabel = (status) => {
  const labels = {
    'pending': '대기',
    'requested': '요청됨',
    'completed': '완료'
  }
  return labels[status] || status
}

const getRequestStatusLabel = (status) => {
  const labels = {
    'pending': '대기',
    'submitted': '제출됨',
    'approved': '승인됨',
    'rejected': '거절됨'
  }
  return labels[status] || status
}

const getDeclarationStatusLabel = (status) => {
  const labels = {
    'draft': '초안',
    'submitted': '제출됨',
    'approved': '승인됨',
    'rejected': '거절됨'
  }
  return labels[status] || status
}

const loadPurchaseOrder = async () => {
  loading.value = true
  try {
    const response = await api.get(`/purchase-orders/${route.params.id}/`)
    purchaseOrder.value = response.data
  } catch (error) {
    console.error('Failed to load purchase order:', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadPurchaseOrder()
})
</script>

<style scoped>
.page-container {
  padding: 2rem;
  max-width: 1400px;
  margin: 0 auto;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 2rem;
}

.breadcrumb {
  font-size: 0.875rem;
  color: #6b7280;
  margin-bottom: 0.5rem;
}

.breadcrumb a {
  color: #2563eb;
  text-decoration: none;
}

.breadcrumb a:hover {
  text-decoration: underline;
}

.separator {
  margin: 0 0.5rem;
}

.page-header h1 {
  font-size: 1.875rem;
  font-weight: 700;
  color: #111827;
  margin: 0 0 0.75rem 0;
}

.header-actions {
  display: flex;
  gap: 0.75rem;
}

.badge {
  display: inline-block;
  padding: 0.375rem 0.875rem;
  font-size: 0.875rem;
  font-weight: 600;
  border-radius: 9999px;
  text-transform: capitalize;
}

.badge-pending {
  background-color: #fef3c7;
  color: #92400e;
}

.badge-requested {
  background-color: #dbeafe;
  color: #1e40af;
}

.badge-completed {
  background-color: #d1fae5;
  color: #065f46;
}

.content-grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 1.5rem;
}

.details-card,
.status-card {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.card-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: #111827;
  margin: 0 0 1.5rem 0;
}

.details-view {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.detail-row {
  display: flex;
  justify-content: space-between;
  padding: 0.75rem 0;
  border-bottom: 1px solid #f3f4f6;
}

.detail-row.full-width {
  flex-direction: column;
  gap: 0.5rem;
}

.detail-row:last-child {
  border-bottom: none;
}

.detail-label {
  font-weight: 500;
  color: #6b7280;
}

.detail-value {
  color: #111827;
  text-align: right;
}

.description-text {
  text-align: left;
  white-space: pre-wrap;
  word-break: break-word;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
  margin-bottom: 1rem;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
  margin-top: 1.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid #e5e7eb;
}

.status-info {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.status-item {
  display: flex;
  gap: 1rem;
  align-items: flex-start;
}

.status-icon {
  width: 40px;
  height: 40px;
  flex-shrink: 0;
  padding: 0.5rem;
  border-radius: 8px;
}

.status-icon-info {
  background-color: #dbeafe;
  color: #2563eb;
}

.status-icon-success {
  background-color: #d1fae5;
  color: #059669;
}

.status-icon-warning {
  background-color: #fef3c7;
  color: #f59e0b;
}

.status-label {
  font-weight: 600;
  color: #111827;
  margin: 0 0 0.25rem 0;
}

.status-value {
  color: #374151;
  margin: 0 0 0.25rem 0;
}

.status-meta {
  font-size: 0.875rem;
  color: #6b7280;
  margin: 0;
}

.link {
  color: #2563eb;
  text-decoration: none;
}

.link:hover {
  text-decoration: underline;
}

.btn {
  padding: 0.625rem 1.25rem;
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

.error-message {
  text-align: center;
  padding: 3rem;
}

.error-message p {
  font-size: 1.125rem;
  color: #6b7280;
  margin-bottom: 1.5rem;
}

.modal-text {
  margin-bottom: 1.5rem;
  color: #374151;
  line-height: 1.5;
}

@media (max-width: 1024px) {
  .content-grid {
    grid-template-columns: 1fr;
  }
  
  .form-grid {
    grid-template-columns: 1fr;
  }
}
</style>
