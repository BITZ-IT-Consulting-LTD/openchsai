<template>
  <div 
    class="w-full rounded-lg p-4 shadow-xl border mb-4"
    :class="isDarkMode 
      ? 'bg-black border-transparent' 
      : 'bg-white border-transparent'"
  >
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">

      <!-- Date Range From -->
      <div class="flex flex-col">
        <label class="text-sm font-medium mb-1" :class="isDarkMode ? 'text-gray-300' : 'text-gray-700'">
          From Date
        </label>
        <input type="date" v-model="filters.dateFrom"
          class="rounded px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:border-transparent" :class="isDarkMode
            ? 'bg-neutral-800 border border-transparent text-gray-100 focus:ring-amber-500'
            : 'bg-gray-50 border border-transparent text-gray-900 focus:ring-amber-600'" />
      </div>

      <!-- Date Range To -->
      <div class="flex flex-col">
        <label class="text-sm font-medium mb-1" :class="isDarkMode ? 'text-gray-300' : 'text-gray-700'">
          To Date
        </label>
        <input type="date" v-model="filters.dateTo"
          class="rounded px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:border-transparent" :class="isDarkMode
            ? 'bg-neutral-800 border border-transparent text-gray-100 focus:ring-amber-500'
            : 'bg-gray-50 border border-transparent text-gray-900 focus:ring-amber-600'" />
      </div>

      <!-- Direction -->
      <div class="flex flex-col">
        <label class="text-sm font-medium mb-1" :class="isDarkMode ? 'text-gray-300' : 'text-gray-700'">
          Direction
        </label>
        <select v-model="filters.direction"
          class="rounded px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:border-transparent" :class="isDarkMode
            ? 'bg-neutral-800 border border-transparent text-gray-100 focus:ring-amber-500'
            : 'bg-gray-50 border border-transparent text-gray-900 focus:ring-amber-600'">
          <option value="">All</option>
          <option value="1">Inbound</option>
          <option value="2">Outbound</option>
        </select>
      </div>

      <!-- Phone Number -->
      <div class="flex flex-col">
        <label class="text-sm font-medium mb-1" :class="isDarkMode ? 'text-gray-300' : 'text-gray-700'">
          Phone
        </label>
        <input type="text" v-model="filters.phone" placeholder="Enter phone number"
          class="rounded px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:border-transparent" :class="isDarkMode
            ? 'bg-neutral-800 border border-transparent text-gray-100 placeholder-gray-500 focus:ring-amber-500'
            : 'bg-gray-50 border border-transparent text-gray-900 placeholder-gray-400 focus:ring-amber-600'" />
      </div>

      <!-- Extension -->
      <div class="flex flex-col">
        <label class="text-sm font-medium mb-1" :class="isDarkMode ? 'text-gray-300' : 'text-gray-700'">
          Extension
        </label>
        <input type="text" v-model="filters.extension" placeholder="Enter extension"
          class="rounded px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:border-transparent" :class="isDarkMode
            ? 'bg-neutral-800 border border-transparent text-gray-100 placeholder-gray-500 focus:ring-amber-500'
            : 'bg-gray-50 border border-transparent text-gray-900 placeholder-gray-400 focus:ring-amber-600'" />
      </div>

      <!-- Hangup Status -->
      <div class="flex flex-col">
        <label class="text-sm font-medium mb-1" :class="isDarkMode ? 'text-gray-300' : 'text-gray-700'">
          Hangup Status
        </label>
        <select v-model="filters.hangupStatus"
          class="rounded px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:border-transparent" :class="isDarkMode
            ? 'bg-neutral-800 border border-transparent text-gray-100 focus:ring-amber-500'
            : 'bg-gray-50 border border-transparent text-gray-900 focus:ring-amber-600'">
          <option value="">All</option>
          <option value="answered">Answered</option>
          <option value="abandoned">Abandoned</option>
          <option value="dump">AgentDump</option>
          <option value="missed">Missed</option>
          <option value="ivr">IVR</option>
          <option value="noanswer">Flash</option>
          <option value="busy">Busy</option>
          <option value="networkerror">Network Error</option>
          <option value="voicemail">Voicemail</option>
          <option value="xfer_consult">Consult</option>
          <option value="xfer_noanswer">Transfer No Answer</option>
          <option value="xfer_offline">Transfer Unavailable</option>
          <option value="xfer_ok">Transferred</option>
          <option value="sched">Sched</option>
          <option value="reattempt">Reattempt</option>
        </select>
      </div>

      <!-- Hangup By -->
      <div class="flex flex-col">
        <label class="text-sm font-medium mb-1" :class="isDarkMode ? 'text-gray-300' : 'text-gray-700'">
          Hangup By
        </label>
        <select v-model="filters.hangupBy"
          class="rounded px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:border-transparent" :class="isDarkMode
            ? 'bg-neutral-800 border border-transparent text-gray-100 focus:ring-amber-500'
            : 'bg-gray-50 border border-transparent text-gray-900 focus:ring-amber-600'">
          <option value="">All</option>
          <option value="phone">Customer</option>
          <option value="usr">Extension</option>
          <option value="ivr">IVR</option>
          <option value="net">Network</option>
        </select>
      </div>

      <!-- QA Score -->
      <div class="flex flex-col">
        <label class="text-sm font-medium mb-1" :class="isDarkMode ? 'text-gray-300' : 'text-gray-700'">
          Min QA Score
        </label>
        <input type="number" v-model="filters.qaScore" placeholder="0-100" min="0" max="100"
          class="rounded px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:border-transparent" :class="isDarkMode
            ? 'bg-neutral-800 border border-transparent text-gray-100 placeholder-gray-500 focus:ring-amber-500'
            : 'bg-gray-50 border border-transparent text-gray-900 placeholder-gray-400 focus:ring-amber-600'" />
      </div>

    </div>

    <!-- Collapsible: Case Filters -->
    <div class="mt-4">
      <button @click="showCaseFilters = !showCaseFilters"
        class="text-xs font-semibold flex items-center gap-1 transition-colors"
        :class="isDarkMode ? 'text-amber-500 hover:text-amber-400' : 'text-amber-700 hover:text-amber-800'">
        <component :is="showCaseFilters ? 'i-mdi-chevron-up' : 'i-mdi-chevron-down'" class="w-4 h-4" />
        {{ showCaseFilters ? 'Hide Case Filters' : 'Show Case Filters' }}
      </button>
      <Transition name="fade">
        <div v-if="showCaseFilters" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mt-3">
          <!-- Case ID -->
          <div class="flex flex-col">
            <label class="text-sm font-medium mb-1" :class="isDarkMode ? 'text-gray-300' : 'text-gray-700'">
              Case ID
            </label>
            <input type="text" v-model="filters.caseId" placeholder="Enter case ID"
              class="rounded px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:border-transparent" :class="isDarkMode
                ? 'bg-neutral-800 border border-transparent text-gray-100 placeholder-gray-500 focus:ring-amber-500'
                : 'bg-gray-50 border border-transparent text-gray-900 placeholder-gray-400 focus:ring-amber-600'" />
          </div>
        </div>
      </Transition>
    </div>

    <!-- Collapsible: Reporter Filters -->
    <div class="mt-4">
      <button @click="showReporterFilters = !showReporterFilters"
        class="text-xs font-semibold flex items-center gap-1 transition-colors"
        :class="isDarkMode ? 'text-amber-500 hover:text-amber-400' : 'text-amber-700 hover:text-amber-800'">
        <component :is="showReporterFilters ? 'i-mdi-chevron-up' : 'i-mdi-chevron-down'" class="w-4 h-4" />
        {{ showReporterFilters ? 'Hide Reporter Filters' : 'Show Reporter Filters' }}
      </button>
      <Transition name="fade">
        <div v-if="showReporterFilters" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mt-3">
          <!-- Reporter Name -->
          <div class="flex flex-col">
            <label class="text-sm font-medium mb-1" :class="isDarkMode ? 'text-gray-300' : 'text-gray-700'">
              Name
            </label>
            <input type="text" v-model="filters.reporterName" placeholder="Reporter name"
              class="rounded px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:border-transparent" :class="isDarkMode
                ? 'bg-neutral-800 border border-transparent text-gray-100 placeholder-gray-500 focus:ring-amber-500'
                : 'bg-gray-50 border border-transparent text-gray-900 placeholder-gray-400 focus:ring-amber-600'" />
          </div>

          <!-- Reporter Phone -->
          <div class="flex flex-col">
            <label class="text-sm font-medium mb-1" :class="isDarkMode ? 'text-gray-300' : 'text-gray-700'">
              Phone
            </label>
            <input type="text" v-model="filters.reporterPhone" placeholder="Reporter phone"
              class="rounded px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:border-transparent" :class="isDarkMode
                ? 'bg-neutral-800 border border-transparent text-gray-100 placeholder-gray-500 focus:ring-amber-500'
                : 'bg-gray-50 border border-transparent text-gray-900 placeholder-gray-400 focus:ring-amber-600'" />
          </div>

          <!-- Reporter Age -->
          <div class="flex flex-col">
            <label class="text-sm font-medium mb-1" :class="isDarkMode ? 'text-gray-300' : 'text-gray-700'">
              Age
            </label>
            <input type="number" v-model="filters.reporterAge" placeholder="Age" min="0" max="150"
              class="rounded px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:border-transparent" :class="isDarkMode
                ? 'bg-neutral-800 border border-transparent text-gray-100 placeholder-gray-500 focus:ring-amber-500'
                : 'bg-gray-50 border border-transparent text-gray-900 placeholder-gray-400 focus:ring-amber-600'" />
          </div>

          <!-- Reporter Sex -->
          <div class="flex flex-col">
            <TaxonomySelect v-model="filters.reporterSex" label="Sex" placeholder="Select sex"
              root-key="SEX" />
          </div>

          <!-- Reporter Location -->
          <div class="flex flex-col">
            <TaxonomySelect v-model="filters.reporterLocation" label="Location" placeholder="Select location"
              root-key="LOCATION" />
          </div>

          <!-- Reporter Nationality -->
          <div class="flex flex-col">
            <TaxonomySelect v-model="filters.reporterNationality" label="Nationality" placeholder="Select nationality"
              root-key="NATIONALITY" />
          </div>

          <!-- Reporter Language -->
          <div class="flex flex-col">
            <TaxonomySelect v-model="filters.reporterLanguage" label="Language" placeholder="Select language"
              root-key="LANGUAGE" />
          </div>

          <!-- Reporter Tribe -->
          <div class="flex flex-col">
            <TaxonomySelect v-model="filters.reporterTribe" label="Tribe" placeholder="Select tribe"
              root-key="TRIBE" />
          </div>
        </div>
      </Transition>
    </div>

    <!-- Action Buttons -->
    <div class="flex gap-2 mt-4">
      <button @click="applyFilters"
        class="text-white px-6 py-2 rounded-lg transition-all duration-200 font-medium shadow-lg flex items-center gap-2 active:scale-95"
        :class="isDarkMode
          ? 'bg-amber-600 hover:bg-amber-700'
          : 'bg-amber-700 hover:bg-amber-800'">
        <i-mdi-filter class="w-4 h-4" />
        Apply Filters
      </button>

      <button @click="resetFilters"
        class="px-6 py-2 rounded-lg transition-all duration-200 font-medium border flex items-center gap-2" :class="isDarkMode
          ? 'bg-gray-700 text-gray-300 border-transparent hover:bg-gray-600'
          : 'bg-gray-100 text-gray-700 border-transparent hover:bg-gray-200'">
        <i-mdi-refresh class="w-4 h-4" />
        Reset
      </button>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref, inject } from 'vue'
