<template>
  <div class="page-container">
    <div class="page-header">
      <div>
        <h1>신고서 상세</h1>
        <p class="subtitle">신고서 정보를 확인합니다</p>
      </div>
    </div>

    <div class="form-card" v-if="declaration">
      <div class="form-section">
        <h3 class="section-title">신고 요청서 정보</h3>
        <div class="form-grid">
          <FormInput 
            :model-value="declaration.declaration_request_info?.order_number || '-'" 
            type="text" 
            label="신고 요청서 번호" 
            :disabled="true"
          />
          <FormInput 
            :model-value="declaration.declaration_request_info?.purchase_order?.title || '-'" 
            type="text" 
            label="제목" 
            :disabled="true"
          />
        </div>
      </div>

      <div class="form-section">
        <h3 class="section-title">신고서 정보</h3>
        <div class="form-grid">
          <FormInput 
            :model-value="declaration.declaration_number" 
            type="text" 
            label="신고서 번호" 
            :disabled="true"
          />
          <FormInput 
            :model-value="declaration.title || '-'" 
            type="text" 
            label="신고서 제목" 
            :disabled="true"
          />
          <FormInput 
            :model-value="getDeclarationTypeLabel(declaration.declaration_type)" 
            type="text" 
            label="신고서 유형" 
            :disabled="true"
          />
        </div>
      </div>

      <div class="form-section">
        <div class="section-header">
          <h3 class="section-title">유해물질 목록</h3>
        </div>
        
        <div v-if="declaration.hazardous_materials && declaration.hazardous_materials.length > 0">
          <div v-for="(material, index) in declaration.hazardous_materials" :key="index" class="material-card">
            <div class="material-header">
              <h4>물질 {{ index + 1 }}</h4>
            </div>
            <div class="form-grid">
              <FormInput :model-value="material.material_name || '-'" type="text" label="물질명" :disabled="true" />
              <FormInput :model-value="material.cas_number || '-'" type="text" label="CAS 번호" :disabled="true" />
              <FormInput :model-value="material.content_percentage || '-'" type="text" label="함유율 (%)" :disabled="true" />
              <FormInput :model-value="material.location_in_product || '-'" type="text" label="제품 내 위치" :disabled="true" />
            </div>
            <FormInput :model-value="material.remarks || '-'" type="textarea" label="비고" :rows="2" :disabled="true" />
          </div>
        </div>
        <div v-else class="empty-materials">
          유해물질 정보가 없습니다.
        </div>
      </div>

      <div class="form-actions">
        <button type="button" @click="router.back()" class="btn btn-secondary">목록으로</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '@/services/api'
import FormInput from '@/components/FormInput.vue'

const route = useRoute()
const router = useRouter()
const declaration = ref(null)

const getDeclarationTypeLabel = (type) => {
  const types = {
    'MD': 'MD (Material Declaration)',
    'SDoC': 'SDoC (Supplier Declaration of Conformity)'
  }
  return types[type] || type
}

const loadDeclaration = async () => {
  try {
    const response = await api.get(`/declarations/${route.params.id}/`)
    declaration.value = response.data
    console.log('Declaration loaded:', response.data)
  } catch (error) {
    console.error('Failed to load declaration:', error)
    alert('신고서를 불러오는데 실패했습니다.')
    router.push('/my-declarations')
  }
}

onMounted(() => loadDeclaration())
</script>

<style scoped>
.page-container { padding: 2rem; max-width: 1200px; margin: 0 auto; }
.page-header h1 { font-size: 1.875rem; font-weight: 700; color: #111827; margin: 0 0 0.5rem 0; }
.subtitle { color: #6b7280; font-size: 0.875rem; margin: 0; }
.form-card { background: white; padding: 2rem; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
.form-section { margin-bottom: 2rem; padding-bottom: 2rem; border-bottom: 1px solid #e5e7eb; }
.section-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem; }
.section-title { font-size: 1.125rem; font-weight: 600; color: #111827; margin: 0 0 1.5rem 0; }
.form-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem; }
.material-card { background: #f9fafb; padding: 1.5rem; border-radius: 8px; margin-bottom: 1rem; }
.material-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; }
.material-header h4 { margin: 0; color: #374151; font-size: 1rem; }
.empty-materials { text-align: center; padding: 2rem; color: #6b7280; }
.form-actions { display: flex; justify-content: flex-end; gap: 1rem; padding-top: 1.5rem; }
.btn { padding: 0.625rem 1.5rem; font-size: 0.875rem; font-weight: 500; border-radius: 6px; border: none; cursor: pointer; }
.btn-secondary { background-color: white; color: #374151; border: 1px solid #d1d5db; }
.btn-secondary:hover { background-color: #f9fafb; }
</style>
