<template>
  <div class="loading-spinner" :class="sizeClass">
    <div class="spinner"></div>
    <p v-if="message" class="loading-message">{{ message }}</p>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  size: {
    type: String,
    default: 'medium',
    validator: (value) => ['small', 'medium', 'large'].includes(value)
  },
  message: {
    type: String,
    default: ''
  }
})

const sizeClass = computed(() => `loading-${props.size}`)
</script>

<style scoped>
.loading-spinner {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem;
}

.spinner {
  border: 3px solid #f3f4f6;
  border-top: 3px solid #2563eb;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.loading-small .spinner {
  width: 24px;
  height: 24px;
  border-width: 2px;
}

.loading-medium .spinner {
  width: 40px;
  height: 40px;
}

.loading-large .spinner {
  width: 60px;
  height: 60px;
  border-width: 4px;
}

.loading-message {
  margin-top: 1rem;
  color: #6b7280;
  font-size: 0.875rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>
