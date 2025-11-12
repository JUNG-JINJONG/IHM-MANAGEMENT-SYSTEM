<template>
  <div class="page-container">
    <div class="page-header">
      <h1>신고서 검토</h1>
    </div>

    <div class="tabs">
      <button 
        v-for="tab in tabs" 
        :key="tab.value"
        @click="activeTab = tab.value"
        class="tab"
        :class="{ active: activeTab === tab.value }"
      >
        {{ tab.label }}
      </button>
    </div>

    <div class="filters-card">
      <FormInput
        v-model="searchQuery"
        type="text"
        placeholder="신고서 검색..."
        @update:modelValue="handleSearch"
      />
    </div>

    <DataTable
      :columns="columns"
      :data="declarations"
      :loading="loading"
      :pagination="true"
      :current-page="currentPage"
      :page-size="pageSize"
      :total="totalCount"
      @page-change="handlePageChange"
    >
      <template #cell-declaration_number="{ row }">
        <router-link :to="`/declarations/${row.id}`" class="link">
          {{ row.declaration_number }}
        </router-link>
      </template>

      <template #cell-status="{ value }">
        <span class="badge" :class="`badge-${value}`">{{ getStatusLabel(value) }}</span>
      </template>

      <template #cell-submitted_date="{ value }">
        {{ formatDate(value) }}
      </template>

      <template #cell-actions="{ row }">
        <div class="action-buttons" v-if="row.status === 'submitted'">
          <button @click="approveDeclaration(row.id)" class="btn-approve" title="승인">
            승인
          </button>
          <button @click="rejectDeclaration(row.id)" class="btn-reject" title="거부">
            거부
          </button>
        </div>
        <span v-else class="action-text">-</span>
      </template>
    </DataTable>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/services/api'
import DataTable from '@/components/DataTable.vue'
import FormInput from '@/components/FormInput.vue'

const router = useRouter()
const declarations = ref([])
const loading = ref(false)
const currentPage = ref(1)
const pageSize = ref(10)
const totalCount = ref(0)
const searchQuery = ref('')
const activeTab = ref('all')

const tabs = [
  { label: '전체', value: 'all' },
  { label: '제출됨', value: 'submitted' },
  { label: '승인됨', value: 'approved' },
  { label: '거절됨', value: 'rejected' }
]

const columns = [
  { key: 'declaration_number', label: '신고서 번호', width: '150px' },
  { key: 'purchase_order_title', label: '신고요청서 제목', width: '180px' },
  { key: 'title', label: '신고서 제목', width: '180px' },
  { key: 'ship_name', label: '선박명', width: '150px' },
  { key: 'supplier_name', label: '공급업체', width: '150px' },
  { key: 'submitted_date', label: '제출일', width: '120px' },
  { key: 'status', label: '상태', width: '100px' },
  { key: 'actions', label: '승인여부', width: '180px' }
]

const formatDate = (date) => {
  if (!date) return '-'
  const d = new Date(date)
  const year = d.getFullYear()
  const month = String(d.getMonth() + 1).padStart(2, '0')
  const day = String(d.getDate()).padStart(2, '0')
  return `${year}-${month}-${day}`
}

const getStatusLabel = (status) => {
  const labels = {
    'submitted': '제출됨',
    'approved': '승인됨',
    'rejected': '거절됨'
  }
  return labels[status] || status
}

const approveDeclaration = async (id) => {
  if (!confirm('이 신고서를 승인하시겠습니까?')) return
  
  try {
    await api.post(`/declarations/${id}/approve/`)
    alert('신고서가 승인되었습니다.')
    loadDeclarations()
  } catch (error) {
    console.error('Failed to approve declaration:', error)
    alert('승인에 실패했습니다.')
  }
}

const rejectDeclaration = async (id) => {
  if (!confirm('이 신고서를 거부하시겠습니까?')) return
  
  try {
    await api.post(`/declarations/${id}/reject/`, { rejection_reason: '거부됨' })
    alert('신고서가 거부되었습니다.')
    loadDeclarations()
  } catch (error) {
    console.error('Failed to reject declaration:', error)
    alert('거부에 실패했습니다.')
  }
}

const loadDeclarations = async () => {
  loading.value = true
  try {
    const params = {
      page: currentPage.value,
      page_size: pageSize.value,
      search: searchQuery.value || undefined,
      status: activeTab.value !== 'all' ? activeTab.value : undefined
    }
    const response = await api.get('/declarations/', { params })
    declarations.value = response.data.results
    totalCount.value = response.data.count
  } catch (error) {
    console.error('Failed to load declarations:', error)
  } finally {
    loading.value = false
  }
}

let searchTimeout
const handleSearch = () => {
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    currentPage.value = 1
    loadDeclarations()
  }, 500)
}

const handlePageChange = (page) => {
  currentPage.value = page
  loadDeclarations()
}

const viewDeclaration = (id) => router.push(`/declarations/${id}`)

watch(activeTab, () => {
  currentPage.value = 1
  loadDeclarations()
})

onMounted(() => loadDeclarations())
</script>

<style scoped>
.page-container { padding: 2rem; }
.page-header { margin-bottom: 2rem; }
.page-header h1 { font-size: 1.875rem; font-weight: 700; color: #111827; margin: 0; }
.tabs { display: flex; gap: 0.5rem; margin-bottom: 1.5rem; background: white; padding: 0.5rem; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
.tab { padding: 0.625rem 1.25rem; background: none; border: none; border-radius: 6px; cursor: pointer; font-weight: 500; color: #6b7280; transition: all 0.2s; }
.tab:hover { background-color: #f3f4f6; }
.tab.active { background-color: #2563eb; color: white; }
.filters-card { background: white; padding: 1.5rem; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); margin-bottom: 1.5rem; }
.link { color: #2563eb; text-decoration: none; font-weight: 500; }
.link:hover { text-decoration: underline; }
.badge { display: inline-block; padding: 0.25rem 0.75rem; font-size: 0.75rem; font-weight: 600; border-radius: 9999px; }
.badge-Pending { background-color: #fef3c7; color: #92400e; }
.badge-Approved { background-color: #d1fae5; color: #065f46; }
.badge-Rejected { background-color: #fee2e2; color: #991b1b; }
.type-badge { font-size: 0.875rem; font-weight: 500; color: #374151; }
.action-buttons { display: flex; gap: 0.5rem; }
.action-text { color: #9ca3af; font-size: 0.875rem; }
.btn-approve { padding: 0.5rem 1rem; background-color: #10b981; color: white; border: none; border-radius: 6px; cursor: pointer; font-size: 0.875rem; font-weight: 500; }
.btn-approve:hover { background-color: #059669; }
.btn-reject { padding: 0.5rem 1rem; background-color: #ef4444; color: white; border: none; border-radius: 6px; cursor: pointer; font-size: 0.875rem; font-weight: 500; }
.btn-reject:hover { background-color: #dc2626; }
</style>
