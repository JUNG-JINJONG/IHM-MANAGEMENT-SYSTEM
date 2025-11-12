<template>
  <div class="page-container">
    <div class="page-header">
      <div>
        <h1>신고서 작성</h1>
        <p class="subtitle">유해물질 신고서를 작성합니다</p>
      </div>
    </div>

    <div class="form-card">
      <form @submit.prevent="submitForm">
        <div class="form-section">
          <h3 class="section-title">신고 요청서 정보</h3>
          <div class="form-grid">
            <FormInput 
              v-model="purchaseOrderNumber" 
              type="text" 
              label="신고 요청서 번호" 
              :disabled="true"
              required 
            />
            <FormInput 
              v-model="purchaseOrderTitle" 
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
              v-model="form.declaration_number" 
              type="text" 
              label="신고서 번호" 
              :disabled="true"
            />
            <FormInput 
              v-model="form.title" 
              type="text" 
              label="신고서 제목" 
              placeholder="신고서 제목을 입력하세요"
            />
            <FormInput v-model="form.declaration_type" type="select" label="신고서 유형" :options="declarationTypeOptions" option-value="value" option-label="label" />
            <!-- <FormInput v-model="form.item_name" type="text" label="품목명" placeholder="품목명을 입력하세요" /> -->
            <!-- <FormInput v-model="form.manufacturer" type="text" label="제조사" placeholder="제조사를 입력하세요" /> -->
            <!-- <FormInput v-model="form.model_number" type="text" label="모델번호" placeholder="모델번호를 입력하세요" /> -->
            <!-- <FormInput v-model="form.compliance_status" type="select" label="적합성 상태" :options="complianceOptions" option-value="value" option-label="label" /> -->
            <!-- <FormInput v-model="form.certification_number" type="text" label="인증번호" placeholder="인증번호를 입력하세요" /> -->
            <!-- <FormInput v-model="form.supplier_signature" type="text" label="전자서명" placeholder="서명을 입력하세요" /> -->
            <!-- <FormInput v-model="form.supplier_name" type="text" label="서명자명" placeholder="서명자명을 입력하세요" /> -->
            <!-- <FormInput v-model="form.signature_date" type="date" label="서명일" /> -->
          </div>
        </div>

        <div class="form-section">
          <div class="section-header">
            <h3 class="section-title">유해물질 목록</h3>
            <button type="button" @click="addMaterial" class="btn btn-secondary btn-sm">물질 추가</button>
          </div>
          
          <div v-for="(material, index) in form.materials" :key="index" class="material-card">
            <div class="material-header">
              <h4>물질 {{ index + 1 }}</h4>
              <button type="button" @click="removeMaterial(index)" class="btn-remove">제거</button>
            </div>
            <div class="form-grid">
              <FormInput v-model="material.material_name" type="text" label="물질명" />
              <FormInput v-model="material.cas_number" type="text" label="CAS 번호" />
              <FormInput v-model="material.content_percentage" type="number" label="함유율 (%)" step="0.01" />
              <FormInput v-model="material.location_in_product" type="text" label="제품 내 위치" />
            </div>
            <FormInput v-model="material.remarks" type="textarea" label="비고" :rows="2" />
          </div>
        </div>

        <div class="form-actions">
          <button type="button" @click="router.back()" class="btn btn-secondary">취소</button>
          <button type="submit" class="btn btn-primary" :disabled="submitting">
            {{ submitting ? '생성 중...' : '신고서 생성' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import api from '@/services/api'
import FormInput from '@/components/FormInput.vue'

const router = useRouter()
const route = useRoute()
const submitting = ref(false)
const purchaseOrderNumber = ref('')
const purchaseOrderTitle = ref('')

const declarationTypeOptions = [
  { value: 'MD', label: 'MD (Material Declaration)' },
  { value: 'SDoC', label: 'SDoC (Supplier Declaration of Conformity)' }
]

const complianceOptions = [
  { value: 'compliant', label: '적합' },
  { value: 'non_compliant', label: '부적합' },
  { value: 'pending', label: '검토중' }
]

// 신고서 번호 자동 생성
const generateDeclarationNumber = () => {
  const now = new Date()
  const year = now.getFullYear()
  const month = String(now.getMonth() + 1).padStart(2, '0')
  const day = String(now.getDate()).padStart(2, '0')
  const random = Math.floor(Math.random() * 10000).toString().padStart(4, '0')
  return `DEC-${year}${month}${day}-${random}`
}

const form = reactive({
  declaration_number: generateDeclarationNumber(),
  title: '',
  declaration_type: 'MD',
  item_name: '',
  manufacturer: '',
  model_number: '',
  compliance_status: 'pending',
  certification_number: '',
  supplier_signature: '',
  supplier_name: '',
  signature_date: new Date().toISOString().split('T')[0],
  purchase_order: '',
  materials: [{ material_name: '', cas_number: '', content_percentage: '', location_in_product: '', remarks: '' }]
})

const addMaterial = () => {
  form.materials.push({ material_name: '', cas_number: '', content_percentage: '', location_in_product: '', remarks: '' })
}

const removeMaterial = (index) => {
  if (form.materials.length > 1) {
    form.materials.splice(index, 1)
  }
}

const loadPurchaseOrder = async () => {
  try {
    // URL에서 purchase_order ID 가져오기
    const purchaseOrderId = route.query.purchase_order
    if (!purchaseOrderId) {
      alert('신고 요청서 정보가 없습니다.')
      router.push('/purchase-orders')
      return
    }

    form.purchase_order = purchaseOrderId
    
    // PurchaseOrder 상세 정보 가져오기
    const response = await api.get(`/purchase-orders/${purchaseOrderId}/`)
    purchaseOrderNumber.value = response.data.order_number
    purchaseOrderTitle.value = response.data.title
  } catch (error) {
    console.error('Failed to load purchase order:', error)
    alert('신고 요청서를 불러오는데 실패했습니다.')
    router.push('/purchase-orders')
  }
}

const submitForm = async () => {
  submitting.value = true
  try {
    await api.post('/declarations/', {
      purchase_order: form.purchase_order,
      declaration_number: form.declaration_number,
      title: form.title,
      declaration_type: form.declaration_type,
      item_name: form.item_name,
      manufacturer: form.manufacturer,
      model_number: form.model_number,
      compliance_status: form.compliance_status,
      certification_number: form.certification_number,
      supplier_signature: form.supplier_signature,
      supplier_name: form.supplier_name,
      signature_date: form.signature_date,
      hazardous_materials: form.materials.map(m => ({
        material_name: m.material_name,
        cas_number: m.cas_number,
        content_percentage: m.content_percentage ? parseFloat(m.content_percentage) : null,
        location_in_product: m.location_in_product,
        remarks: m.remarks
      }))
    })
    alert('신고서가 생성되었습니다')
    router.push('/my-declarations')
  } catch (error) {
    console.error('===== 신고서 생성 실패 =====')
    console.error('Full Error:', error)
    console.error('Error Response Data:', JSON.stringify(error.response?.data, null, 2))
    console.error('Hazardous Materials Errors:', error.response?.data?.hazardous_materials)
    console.error('Request Data:', {
      purchase_order: form.purchase_order,
      declaration_number: form.declaration_number,
      title: form.title,
      declaration_type: form.declaration_type,
      hazardous_materials: form.materials.map(m => ({
        material_name: m.material_name,
        cas_number: m.cas_number,
        content_percentage: m.content_percentage,
        location_in_product: m.location_in_product,
        remarks: m.remarks
      }))
    })
    console.error('========================')
    alert('신고서 생성에 실패했습니다. 콘솔을 확인해주세요.')
  } finally {
    submitting.value = false
  }
}

onMounted(() => loadPurchaseOrder())
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
.btn-remove { background: #dc2626; color: white; border: none; padding: 0.375rem 0.75rem; border-radius: 4px; cursor: pointer; font-size: 0.875rem; }
.btn-remove:hover { background: #b91c1c; }
.form-actions { display: flex; justify-content: flex-end; gap: 1rem; padding-top: 1.5rem; }
.btn { padding: 0.625rem 1.5rem; font-size: 0.875rem; font-weight: 500; border-radius: 6px; border: none; cursor: pointer; }
.btn:disabled { opacity: 0.6; cursor: not-allowed; }
.btn-primary { background-color: #2563eb; color: white; }
.btn-primary:hover:not(:disabled) { background-color: #1d4ed8; }
.btn-secondary { background-color: white; color: #374151; border: 1px solid #d1d5db; }
.btn-secondary:hover { background-color: #f9fafb; }
.btn-sm { padding: 0.5rem 1rem; font-size: 0.813rem; }
</style>
