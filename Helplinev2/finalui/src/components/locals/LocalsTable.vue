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
            Direction
          </th>
          <th class="px-4 py-4 text-xs font-semibold uppercase tracking-wider"
            :class="isDarkMode ? 'text-gray-300' : 'text-gray-700'">
            Extension
          </th>
          <th class="px-4 py-4 text-xs font-semibold uppercase tracking-wider"
            :class="isDarkMode ? 'text-gray-300' : 'text-gray-700'">
            Phone
          </th>
          <th class="px-4 py-4 text-xs font-semibold uppercase tracking-wider"
            :class="isDarkMode ? 'text-gray-300' : 'text-gray-700'">
            Wait Time
          </th>
          <th class="px-4 py-4 text-xs font-semibold uppercase tracking-wider"
            :class="isDarkMode ? 'text-gray-300' : 'text-gray-700'">
            Talk Time
          </th>
          <th class="px-4 py-4 text-xs font-semibold uppercase tracking-wider"
            :class="isDarkMode ? 'text-gray-300' : 'text-gray-700'">
            Hangup By
          </th>
          <th class="px-4 py-4 text-xs font-semibold uppercase tracking-wider"
            :class="isDarkMode ? 'text-gray-300' : 'text-gray-700'">
            Status
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

          <!-- Direction -->
          <td class="px-4 py-3">
            <span
              :class="['px-3 py-1 rounded-full text-xs font-semibold border', directionClass(row.direction)]">
              {{ row.direction === '1' ? 'Inbound' : row.direction === '2' ? 'Outbound' : 'N/A' }}
            </span>
          </td>

          <!-- Extension -->
          <td class="px-4 py-3 font-medium" :class="isDarkMode ? 'text-gray-200' : 'text-gray-900'">
            {{ row.extension || 'N/A' }}
          </td>

          <!-- Phone -->
          <td class="px-4 py-3" :class="isDarkMode ? 'text-gray-300' : 'text-gray-700'">
            {{ row.phone || 'N/A' }}
          </td>

          <!-- Wait Time -->
          <td class="px-4 py-3" :class="isDarkMode ? 'text-gray-400' : 'text-gray-600'">
            {{ formatDuration(row.waitTime) }}
          </td>

          <!-- Talk Time -->
          <td class="px-4 py-3" :class="isDarkMode ? 'text-gray-400' : 'text-gray-600'">
            {{ formatDuration(row.talkTime) }}
          </td>

          <!-- Hangup By -->
          <td class="px-4 py-3" :class="isDarkMode ? 'text-gray-400' : 'text-gray-600'">
            {{ getHangupReasonLabel(row.hangupBy) }}
          </td>

          <!-- Status -->
          <td class="px-4 py-3">
            <span :class="['px-3 py-1 rounded-full text-xs font-semibold border', statusClass(row.status)]">
              {{ getStatusLabel(row.status) }}
            </span>
          </td>
        </tr>
      </tbody>
    </table>

    <div v-if="!locals || locals.length === 0" class="p-4 text-center"
      :class="isDarkMode ? 'text-gray-500' : 'text-gray-500'">
      No internal call records found.
    </div>
  </div>
</template>

<script setup>
import { inject, computed } from 'vue'

const isDarkMode = inject('isDarkMode')

const props = defineProps({
  locals: { type: Array, required: true },
  localsStore: { type: Object, required: true }
})

// Map raw array rows to named fields using locals_k
const rows = computed(() => {
  if (!props.locals || !Array.isArray(props.locals)) return []

  const k = props.localsStore.locals_k || {}
  return props.locals.map(row => ({
    date: getVal(row, k, 'dth') || getVal(row, k, 'chan_ts') || getVal(row, k, 'date'),
    direction: getVal(row, k, 'vector') || getVal(row, k, 'direction'),
    extension: getVal(row, k, 'usr') || getVal(row, k, 'extension') || getVal(row, k, 'ext'),
    phone: getVal(row, k, 'phone') || getVal(row, k, 'callerid'),
    waitTime: getVal(row, k, 'wait_time') || getVal(row, k, 'wait_time_tot'),
    talkTime: getVal(row, k, 'talk_time') || getVal(row, k, 'duration'),
    hangupBy: getVal(row, k, 'hangup_reason') || getVal(row, k, 'hangup_by'),
    status: getVal(row, k, 'hangup_status') || getVal(row, k, 'hangup_status_txt') || getVal(row, k, 'status')
  }))
})

function getVal(row, keys, field) {
  const idx = keys[field]?.[0]
  return idx !== undefined ? row[idx] : null
}

const hangupReasonMap = {
  "": "",
  "phone": "Customer",
  "usr": "Extension",
  "ivr": "IVR",
  "net": "Network"
}

const hangupStatusMap = {
  "": "",
  "answered": "Answered",
  "abandoned": "Abandoned",
  "dump": "AgentDump",
  "ivr": "IVR",
  "missed": "Missed",
  "no-answer": "Flash",
  "noanswer": "Flash",
  "busy": "Busy",
  "networkerror": "Network Error",
  "voicemail": "Voicemail",
  "xfer_consult": "Consult",
  "xfer_noanswer": "Transfer No Answer",
  "xfer_offline": "Transfer Unavailable",
  "xfer_ok": "Transferred"
}

function getHangupReasonLabel(reason) {
  if (!reason) return 'N/A'
  return hangupReasonMap[reason] || reason
}

function getStatusLabel(status) {
  if (!status) return 'Unknown'
  return hangupStatusMap[status] || status
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

function directionClass(direction) {
  if (!direction) {
    return isDarkMode.value
      ? 'bg-gray-700/50 text-gray-400 border-transparent'
      : 'bg-gray-100 text-gray-600 border-transparent'
  }
  const d = String(direction)
  if (d === '1') {
    return isDarkMode.value
      ? 'bg-blue-600/20 text-blue-400 border-blue-600/30'
      : 'bg-blue-100 text-blue-700 border-blue-300'
  }
  if (d === '2') {
    return isDarkMode.value
      ? 'bg-green-600/20 text-green-400 border-green-600/30'
      : 'bg-green-100 text-green-700 border-green-300'
  }
  return isDarkMode.value
    ? 'bg-gray-700/50 text-gray-400 border-transparent'
    : 'bg-gray-100 text-gray-600 border-transparent'
}

function statusClass(status) {
  if (!status) {
    return isDarkMode.value
      ? 'bg-gray-700/50 text-gray-400 border-transparent'
      : 'bg-gray-100 text-gray-600 border-transparent'
  }
  const s = String(status).toLowerCase()

  if (s === 'answered' || s === 'xfer_ok') {
    return isDarkMode.value
      ? 'bg-green-600/20 text-green-400 border-green-600/30'
      : 'bg-green-100 text-green-700 border-green-300'
  }
  if (s === 'abandoned' || s === 'missed' || s === 'no-answer' || s === 'noanswer' || s === 'busy') {
    return isDarkMode.value
      ? 'bg-amber-600/20 text-amber-400 border-amber-600/30'
      : 'bg-amber-100 text-amber-700 border-amber-300'
  }
  if (s === 'dump') {
    return isDarkMode.value
      ? 'bg-red-600/20 text-red-400 border-red-600/30'
      : 'bg-red-100 text-red-700 border-red-300'
  }

  return isDarkMode.value
    ? 'bg-gray-700/50 text-gray-400 border-transparent'
    : 'bg-gray-100 text-gray-600 border-transparent'
}
</script>
