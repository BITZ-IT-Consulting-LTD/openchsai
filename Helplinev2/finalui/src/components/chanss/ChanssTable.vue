<template>
  <div class="rounded-xl shadow-xl overflow-auto border" :class="isDarkMode
    ? 'bg-black border-transparent'
    : 'bg-white border-transparent'">
    <table class="min-w-full text-sm text-left">
      <thead class="border-b" :class="isDarkMode
        ? 'bg-black/60 border-transparent'
        : 'bg-gray-50 border-transparent'">
        <tr>
          <th class="px-4 py-4 text-xs font-semibold uppercase tracking-wider"
            :class="isDarkMode ? 'text-gray-300' : 'text-gray-700'">
            Date
          </th>
          <th class="px-4 py-4 text-xs font-semibold uppercase tracking-wider"
            :class="isDarkMode ? 'text-gray-300' : 'text-gray-700'">
            Extension
          </th>
          <th class="px-4 py-4 text-xs font-semibold uppercase tracking-wider"
            :class="isDarkMode ? 'text-gray-300' : 'text-gray-700'">
            Last Call
          </th>
          <th class="px-4 py-4 text-xs font-semibold uppercase tracking-wider"
            :class="isDarkMode ? 'text-gray-300' : 'text-gray-700'">
            End Time
          </th>
          <th class="px-4 py-4 text-xs font-semibold uppercase tracking-wider"
            :class="isDarkMode ? 'text-gray-300' : 'text-gray-700'">
            Duration
          </th>
          <th class="px-4 py-4 text-xs font-semibold uppercase tracking-wider"
            :class="isDarkMode ? 'text-gray-300' : 'text-gray-700'">
            Occupied
          </th>
          <th class="px-4 py-4 text-xs font-semibold uppercase tracking-wider"
            :class="isDarkMode ? 'text-gray-300' : 'text-gray-700'">
            Occupancy Rate
          </th>
        </tr>
      </thead>

      <tbody class="divide-y" :class="isDarkMode ? 'divide-gray-700' : 'divide-gray-200'">
        <tr v-for="(row, idx) in rows" :key="idx" :class="[
          'transition-all duration-200',
          isDarkMode
            ? 'hover:bg-gray-700/30'
            : 'hover:bg-gray-50'
        ]">
          <!-- Date -->
          <td class="px-4 py-3" :class="isDarkMode ? 'text-gray-300' : 'text-gray-700'">
            {{ row.date ? formatDateTime(row.date) : 'N/A' }}
          </td>

          <!-- Extension -->
          <td class="px-4 py-3 font-medium" :class="isDarkMode ? 'text-gray-200' : 'text-gray-900'">
            {{ row.extension || 'N/A' }}
          </td>

          <!-- Last Call -->
          <td class="px-4 py-3" :class="isDarkMode ? 'text-gray-300' : 'text-gray-700'">
            {{ row.lastCall ? formatDateTime(row.lastCall) : 'N/A' }}
          </td>

          <!-- End Time -->
          <td class="px-4 py-3" :class="isDarkMode ? 'text-gray-300' : 'text-gray-700'">
            {{ row.endTime ? formatDateTime(row.endTime) : 'N/A' }}
          </td>

          <!-- Duration -->
          <td class="px-4 py-3" :class="isDarkMode ? 'text-gray-400' : 'text-gray-600'">
            {{ formatDuration(row.duration) }}
          </td>

          <!-- Occupied -->
          <td class="px-4 py-3" :class="isDarkMode ? 'text-gray-400' : 'text-gray-600'">
            {{ formatDuration(row.occupied) }}
          </td>

          <!-- Occupancy Rate -->
          <td class="px-4 py-3">
            <span :class="['px-3 py-1 rounded-full text-xs font-semibold border', occupancyClass(row.occupancyRate)]">
              {{ row.occupancyRate ? `${row.occupancyRate}%` : 'N/A' }}
            </span>
          </td>
        </tr>
      </tbody>
    </table>

    <div v-if="!chanss || chanss.length === 0" class="p-4 text-center"
      :class="isDarkMode ? 'text-gray-500' : 'text-gray-500'">
      No agent availability records found.
    </div>
  </div>
</template>

<script setup>
import { inject, computed } from 'vue'

const isDarkMode = inject('isDarkMode')

const props = defineProps({
  chanss: { type: Array, required: true },
  chanssStore: { type: Object, required: true }
})

// Map raw array rows to named fields using chanss_k
const rows = computed(() => {
  if (!props.chanss || !Array.isArray(props.chanss)) return []

  const k = props.chanssStore.chanss_k || {}
  return props.chanss.map(row => ({
    date: getVal(row, k, 'dth') || getVal(row, k, 'chan_ts') || getVal(row, k, 'date'),
    extension: getVal(row, k, 'usr') || getVal(row, k, 'extension') || getVal(row, k, 'ext'),
    lastCall: getVal(row, k, 'last_call') || getVal(row, k, 'last_call_ts'),
    endTime: getVal(row, k, 'end_time') || getVal(row, k, 'end_ts'),
    duration: getVal(row, k, 'duration') || getVal(row, k, 'dur'),
    occupied: getVal(row, k, 'occupied') || getVal(row, k, 'occ'),
    occupancyRate: getVal(row, k, 'occupancy_rate') || getVal(row, k, 'occ_rate') || getVal(row, k, 'rate')
  }))
})

function getVal(row, keys, field) {
  const idx = keys[field]?.[0]
  return idx !== undefined ? row[idx] : null
}

function formatDateTime(timestamp) {
  if (!timestamp || timestamp === '0') return 'N/A'
  const ts = parseInt(timestamp)
  if (isNaN(ts)) return timestamp
  const date = new Date(ts * 1000)
  return date.toLocaleString('en-GB', {
    day: '2-digit',
    month: 'short',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    hour12: true
  })
}

function formatDuration(value) {
  if (!value || value === '0') return '0.00'
  const num = parseFloat(value)
  const minutes = num / 100
  return minutes.toFixed(2)
}

function occupancyClass(rate) {
  if (!rate) {
    return isDarkMode.value
      ? 'bg-gray-700/50 text-gray-400 border-transparent'
      : 'bg-gray-100 text-gray-600 border-transparent'
  }
  const r = parseFloat(rate)
  if (r >= 80) {
    return isDarkMode.value
      ? 'bg-green-600/20 text-green-400 border-green-600/30'
      : 'bg-green-100 text-green-700 border-green-300'
  }
  if (r >= 50) {
    return isDarkMode.value
      ? 'bg-amber-600/20 text-amber-400 border-amber-600/30'
      : 'bg-amber-100 text-amber-700 border-amber-300'
  }
  return isDarkMode.value
    ? 'bg-red-600/20 text-red-400 border-red-600/30'
    : 'bg-red-100 text-red-700 border-red-300'
}
</script>
