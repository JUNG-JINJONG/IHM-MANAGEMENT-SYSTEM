<template>
  <div class="page-container">
    <div class="page-header">
      <h1>{{ isEdit ? 'Edit Ship' : 'Add Ship' }}</h1>
    </div>

    <div class="form-card">
      <form @submit.prevent="submitForm">
        <div class="form-grid">
          <FormInput v-model="form.name" type="text" label="Ship Name" required />
          <FormInput v-model="form.imo_number" type="text" label="IMO Number" required />
          <FormInput v-model="form.flag" type="text" label="Flag" required />
          <FormInput v-model="form.type" type="text" label="Ship Type" required />
          <FormInput v-model="form.built_year" type="number" label="Built Year" />
          <FormInput v-model="form.gross_tonnage" type="number" label="Gross Tonnage" />
        </div>
        <FormInput v-model="form.classification_society" type="text" label="Classification Society" />
        
        <div class="form-actions">
          <button type="button" @click="router.back()" class="btn btn-secondary">Cancel</button>
          <button type="submit" class="btn btn-primary" :disabled="submitting">
            {{ submitting ? 'Saving...' : (isEdit ? 'Update' : 'Create') }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import api from '@/services/api'
import FormInput from '@/components/FormInput.vue'

const router = useRouter()
const route = useRoute()
const submitting = ref(false)
const isEdit = computed(() => !!route.params.id)

const form = reactive({
  name: '',
  imo_number: '',
  flag: '',
  type: '',
  built_year: '',
  gross_tonnage: '',
  classification_society: ''
})

const loadShip = async () => {
  if (!isEdit.value) return
  try {
    const response = await api.get(`/ships/${route.params.id}/`)
    Object.assign(form, response.data)
  } catch (error) {
    console.error('Failed to load ship:', error)
  }
}

const submitForm = async () => {
  submitting.value = true
  try {
    if (isEdit.value) {
      await api.put(`/ships/${route.params.id}/`, form)
      alert('Ship updated successfully')
    } else {
      await api.post('/ships/', form)
      alert('Ship created successfully')
    }
    router.push('/ships')
  } catch (error) {
    console.error('Failed to save ship:', error)
    alert('Failed to save ship')
  } finally {
    submitting.value = false
  }
}

onMounted(() => loadShip())
</script>

<style scoped>
.page-container { padding: 2rem; max-width: 1000px; margin: 0 auto; }
.page-header h1 { font-size: 1.875rem; font-weight: 700; color: #111827; margin: 0 0 2rem 0; }
.form-card { background: white; padding: 2rem; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
.form-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem; margin-bottom: 1rem; }
.form-actions { display: flex; justify-content: flex-end; gap: 1rem; margin-top: 2rem; padding-top: 2rem; border-top: 1px solid #e5e7eb; }
.btn { padding: 0.625rem 1.5rem; font-size: 0.875rem; font-weight: 500; border-radius: 6px; border: none; cursor: pointer; }
.btn:disabled { opacity: 0.6; cursor: not-allowed; }
.btn-primary { background-color: #2563eb; color: white; }
.btn-primary:hover:not(:disabled) { background-color: #1d4ed8; }
.btn-secondary { background-color: white; color: #374151; border: 1px solid #d1d5db; }
.btn-secondary:hover { background-color: #f9fafb; }
</style>
