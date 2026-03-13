<template>
  <div class="fixed inset-0 z-50 flex items-center justify-center bg-black/30 backdrop-blur-sm" @click.self="$emit('close')">
    <div class="w-full max-w-md rounded-2xl shadow-2xl border p-6 space-y-4"
      :class="isDarkMode ? 'bg-neutral-900 border-neutral-800' : 'bg-white border-gray-200'">
      <div class="flex justify-between items-center">
        <h3 class="text-lg font-bold" :class="isDarkMode ? 'text-white' : 'text-gray-900'">
          {{ category ? 'Edit Category' : 'New Category' }}
        </h3>
        <button @click="$emit('close')" class="p-1 rounded-full hover:bg-gray-100 dark:hover:bg-neutral-800">
          <svg class="w-5 h-5" :class="isDarkMode ? 'text-gray-400' : 'text-gray-500'"
            xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
            <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/>
          </svg>
        </button>
      </div>

      <div class="space-y-4">
        <div v-if="parentName">
          <label class="block text-xs font-semibold mb-1" :class="isDarkMode ? 'text-gray-400' : 'text-gray-600'">Parent Category</label>
          <div class="px-3 py-2 rounded-lg text-sm" :class="isDarkMode ? 'bg-neutral-800 text-gray-300' : 'bg-gray-100 text-gray-600'">
            {{ parentName }}
          </div>
        </div>

        <div>
          <label class="block text-xs font-semibold mb-1" :class="isDarkMode ? 'text-gray-300' : 'text-gray-700'">Name *</label>
          <input v-model="form.name" type="text" placeholder="Category name..."
            class="w-full px-3 py-2 rounded-lg border text-sm focus:ring-2 focus:ring-amber-500 focus:border-transparent outline-none"
            :class="isDarkMode ? 'bg-neutral-800 border-neutral-700 text-white' : 'bg-gray-50 border-gray-200 text-gray-900'" />
        </div>

        <div class="flex items-center gap-3">
          <label class="flex items-center gap-2 cursor-pointer">
            <input type="checkbox" v-model="form.is_active" true-value="1" false-value="0"
              class="w-4 h-4 rounded text-amber-600 focus:ring-amber-500 border-gray-300" />
            <span class="text-sm" :class="isDarkMode ? 'text-gray-300' : 'text-gray-700'">Active</span>
          </label>
        </div>
      </div>

      <div class="flex justify-end gap-3 pt-2">
        <button @click="$emit('close')" class="px-4 py-2 text-sm font-medium rounded-lg transition-colors"
          :class="isDarkMode ? 'bg-neutral-800 text-gray-300 hover:bg-neutral-700' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'">
          Cancel
        </button>
        <button @click="handleSave" :disabled="!form.name.trim()"
          class="px-4 py-2 text-sm font-medium text-white rounded-lg transition-colors disabled:opacity-50"
          :class="isDarkMode ? 'bg-amber-600 hover:bg-amber-700' : 'bg-amber-700 hover:bg-amber-800'">
          {{ category ? 'Update' : 'Create' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, inject, onMounted } from 'vue'

const props = defineProps({
  category: { type: Object, default: null },
  parentName: { type: String, default: '' },
  parentId: { type: String, default: '' }
})

const emit = defineEmits(['save', 'close'])
const isDarkMode = inject('isDarkMode')

const form = reactive({
  name: '',
  is_active: '1'
})

onMounted(() => {
  if (props.category) {
    form.name = props.category.name || ''
    form.is_active = props.category.is_active || '1'
  }
})

const handleSave = () => {
  if (!form.name.trim()) return
  emit('save', { ...form })
}
</script>
