<template>
  <div class="page-container">
    <div class="page-header">
      <h1>선박 관리</h1>
      <button v-if="authStore.isCustomer" @click="router.push('/ships/new')" class="btn btn-primary">선박 추가</button>
    </div>

    <DataTable :columns="columns" :data="ships" :loading="loading" :pagination="true" :current-page="currentPage" :page-size="pageSize" :total="totalCount" @page-change="handlePageChange">
      <template #cell-ship_name="{ row }">
        <router-link :to="`/ships/${row.id}/edit`" class="link">{{ row.ship_name }}</router-link>
      </template>
      <template #actions="{ row }">
        <button @click="router.push(`/ships/${row.id}/edit`)" class="btn-icon" title="수정">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
          </svg>
        </button>
      </template>
    </DataTable>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import api from '@/services/api'
import DataTable from '@/components/DataTable.vue'

const router = useRouter()
const authStore = useAuthStore()
const ships = ref([])
const loading = ref(false)
const currentPage = ref(1)
const pageSize = ref(10)
const totalCount = ref(0)

const columns = [
  { key: 'ship_name', label: '선박명', width: '200px' },
  { key: 'imo_number', label: 'IMO 번호', width: '150px' },
  { key: 'ship_type', label: '선박 유형', width: '150px' },
  { key: 'gross_tonnage', label: '총톤수', width: '120px' },
  { key: 'year_built', label: '건조년도', width: '100px' }
]

const loadShips = async () => {
  loading.value = true
  try {
    const response = await api.get('/ships/', { params: { page: currentPage.value, page_size: pageSize.value } })
    ships.value = response.data.results
    totalCount.value = response.data.count
  } catch (error) {
    console.error('Failed to load ships:', error)
  } finally {
    loading.value = false
  }
}

const handlePageChange = (page) => {
  currentPage.value = page
  loadShips()
}

onMounted(() => loadShips())
</script>

<style scoped>
.page-container { padding: 2rem; }
.page-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 2rem; }
.page-header h1 { font-size: 1.875rem; font-weight: 700; color: #111827; margin: 0; }
.link { color: #2563eb; text-decoration: none; font-weight: 500; }
.link:hover { text-decoration: underline; }
.btn { padding: 0.625rem 1.25rem; font-size: 0.875rem; font-weight: 500; border-radius: 6px; border: none; cursor: pointer; }
.btn-primary { background-color: #2563eb; color: white; }
.btn-primary:hover { background-color: #1d4ed8; }
.btn-icon { padding: 0.5rem; background: none; border: 1px solid #d1d5db; border-radius: 6px; cursor: pointer; color: #6b7280; }
.btn-icon:hover { background-color: #f3f4f6; }
.btn-icon svg { width: 18px; height: 18px; }
</style>
