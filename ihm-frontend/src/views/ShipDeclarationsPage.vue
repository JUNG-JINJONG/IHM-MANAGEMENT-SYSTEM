<template>
  <div class="page-container">
    <div class="page-header">
      <h1>선박 신고서</h1>
    </div>

    <DataTable :columns="columns" :data="declarations" :loading="loading" empty-message="승인된 신고서가 없습니다">
      <template #cell-declaration_number="{ row }">
        <router-link :to="`/declarations/${row.id}`" class="link">{{ row.declaration_number }}</router-link>
      </template>
      <template #cell-title="{ row }">
        <router-link :to="`/declarations/${row.id}`" class="link">{{ row.title || '-' }}</router-link>
      </template>
      <template #cell-submitted_date="{ value }">{{ formatDate(value) }}</template>
      <template #cell-approved_date="{ value }">{{ formatDate(value) }}</template>
    </DataTable>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import api from '@/services/api'
import DataTable from '@/components/DataTable.vue'

const route = useRoute()
const declarations = ref([])
const loading = ref(false)

const columns = [
  { key: 'declaration_number', label: '신고서 번호', width: '150px' },
  { key: 'purchase_order_title', label: '신고요청서 제목', width: '200px' },
  { key: 'title', label: '신고서 제목', width: '200px' },
  { key: 'ship_name', label: '선박명', width: '150px' },
  { key: 'supplier_name', label: '공급업체', width: '150px' },
  { key: 'submitted_date', label: '제출일', width: '120px' },
  { key: 'approved_date', label: '승인일', width: '120px' }
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
    const params = {
      status: 'approved',  // 승인된 신고서만 조회
      ...(route.query.ship_id && { ship: route.query.ship_id })
    }
    const response = await api.get('/declarations/', { params })
    declarations.value = response.data.results || response.data
  } catch (error) {
    console.error('Failed to load declarations:', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => loadDeclarations())
</script>

<style scoped>
.page-container { padding: 2rem; }
.page-header h1 { font-size: 1.875rem; font-weight: 700; color: #111827; margin: 0 0 2rem 0; }
.link { color: #2563eb; text-decoration: none; font-weight: 500; }
.link:hover { text-decoration: underline; }
.badge { display: inline-block; padding: 0.25rem 0.75rem; font-size: 0.75rem; font-weight: 600; border-radius: 9999px; }
.badge-draft { background-color: #e5e7eb; color: #374151; }
.badge-submitted { background-color: #dbeafe; color: #1e40af; }
.badge-approved { background-color: #d1fae5; color: #065f46; }
.badge-rejected { background-color: #fee2e2; color: #991b1b; }
</style>
