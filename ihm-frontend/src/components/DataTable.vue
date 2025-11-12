<template>
  <div class="data-table">
    <div class="table-header" v-if="$slots.header">
      <slot name="header"></slot>
    </div>
    
    <div class="table-container">
      <table>
        <thead>
          <tr>
            <th v-for="column in columns" :key="column.key" :style="{ width: column.width }">
              {{ column.label }}
            </th>
          </tr>
        </thead>
        <tbody v-if="!loading && data.length > 0">
          <tr v-for="(row, index) in data" :key="row.id || index">
            <td v-for="column in columns" :key="column.key">
              <slot :name="`cell-${column.key}`" :row="row" :value="row[column.key]">
                {{ formatValue(row[column.key], column) }}
              </slot>
            </td>
          </tr>
        </tbody>
        <tbody v-else-if="loading">
          <tr>
            <td :colspan="columns.length" class="text-center">
              <LoadingSpinner />
            </td>
          </tr>
        </tbody>
        <tbody v-else>
          <tr>
            <td :colspan="columns.length" class="text-center empty-message">
              {{ emptyMessage }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="table-footer" v-if="pagination">
      <div class="pagination-info">
        Showing {{ startItem }} to {{ endItem }} of {{ total }} entries
      </div>
      <div class="pagination-controls">
        <button 
          @click="$emit('page-change', currentPage - 1)" 
          :disabled="currentPage === 1"
          class="btn-pagination"
        >
          Previous
        </button>
        <span class="page-numbers">
          <button 
            v-for="page in visiblePages" 
            :key="page"
            @click="$emit('page-change', page)"
            :class="{ active: page === currentPage }"
            class="btn-page"
          >
            {{ page }}
          </button>
        </span>
        <button 
          @click="$emit('page-change', currentPage + 1)" 
          :disabled="currentPage === totalPages"
          class="btn-pagination"
        >
          Next
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import LoadingSpinner from './LoadingSpinner.vue'

const props = defineProps({
  columns: {
    type: Array,
    required: true
  },
  data: {
    type: Array,
    default: () => []
  },
  loading: {
    type: Boolean,
    default: false
  },
  emptyMessage: {
    type: String,
    default: 'No data available'
  },
  pagination: {
    type: Boolean,
    default: false
  },
  currentPage: {
    type: Number,
    default: 1
  },
  pageSize: {
    type: Number,
    default: 10
  },
  total: {
    type: Number,
    default: 0
  }
})

defineEmits(['page-change'])

const totalPages = computed(() => Math.ceil(props.total / props.pageSize))
const startItem = computed(() => (props.currentPage - 1) * props.pageSize + 1)
const endItem = computed(() => Math.min(props.currentPage * props.pageSize, props.total))

const visiblePages = computed(() => {
  const pages = []
  const maxVisible = 5
  let start = Math.max(1, props.currentPage - Math.floor(maxVisible / 2))
  let end = Math.min(totalPages.value, start + maxVisible - 1)
  
  if (end - start < maxVisible - 1) {
    start = Math.max(1, end - maxVisible + 1)
  }
  
  for (let i = start; i <= end; i++) {
    pages.push(i)
  }
  
  return pages
})

const formatValue = (value, column) => {
  if (column.format) {
    return column.format(value)
  }
  if (value === null || value === undefined) {
    return '-'
  }
  return value
}
</script>

<style scoped>
.data-table {
  background: white;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.table-header {
  padding: 1rem 1.5rem;
  border-bottom: 1px solid #e5e7eb;
}

.table-container {
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
}

thead {
  background-color: #f9fafb;
}

th {
  padding: 0.75rem 1rem;
  text-align: left;
  font-weight: 600;
  font-size: 0.875rem;
  color: #374151;
  border-bottom: 1px solid #e5e7eb;
}

td {
  padding: 0.75rem 1rem;
  font-size: 0.875rem;
  color: #111827;
  border-bottom: 1px solid #f3f4f6;
}

tbody tr:hover {
  background-color: #f9fafb;
}

.actions-column {
  width: 150px;
  text-align: center;
}

.actions-cell {
  text-align: center;
}

.text-center {
  text-align: center;
}

.empty-message {
  padding: 2rem;
  color: #6b7280;
}

.table-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 1.5rem;
  border-top: 1px solid #e5e7eb;
  background-color: #f9fafb;
}

.pagination-info {
  font-size: 0.875rem;
  color: #6b7280;
}

.pagination-controls {
  display: flex;
  gap: 0.5rem;
  align-items: center;
}

.btn-pagination {
  padding: 0.5rem 1rem;
  font-size: 0.875rem;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  background: white;
  color: #374151;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-pagination:hover:not(:disabled) {
  background-color: #f3f4f6;
}

.btn-pagination:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.page-numbers {
  display: flex;
  gap: 0.25rem;
}

.btn-page {
  padding: 0.5rem 0.75rem;
  font-size: 0.875rem;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  background: white;
  color: #374151;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-page:hover {
  background-color: #f3f4f6;
}

.btn-page.active {
  background-color: #2563eb;
  color: white;
  border-color: #2563eb;
}
</style>
