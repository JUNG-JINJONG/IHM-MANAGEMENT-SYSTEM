<template>
  <div class="page-container">
    <div class="page-header">
      <h1>내 신고서</h1>
    </div>

    <DataTable :columns="columns" :data="declarations" :loading="loading" :pagination="true" :current-page="currentPage" :page-size="pageSize" :total="totalCount" @page-change="handlePageChange" empty-message="신고서가 없습니다">
      <template #cell-declaration_number="{ row }">
        <router-link :to="`/declarations/${row.id}`" class="link">{{ row.declaration_number }}</router-link>
      </template>
      <template #cell-title="{ row }">
        <router-link :to="`/declarations/${row.id}`" class="link">{{ row.title || '-' }}</router-link>
      </template>
      <template #cell-status="{ value }">
        <span class="badge" :class="`badge-${value}`">{{ getStatusLabel(value) }}</span>
      </template>
      <template #cell-submitted_date="{ value }">{{ formatDate(value) }}</template>
      <template #actions="{ row }">
        <button @click="router.push(`/declarations/${row.id}`)" class="btn-icon" title="상세보기">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
          </svg>
        </button>
      </template>
    </DataTable>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/services/api'
import DataTable from '@/components/DataTable.vue'

const router = useRouter()
const declarations = ref([])
const loading = ref(false)
const currentPage = ref(1)
const pageSize = ref(10)
const totalCount = ref(0)

const columns = [
  { key: 'declaration_number', label: '신고서 번호', width: '150px' },
  { key: 'title', label: '신고서 제목', width: '200px' },
  { key: 'ship_name', label: '선박명', width: '150px' },
  { key: 'supplier_name', label: '공급업체', width: '150px' },
  { key: 'declaration_type', label: '유형', width: '80px' },
  { key: 'submitted_date', label: '제출일', width: '120px' },
  { key: 'status', label: '상태', width: '100px' }
]

const formatDate = (date) => date ? new Date(date).toLocaleDateString('ko-KR') : '-'

const getStatusLabel = (status) => {
  const labels = {
    'draft': '임시저장',
    'submitted': '제출됨',
    'approved': '승인됨',
    'rejected': '거절됨'
  }
  return labels[status] || status
}

const loadDeclarations = async () => {
  loading.value = true
  try {
    const response = await api.get('/declarations/', {
      params: {
        page: currentPage.value,
        page_size: pageSize.value
      }
    })
    declarations.value = response.data.results || response.data
    totalCount.value = response.data.count || declarations.value.length
  } catch (error) {
    console.error('Failed to load declarations:', error)
  } finally {
    loading.value = false
  }
}

const handlePageChange = (page) => {
  currentPage.value = page
  loadDeclarations()
}

onMounted(() => loadDeclarations())
</script>

<style scoped>
.page-container { padding: 2rem; }
.page-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 2rem; }
.page-header h1 { font-size: 1.875rem; font-weight: 700; color: #111827; margin: 0; }
.link { color: #2563eb; text-decoration: none; font-weight: 500; }
.link:hover { text-decoration: underline; }
.badge { display: inline-block; padding: 0.25rem 0.75rem; font-size: 0.75rem; font-weight: 600; border-radius: 9999px; }
.badge-draft { background-color: #e5e7eb; color: #374151; }
.badge-submitted { background-color: #dbeafe; color: #1e40af; }
.badge-approved { background-color: #d1fae5; color: #065f46; }
.badge-rejected { background-color: #fee2e2; color: #991b1b; }
.btn { padding: 0.625rem 1.25rem; font-size: 0.875rem; font-weight: 500; border-radius: 6px; border: none; cursor: pointer; }
.btn-primary { background-color: #2563eb; color: white; }
.btn-primary:hover { background-color: #1d4ed8; }
.btn-icon { padding: 0.5rem; background: none; border: 1px solid #d1d5db; border-radius: 6px; cursor: pointer; color: #6b7280; }
.btn-icon:hover { background-color: #f3f4f6; }
.btn-icon svg { width: 18px; height: 18px; }
</style>
