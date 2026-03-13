<template>
  <div class="space-y-4 p-4 rounded-xl border" :class="isDarkMode ? 'bg-neutral-900 border-neutral-800' : 'bg-white border-gray-100'">
    <h3 class="text-sm font-bold uppercase tracking-wider" :class="isDarkMode ? 'text-gray-400' : 'text-gray-600'">Filters</h3>

    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <!-- Date Range From -->
      <div>
        <label class="block text-xs font-semibold mb-1" :class="isDarkMode ? 'text-gray-300' : 'text-gray-700'">From</label>
        <input type="date" v-model="filters.date_from" class="w-full px-3 py-2 rounded-lg border text-sm"
          :class="isDarkMode ? 'bg-neutral-800 border-neutral-700 text-white' : 'bg-gray-50 border-gray-200 text-gray-900'" />
      </div>

      <!-- Date Range To -->
      <div>
        <label class="block text-xs font-semibold mb-1" :class="isDarkMode ? 'text-gray-300' : 'text-gray-700'">To</label>
        <input type="date" v-model="filters.date_to" class="w-full px-3 py-2 rounded-lg border text-sm"
          :class="isDarkMode ? 'bg-neutral-800 border-neutral-700 text-white' : 'bg-gray-50 border-gray-200 text-gray-900'" />
      </div>

      <!-- Direction -->
      <div>
        <label class="block text-xs font-semibold mb-1" :class="isDarkMode ? 'text-gray-300' : 'text-gray-700'">Direction</label>
        <select v-model="filters.direction" class="w-full px-3 py-2 rounded-lg border text-sm"
          :class="isDarkMode ? 'bg-neutral-800 border-neutral-700 text-white' : 'bg-gray-50 border-gray-200 text-gray-900'">
          <option value="">All</option>
          <option value="inbound">Inbound</option>
          <option value="outbound">Outbound</option>
        </select>
      </div>

      <!-- Phone -->
      <div>
        <label class="block text-xs font-semibold mb-1" :class="isDarkMode ? 'text-gray-300' : 'text-gray-700'">Phone</label>
        <input type="text" v-model="filters.phone" placeholder="Phone number..."
          class="w-full px-3 py-2 rounded-lg border text-sm"
          :class="isDarkMode ? 'bg-neutral-800 border-neutral-700 text-white placeholder-gray-500' : 'bg-gray-50 border-gray-200 text-gray-900 placeholder-gray-400'" />
      </div>

      <!-- Extension -->
      <div>
        <label class="block text-xs font-semibold mb-1" :class="isDarkMode ? 'text-gray-300' : 'text-gray-700'">Extension</label>
        <input type="text" v-model="filters.extension" placeholder="Extension..."
          class="w-full px-3 py-2 rounded-lg border text-sm"
          :class="isDarkMode ? 'bg-neutral-800 border-neutral-700 text-white placeholder-gray-500' : 'bg-gray-50 border-gray-200 text-gray-900 placeholder-gray-400'" />
      </div>

      <!-- Source -->
      <div>
        <label class="block text-xs font-semibold mb-1" :class="isDarkMode ? 'text-gray-300' : 'text-gray-700'">Source</label>
        <select v-model="filters.source" class="w-full px-3 py-2 rounded-lg border text-sm"
          :class="isDarkMode ? 'bg-neutral-800 border-neutral-700 text-white' : 'bg-gray-50 border-gray-200 text-gray-900'">
          <option value="">All Sources</option>
          <option value="whatsapp">WhatsApp</option>
          <option value="sms">SMS</option>
          <option value="email">Email</option>
          <option value="webchat">Web Chat</option>
        </select>
      </div>

      <!-- Hangup Status -->
      <div>
        <label class="block text-xs font-semibold mb-1" :class="isDarkMode ? 'text-gray-300' : 'text-gray-700'">Hangup Status</label>
        <select v-model="filters.hangup_status" class="w-full px-3 py-2 rounded-lg border text-sm"
          :class="isDarkMode ? 'bg-neutral-800 border-neutral-700 text-white' : 'bg-gray-50 border-gray-200 text-gray-900'">
          <option value="">All</option>
          <option value="answered">Answered</option>
          <option value="abandoned">Abandoned</option>
          <option value="missed">Missed</option>
          <option value="busy">Busy</option>
          <option value="voicemail">Voicemail</option>
        </select>
      </div>
    </div>

    <div class="flex justify-end gap-2 pt-2">
      <button @click="clearFilters" class="px-4 py-2 text-xs font-semibold rounded-lg transition-colors"
        :class="isDarkMode ? 'bg-neutral-800 text-gray-300 hover:bg-neutral-700' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'">
        Clear
      </button>
      <button @click="applyFilters" class="px-4 py-2 text-xs font-semibold text-white rounded-lg transition-colors"
        :class="isDarkMode ? 'bg-amber-600 hover:bg-amber-700' : 'bg-amber-700 hover:bg-amber-800'">
        Apply
      </button>
    </div>
  </div>
</template>

<script setup>
import { reactive, inject } from 'vue'

const isDarkMode = inject('isDarkMode')
const emit = defineEmits(['apply', 'clear'])

const filters = reactive({
  date_from: '',
  date_to: '',
  direction: '',
  phone: '',
  extension: '',
  source: '',
  hangup_status: ''
})

const applyFilters = () => {
  const activeFilters = {}
  Object.entries(filters).forEach(([key, value]) => {
    if (value) activeFilters[key] = value
  })
  emit('apply', activeFilters)
}

const clearFilters = () => {
  Object.keys(filters).forEach(key => filters[key] = '')
  emit('clear')
}
</script>