import TaxonomySelect from '@/components/base/TaxonomySelect.vue'

  // Inject theme
  const isDarkMode = inject('isDarkMode')

  const emit = defineEmits(['update:filters'])

  // Collapsible section state
  const showCaseFilters = ref(false)
  const showReporterFilters = ref(false)

  const filters = reactive({
    dateFrom: '',
    dateTo: '',
    direction: '',
    phone: '',
    extension: '',
    hangupStatus: '',
    hangupBy: '',
    qaScore: '',
    // Case filters
    caseId: '',
    // Reporter filters
    reporterName: '',
    reporterPhone: '',
    reporterAge: '',
    reporterSex: '',
    reporterLocation: '',
    reporterNationality: '',
    reporterLanguage: '',
    reporterTribe: ''
  })

  // Helper to get unix timestamp from date string
  function getUnixTimestamp(dateString) {
    if (!dateString) return null
    const date = new Date(dateString)
    date.setHours(0, 0, 0, 0)
    return Math.floor(date.getTime() / 1000)
  }

  // Helper to get end of day timestamp
  function getEndOfDayTimestamp(dateString) {
    if (!dateString) return null
    const date = new Date(dateString)
    date.setHours(23, 59, 59, 999)
    return Math.floor(date.getTime() / 1000)
  }

  function applyFilters() {
    const params = {}

    // Date range - using chan_ts field
    if (filters.dateFrom || filters.dateTo) {
      const fromTs = filters.dateFrom ? getUnixTimestamp(filters.dateFrom) : 0
      const toTs = filters.dateTo ? getEndOfDayTimestamp(filters.dateTo) : Math.floor(Date.now() / 1000)
      params.chan_ts = `${fromTs};${toTs}`
    }

    // Direction - using vector field
    if (filters.direction) {
      params.vector = filters.direction
    }

    // Phone - using phone field
    if (filters.phone) {
      params.phone = filters.phone.trim()
    }

    // Extension - using usr field
    if (filters.extension) {
      params.usr = filters.extension.trim()
    }

    // Hangup Status - using hangup_status_txt field for text values
    if (filters.hangupStatus) {
      params.hangup_status_txt = filters.hangupStatus
    }

    // Hangup By - using hangup_reason_txt field if applicable, or hangup_reason
    // Backend usually expects 'hangup_reason_txt' if status is also text.
    // But let's check values: 'phone', 'usr'. These look like codes.
    // If user provided specific URL example for status, I'll stick to that fix primarily.
    if (filters.hangupBy) {
      params.hangup_reason = filters.hangupBy
    }

    // QA Score - using qa_score field (minimum score)
    if (filters.qaScore) {
      params.qa_score = filters.qaScore
    }

    // Case filters
    if (filters.caseId) {
      params.case_id = filters.caseId.trim()
    }

    // Reporter filters
    if (filters.reporterName) {
      params.reporter_name = filters.reporterName.trim()
    }
    if (filters.reporterPhone) {
      params.reporter_phone = filters.reporterPhone.trim()
    }
    if (filters.reporterAge) {
      params.reporter_age = filters.reporterAge
    }
    if (filters.reporterSex) {
      params.reporter_sex = filters.reporterSex
    }
    if (filters.reporterLocation) {
      params.reporter_location = filters.reporterLocation
    }
    if (filters.reporterNationality) {
      params.reporter_nationality = filters.reporterNationality
    }
    if (filters.reporterLanguage) {
      params.reporter_language = filters.reporterLanguage
    }
    if (filters.reporterTribe) {
      params.reporter_tribe = filters.reporterTribe
    }

    emit('update:filters', params)
  }

  function resetFilters() {
    Object.keys(filters).forEach(key => {
      filters[key] = ''
    })

    emit('update:filters', {})
  }
</script>

<style scoped>
  .fade-enter-active,
  .fade-leave-active {
    transition: all 0.3s ease;
  }

  .fade-enter-from,
  .fade-leave-to {
    opacity: 0;
    transform: translateY(-10px);
  }
</style>