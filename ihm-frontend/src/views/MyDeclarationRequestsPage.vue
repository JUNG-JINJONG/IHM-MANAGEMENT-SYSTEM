<template>
  <div class="page-container">
    <div class="page-header">
      <h1>내 신고서 요청</h1>
    </div>

    <div class="filters-card">
      <div class="filters-grid">
        <FormInput
          v-model="filters.search"
          type="text"
          placeholder="주문번호로 검색..."
          @update:modelValue="handleSearch"
        />
        <FormInput
          v-model="filters.status"
          type="select"
          placeholder="전체 상태"
          :options="statusOptions"
          @update:modelValue="loadRequests"
        />
      </div>
    </div>

    <DataTable
      :columns="columns"
      :data="requests"
      :loading="loading"
      :pagination="true"
      :current-page="currentPage"
      :page-size="pageSize"
      :total="totalCount"
      @page-change="handlePageChange"
      empty-message="신고서 요청이 없습니다"
    >
      <template #cell-order_number="{ row }">
        <router-link :to="`/purchase-orders/${row.purchase_order}`" class="link">
          {{ row.order_number }}
        </router-link>
      </template>

      <template #cell-status="{ value }">
        <span class="badge" :class="`badge-${value}`">
          {{ getStatusLabel(value) }}
        </span>
      </template>

      <template #cell-request_date="{ value }">
        {{ formatDate(value) }}
      </template>

      <template #cell-due_date="{ value }">
        {{ formatDate(value) }}
      </template>

      <template #actions="{ row }">
        <div class="action-buttons">
          <button @click="viewDetails(row)" class="btn-icon" title="상세보기">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </button>
          <button 
            v-if="row.status === 'approved'"
            @click="createDeclaration(row)" 
            class="btn-icon btn-icon-primary" 
            title="신고서 생성"
          >
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
            </svg>
          </button>
        </div>
      </template>
    </DataTable>

    <!-- Details Modal -->
    <Modal
      v-model:show="showDetailsModal"
      title="요청 상세정보"
      size="medium"
    >
      <div v-if="selectedRequest" class="details-view">
        <div class="detail-row">
          <span class="detail-label">주문번호:</span>
          <span class="detail-value">{{ selectedRequest.order_number }}</span>
        </div>
        <div class="detail-row">
          <span class="detail-label">선박명:</span>
          <span class="detail-value">{{ selectedRequest.ship_name }}</span>
        </div>
        <div class="detail-row">
          <span class="detail-label">요청일:</span>
          <span class="detail-value">{{ formatDate(selectedRequest.request_date) }}</span>
        </div>
        <div class="detail-row">
          <span class="detail-label">마감일:</span>
          <span class="detail-value">{{ formatDate(selectedRequest.due_date) }}</span>
        </div>
        <div class="detail-row">
          <span class="detail-label">상태:</span>
          <span class="badge" :class="`badge-${selectedRequest.status}`">
            {{ getStatusLabel(selectedRequest.status) }}
          </span>
        </div>
      </div>

      <template #footer>
        <button @click="showDetailsModal = false" class="btn btn-secondary">
          닫기
        </button>
        <button 
          v-if="selectedRequest?.status === 'approved'"
          @click="createDeclaration(selectedRequest)" 
          class="btn btn-primary"
        >
          신고서 생성
        </button>
      </template>
    </Modal>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/services/api'
import DataTable from '@/components/DataTable.vue'
import FormInput from '@/components/FormInput.vue'
import Modal from '@/components/Modal.vue'

const router = useRouter()

const requests = ref([])
const loading = ref(false)
const currentPage = ref(1)
const pageSize = ref(10)
const totalCount = ref(0)

const showDetailsModal = ref(false)
const selectedRequest = ref(null)

const filters = reactive({
  search: '',
  status: ''
})

const statusOptions = [
  { value: 'pending', label: '대기 중' },
  { value: 'submitted', label: '제출됨' },
  { value: 'approved', label: '승인됨' },
  { value: 'rejected', label: '거절됨' }
]

const columns = [
  { key: 'order_number', label: '주문번호', width: '150px' },
  { key: 'supplier_name', label: '공급업체', width: '150px' },
  { key: 'ship_name', label: '선박명', width: '150px' },
  { key: 'request_date', label: '요청일', width: '120px' },
  { key: 'due_date', label: '마감일', width: '120px' },
  { key: 'status', label: '상태', width: '100px' }
]

const formatDate = (dateString) => {
  if (!dateString) return '-'
  return new Date(dateString).toLocaleDateString('ko-KR')
}

const getStatusLabel = (status) => {
  const labels = {
    'pending': '대기 중',
    'submitted': '제출됨',
    'approved': '승인됨',
    'rejected': '거절됨'
  }
  return labels[status] || status
}

const loadRequests = async () => {
  loading.value = true
  try {
    const params = {
      page: currentPage.value,
      page_size: pageSize.value,
      search: filters.search || undefined,
      status: filters.status?.value || filters.status || undefined
    }

    const response = await api.get('/declaration-requests/', { params })
    requests.value = response.data.results || response.data
    totalCount.value = response.data.count || requests.value.length
  } catch (error) {
    console.error('Failed to load declaration requests:', error)
  } finally {
    loading.value = false
  }
}

let searchTimeout
const handleSearch = () => {
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    currentPage.value = 1
    loadRequests()
  }, 500)
}

const handlePageChange = (page) => {
  currentPage.value = page
  loadRequests()
}

const viewDetails = (request) => {
  selectedRequest.value = request
  showDetailsModal.value = true
}

const createDeclaration = (request) => {
  router.push({
    path: '/declarations/new',
    query: { request_id: request.id, po_id: request.purchase_order }
  })
}

onMounted(() => {
  loadRequests()
})
</script>

<style scoped>
.page-container {
  padding: 2rem;
}

.page-header {
  margin-bottom: 2rem;
}

.page-header h1 {
  font-size: 1.875rem;
  font-weight: 700;
  color: #111827;
  margin: 0;
}

.filters-card {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  margin-bottom: 1.5rem;
}

.filters-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
}

.link {
  color: #2563eb;
  text-decoration: none;
  font-weight: 500;
}

.link:hover {
  text-decoration: underline;
}

.badge {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  font-size: 0.75rem;
  font-weight: 600;
  border-radius: 9999px;
  text-transform: capitalize;
}

.badge-pending {
  background-color: #fef3c7;
  color: #92400e;
}

.badge-submitted {
  background-color: #dbeafe;
  color: #1e40af;
}

.badge-approved {
  background-color: #d1fae5;
  color: #065f46;
}

.badge-rejected {
  background-color: #fee2e2;
  color: #991b1b;
}

.action-buttons {
  display: flex;
  gap: 0.5rem;
  justify-content: center;
}

.btn-icon {
  padding: 0.5rem;
  background: none;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  cursor: pointer;
  color: #6b7280;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-icon:hover {
  background-color: #f3f4f6;
  color: #111827;
}

.btn-icon svg {
  width: 18px;
  height: 18px;
}

.btn-icon-primary {
  color: #2563eb;
  border-color: #2563eb;
}

.btn-icon-primary:hover {
  background-color: #dbeafe;
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

.text-danger {
  color: #dc2626 !important;
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

.btn-secondary {
  background-color: white;
  color: #374151;
  border: 1px solid #d1d5db;
}

.btn-secondary:hover {
  background-color: #f9fafb;
}

.btn-primary {
  background-color: #2563eb;
  color: white;
}

.btn-primary:hover {
  background-color: #1d4ed8;
}
</style>
