<template>
  <div class="page-container">
    <div class="page-header">
      <h1>신고 요청서 관리</h1>
      <button 
        v-if="authStore.isOperator"
        @click="router.push('/purchase-orders/new')" 
        class="btn btn-primary"
      >
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" class="icon">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
        </svg>
        신고 요청서 생성
      </button>
    </div>

    <div class="filters-card">
      <div class="filters-grid">
        <FormInput
          v-model="filters.search"
          type="text"
          placeholder="주문번호 또는 선박명으로 검색..."
          @update:modelValue="handleSearch"
        />
        <FormInput
          v-model="filters.status"
          type="select"
          placeholder="전체 상태"
          :options="statusOptions"
          @update:modelValue="loadPurchaseOrders"
        />
      </div>
    </div>

    <DataTable
      :columns="columns"
      :data="purchaseOrders"
      :loading="loading"
      :pagination="true"
      :current-page="currentPage"
      :page-size="pageSize"
      :total="totalCount"
      @page-change="handlePageChange"
      empty-message="신고 요청서가 없습니다"
    >
      <template #cell-order_number="{ value, row }">
        <router-link :to="`/purchase-orders/${row.id}`" class="link">
          {{ value }}
        </router-link>
      </template>

      <template #cell-status="{ value }">
        <span class="badge" :class="`badge-${value}`">
          {{ getStatusLabel(value) }}
        </span>
      </template>

      <template #cell-order_date="{ value }">
        {{ formatDate(value) }}
      </template>

      <template #cell-actions="{ row }">
        <div class="action-buttons">
          <button 
            v-if="row.status === 'pending'"
            @click="createDeclaration(row)" 
            class="btn btn-sm btn-primary" 
            title="신고서 작성"
          >
            신고서 작성
          </button>
          <span v-else class="status-text completed">
            작성완료
          </span>
        </div>
      </template>
    </DataTable>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import api from '@/services/api'
import DataTable from '@/components/DataTable.vue'
import FormInput from '@/components/FormInput.vue'

const router = useRouter()
const authStore = useAuthStore()

const purchaseOrders = ref([])
const loading = ref(false)
const currentPage = ref(1)
const pageSize = ref(10)
const totalCount = ref(0)

const filters = reactive({
  search: '',
  status: ''
})

const statusOptions = [
  { value: '', label: '전체 상태' },
  { value: 'pending', label: '대기' },
  { value: 'requested', label: '요청됨' },
  { value: 'completed', label: '완료' }
]

const columns = [
  { key: 'order_number', label: '주문번호', width: '150px' },
  { key: 'title', label: '제목', width: '250px' },
  { key: 'ship_name', label: '선박명', width: '180px' },
  { key: 'order_date', label: '주문일', width: '120px' },
  { key: 'status', label: '상태', width: '120px' },
  { key: 'actions', label: '작성여부', width: '150px' }
]

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

const loadPurchaseOrders = async () => {
  loading.value = true
  try {
    const params = {
      page: currentPage.value,
      page_size: pageSize.value,
      search: filters.search || undefined,
      status: filters.status?.value || filters.status || undefined
    }

    const response = await api.get('/purchase-orders/', { params })
    purchaseOrders.value = response.data.results
    totalCount.value = response.data.count
  } catch (error) {
    console.error('Failed to load purchase orders:', error)
  } finally {
    loading.value = false
  }
}

let searchTimeout
const handleSearch = () => {
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    currentPage.value = 1
    loadPurchaseOrders()
  }, 500)
}

const handlePageChange = (page) => {
  currentPage.value = page
  loadPurchaseOrders()
}

const viewDetails = (id) => {
  router.push(`/purchase-orders/${id}`)
}

const createDeclaration = (po) => {
  // 신고서 작성 화면으로 이동 (purchase order ID를 전달)
  router.push(`/declarations/new?purchase_order=${po.id}`)
}

onMounted(() => {
  loadPurchaseOrders()
})
</script>

<style scoped>
.page-container {
  padding: 2rem;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
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

.btn {
  padding: 0.625rem 1.25rem;
  font-size: 0.875rem;
  font-weight: 500;
  border-radius: 6px;
  border: none;
  cursor: pointer;
  transition: all 0.2s;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
}

.btn-primary {
  background-color: #2563eb;
  color: white;
}

.btn-primary:hover {
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

.icon {
  width: 20px;
  height: 20px;
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

.badge-requested {
  background-color: #dbeafe;
  color: #1e40af;
}

.badge-completed {
  background-color: #d1fae5;
  color: #065f46;
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

.btn-sm {
  padding: 0.5rem 1rem;
  font-size: 0.875rem;
}

.status-text {
  color: #6b7280;
  font-size: 0.875rem;
}

.status-text.completed {
  color: #059669;
  font-weight: 500;
}
</style>
