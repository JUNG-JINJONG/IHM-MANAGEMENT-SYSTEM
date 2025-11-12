<template>
  <div class="page-container">
    <div class="page-header">
      <h1>내 선박</h1>
    </div>

    <DataTable :columns="columns" :data="ships" :loading="loading" empty-message="선박이 없습니다">
      <template #cell-ship_name="{ row }">
        <router-link :to="`/ship-declarations?ship_id=${row.id}`" class="link">{{ row.ship_name }}</router-link>
      </template>
      <template #actions="{ row }">
        <button @click="viewDeclarations(row.id)" class="btn-icon" title="신고서 보기">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
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
const ships = ref([])
const loading = ref(false)

const columns = [
  { key: 'ship_name', label: '선박명', width: '200px' },
  { key: 'imo_number', label: 'IMO 번호', width: '150px' },
  { key: 'flag', label: '국적', width: '120px' },
  { key: 'ship_type', label: '선박 종류', width: '150px' }
]

const loadShips = async () => {
  loading.value = true
  try {
    const response = await api.get('/ships/')
    ships.value = response.data.results || response.data
  } catch (error) {
    console.error('Failed to load ships:', error)
  } finally {
    loading.value = false
  }
}

const viewDeclarations = (shipId) => {
  router.push(`/ship-declarations?ship_id=${shipId}`)
}

onMounted(() => loadShips())
</script>

<style scoped>
.page-container { padding: 2rem; }
.page-header h1 { font-size: 1.875rem; font-weight: 700; color: #111827; margin: 0 0 2rem 0; }
.link { color: #2563eb; text-decoration: none; font-weight: 500; }
.link:hover { text-decoration: underline; }
.btn-icon { padding: 0.5rem; background: none; border: 1px solid #d1d5db; border-radius: 6px; cursor: pointer; color: #6b7280; }
.btn-icon:hover { background-color: #f3f4f6; }
.btn-icon svg { width: 18px; height: 18px; }
</style>
