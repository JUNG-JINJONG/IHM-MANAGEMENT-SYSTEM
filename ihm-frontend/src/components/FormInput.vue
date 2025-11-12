<template>
  <div class="form-group">
    <label v-if="label" :for="inputId" class="form-label">
      {{ label }}
      <span v-if="required" class="required">*</span>
    </label>
    
    <!-- Text Input -->
    <input
      v-if="type === 'text' || type === 'email' || type === 'password' || type === 'number'"
      :id="inputId"
      :type="type"
      :value="modelValue"
      @input="$emit('update:modelValue', $event.target.value)"
      :placeholder="placeholder"
      :disabled="disabled"
      :required="required"
      class="form-input"
      :class="{ 'has-error': error }"
    />
    
    <!-- Textarea -->
    <textarea
      v-else-if="type === 'textarea'"
      :id="inputId"
      :value="modelValue"
      @input="$emit('update:modelValue', $event.target.value)"
      :placeholder="placeholder"
      :disabled="disabled"
      :required="required"
      :rows="rows"
      class="form-input form-textarea"
      :class="{ 'has-error': error }"
    ></textarea>
    
    <!-- Select -->
    <select
      v-else-if="type === 'select'"
      :id="inputId"
      :value="modelValue"
      @change="$emit('update:modelValue', $event.target.value)"
      :disabled="disabled"
      :required="required"
      class="form-input form-select"
      :class="{ 'has-error': error }"
    >
      <option value="" disabled>{{ placeholder || 'Select an option' }}</option>
      <option 
        v-for="option in options" 
        :key="getOptionValue(option)" 
        :value="getOptionValue(option)"
      >
        {{ getOptionLabel(option) }}
      </option>
    </select>
    
    <!-- Date Input -->
    <input
      v-else-if="type === 'date'"
      :id="inputId"
      type="date"
      :value="modelValue"
      @input="$emit('update:modelValue', $event.target.value)"
      :disabled="disabled"
      :required="required"
      class="form-input"
      :class="{ 'has-error': error }"
    />
    
    <!-- File Input -->
    <input
      v-else-if="type === 'file'"
      :id="inputId"
      type="file"
      @change="handleFileChange"
      :disabled="disabled"
      :required="required"
      :accept="accept"
      class="form-input form-file"
      :class="{ 'has-error': error }"
    />
    
    <p v-if="error" class="error-message">{{ error }}</p>
    <p v-else-if="hint" class="hint-message">{{ hint }}</p>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  modelValue: {
    type: [String, Number, File],
    default: ''
  },
  type: {
    type: String,
    default: 'text',
    validator: (value) => ['text', 'email', 'password', 'number', 'textarea', 'select', 'date', 'file'].includes(value)
  },
  label: {
    type: String,
    default: ''
  },
  placeholder: {
    type: String,
    default: ''
  },
  disabled: {
    type: Boolean,
    default: false
  },
  required: {
    type: Boolean,
    default: false
  },
  error: {
    type: String,
    default: ''
  },
  hint: {
    type: String,
    default: ''
  },
  options: {
    type: Array,
    default: () => []
  },
  optionValue: {
    type: String,
    default: 'value'
  },
  optionLabel: {
    type: String,
    default: 'label'
  },
  rows: {
    type: Number,
    default: 4
  },
  accept: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['update:modelValue'])

const inputId = computed(() => `input-${Math.random().toString(36).substr(2, 9)}`)

const getOptionValue = (option) => {
  return typeof option === 'object' ? option[props.optionValue] : option
}

const getOptionLabel = (option) => {
  return typeof option === 'object' ? option[props.optionLabel] : option
}

const handleFileChange = (event) => {
  const file = event.target.files[0]
  emit('update:modelValue', file)
}
</script>

<style scoped>
.form-group {
  margin-bottom: 1.25rem;
}

.form-label {
  display: block;
  font-size: 0.875rem;
  font-weight: 500;
  color: #374151;
  margin-bottom: 0.5rem;
}

.required {
  color: #dc2626;
  margin-left: 0.25rem;
}

.form-input {
  width: 100%;
  padding: 0.625rem 0.875rem;
  font-size: 0.875rem;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  transition: all 0.2s;
  background-color: white;
  color: #111827;
}

.form-input:focus {
  outline: none;
  border-color: #2563eb;
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
}

.form-input:disabled {
  background-color: #f3f4f6;
  cursor: not-allowed;
  color: #6b7280;
}

.form-input.has-error {
  border-color: #dc2626;
}

.form-input.has-error:focus {
  box-shadow: 0 0 0 3px rgba(220, 38, 38, 0.1);
}

.form-textarea {
  resize: vertical;
  min-height: 100px;
  font-family: inherit;
}

.form-select {
  cursor: pointer;
  appearance: none;
  background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 20 20'%3e%3cpath stroke='%236b7280' stroke-linecap='round' stroke-linejoin='round' stroke-width='1.5' d='M6 8l4 4 4-4'/%3e%3c/svg%3e");
  background-position: right 0.5rem center;
  background-repeat: no-repeat;
  background-size: 1.5em 1.5em;
  padding-right: 2.5rem;
}

.form-file {
  padding: 0.5rem;
}

.error-message {
  margin-top: 0.5rem;
  font-size: 0.875rem;
  color: #dc2626;
}

.hint-message {
  margin-top: 0.5rem;
  font-size: 0.875rem;
  color: #6b7280;
}
</style>
