<template>
  <div 
    class="p-4 border-t"
    :class="isDarkMode 
      ? 'border-transparent bg-black' 
      : 'border-transparent bg-white'"
  >
    <div class="flex gap-3">
      <textarea
        v-model="newMessageLocal"
        rows="2"
        placeholder="Type your message..."
        class="flex-1 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:border-transparent resize-none text-sm"
        :class="isDarkMode
          ? 'bg-neutral-800 border border-transparent text-gray-100 placeholder-gray-400 focus:ring-amber-500'
          : 'bg-gray-50 border border-transparent text-gray-900 placeholder-gray-400 focus:ring-amber-600'"
        @keydown.enter.exact.prevent="sendMessage"
      />
      <!-- File Attachment Button -->
      <label class="flex items-center justify-center px-3 rounded-lg cursor-pointer transition-colors"
        :class="isDarkMode
          ? 'bg-neutral-800 text-gray-400 hover:bg-neutral-700 hover:text-gray-300'
          : 'bg-gray-100 text-gray-500 hover:bg-gray-200 hover:text-gray-700'">
        <i-mdi-paperclip class="w-5 h-5" />
        <input type="file" class="hidden" @change="handleFileSelect" accept="image/*,.pdf,.doc,.docx,.txt" />
      </label>
      <!-- Send Button -->
      <button
        @click="sendMessage"
        class="text-white px-6 rounded-lg transition-all duration-200 shadow-lg font-medium flex items-center gap-2 active:scale-95"
        :class="isDarkMode
          ? 'bg-amber-600 hover:bg-amber-700'
          : 'bg-amber-700 hover:bg-amber-800'"
      >
        <i-mdi-send class="w-5 h-5" />
        Send
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, inject } from "vue"
import { toast } from 'vue-sonner'

const props = defineProps({
  modelValue: String,
})

const emit = defineEmits(['update:modelValue', 'send-message', 'file-selected'])

// Inject theme
const isDarkMode = inject('isDarkMode')

const newMessageLocal = ref(props.modelValue || "")

watch(() => props.modelValue, (val) => {
  newMessageLocal.value = val
})

const handleFileSelect = (event) => {
  const file = event.target.files?.[0]
  if (file) {
    emit('file-selected', file)
  }
  event.target.value = '' // Reset for re-selection
}

const sendMessage = () => {
  if (!newMessageLocal.value.trim()) {
    toast.warning('Please enter a message')
    return
  }

  // Emit the message to parent for handling
  emit('send-message', newMessageLocal.value)

  // Clear input
  newMessageLocal.value = ""
  emit('update:modelValue', "")
}
</script>