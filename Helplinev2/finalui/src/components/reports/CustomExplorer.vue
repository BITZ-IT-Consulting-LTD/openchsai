<template>
  <div class="space-y-6">
    <!-- Controls Section -->
    <div v-if="!isDashboardMode" class="rounded-lg shadow-xl p-6 border"
      :class="isDarkMode ? 'bg-black border-transparent' : 'bg-white border-transparent'">
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <!-- Endpoint Selection -->
        <div v-if="!lockedEndpoint">
          <label class="block text-sm font-semibold mb-3" :class="isDarkMode ? 'text-gray-300' : 'text-gray-700'">
            Data Source
          </label>
          <select v-model="selectedEndpoint"
            class="w-full px-4 py-3 rounded-lg text-sm font-medium cursor-pointer transition-all duration-300 focus:outline-none focus:ring-2 focus:border-transparent"
            :class="isDarkMode
              ? 'bg-gray-700 border border-transparent text-gray-100 hover:border-amber-600 focus:ring-amber-500'
              : 'bg-gray-50 border border-transparent text-gray-900 hover:border-amber-600 focus:ring-amber-600'">
            <option value="qa">QA Results</option>
            <option value="cases">Cases</option>
            <option value="calls">Call History</option>
            <option value="websiteStatistics">Website Statistics Dashboard</option>
          </select>
        </div>
        <div v-else class="flex items-center gap-2">
          <span class="text-sm font-semibold" :class="isDarkMode ? 'text-gray-300' : 'text-gray-700'">Data Source:</span>
          <span class="px-3 py-1 rounded-lg text-sm font-medium"
            :class="isDarkMode ? 'bg-amber-600/20 text-amber-400' : 'bg-amber-100 text-amber-700'">
            {{ formatFieldName(selectedEndpoint) }}
          </span>
        </div>

        <!-- Time Period -->
        <div>
          <label class="block text-sm font-semibold mb-3" :class="isDarkMode ? 'text-gray-300' : 'text-gray-700'">
            Time Period (X-Axis)
          </label>
          <div class="flex gap-2">
            <button v-for="period in timePeriods" :key="period.value" @click="selectTimePeriod(period.value)"
              :class="getTimePeriodButtonClass(xAxis === period.value)">
              {{ period.label }}
            </button>
          </div>
        </div>
      </div>

      <!-- Y-Axis Filter -->
      <div class="mt-6">
        <label class="block text-sm font-semibold mb-3" :class="isDarkMode ? 'text-gray-300' : 'text-gray-700'">
          Filter By (Y-Axis)
        </label>
        <div class="rounded-lg p-4 mb-4 border"
          :class="isDarkMode ? 'bg-black/60 border-transparent' : 'bg-gray-100 border-transparent'">
          <div class="flex flex-wrap gap-2">
            <button v-for="field in availableYAxisFields" :key="field" @click="toggleYAxis(field)"
              :disabled="selectedYAxis.includes(field)" :class="getYAxisButtonClass(selectedYAxis.includes(field))">
              {{ formatFieldName(field) }}
            </button>
          </div>
        </div>

        <div v-if="selectedYAxis.length > 0" class="rounded-lg p-4 border"
          :class="isDarkMode ? 'bg-amber-900/20 border-amber-600/30' : 'bg-amber-50 border-amber-300'">
          <div class="flex items-center justify-between mb-2">
            <span class="text-sm font-semibold" :class="isDarkMode ? 'text-amber-500' : 'text-amber-700'">
              Selected Filters
            </span>
            <button @click="clearAllFilters" class="text-xs font-medium flex items-center gap-1"
              :class="isDarkMode ? 'text-amber-500 hover:text-blue-300' : 'text-amber-700 hover:text-amber-600'">
              <i-mdi-close class="w-3 h-3" />
              Clear All
            </button>
          </div>
          <div class="flex flex-wrap gap-2">
            <div v-for="(field, index) in selectedYAxis" :key="field"
              class="flex items-center gap-2 px-3 py-2 text-white rounded-lg text-sm font-medium shadow-sm"
              :class="isDarkMode ? 'bg-amber-600' : 'bg-amber-700'">
              <span>{{ formatFieldName(field) }}</span>
              <button @click="removeYAxis(index)" class="rounded p-0.5 transition-colors"
                :class="isDarkMode ? 'hover:bg-amber-700' : 'hover:bg-amber-800'">
                <i-mdi-close class="w-4 h-4" />
              </button>
            </div>
          </div>
        </div>

        <p v-else class="text-sm italic" :class="isDarkMode ? 'text-gray-500' : 'text-gray-500'">
          No filters selected. Click on options above to add filters.
        </p>
      </div>
    </div>

    <!-- Dashboard Mode (Website Stats) -->
    <div v-if="isDashboardMode">
      <div class="rounded-lg shadow-xl p-6 mb-6 border"
        :class="isDarkMode ? 'bg-black border-transparent' : 'bg-white border-transparent'">
        <div class="mb-6">
          <label class="block text-sm font-semibold mb-3" :class="isDarkMode ? 'text-gray-300' : 'text-gray-700'">
            Data Source
          </label>
          <select v-model="selectedEndpoint"
            class="w-full md:w-1/3 px-4 py-3 rounded-lg text-sm font-medium cursor-pointer transition-all duration-300 focus:outline-none focus:ring-2 focus:border-transparent"
            :class="isDarkMode
              ? 'bg-gray-700 border border-transparent text-gray-100 hover:border-amber-600 focus:ring-amber-500'
              : 'bg-gray-50 border border-transparent text-gray-900 hover:border-amber-600 focus:ring-amber-600'">
            <option value="qa">QA Results</option>
            <option value="cases">Cases</option>
            <option value="calls">Call History</option>
            <option value="websiteStatistics">Website Statistics Dashboard</option>
          </select>
        </div>
        <WebsiteStats />
      </div>
    </div>

    <!-- Chart Section -->
    <div v-if="!isDashboardMode" class="rounded-lg shadow-xl p-6 mb-6 border"
      :class="isDarkMode ? 'bg-black border-transparent' : 'bg-white border-transparent'">
      <div class="flex items-center justify-between mb-6">
        <h2 class="text-2xl font-bold flex items-center gap-2"
          :class="isDarkMode ? 'text-gray-100' : 'text-gray-900'">
          <i-mdi-chart-line class="w-6 h-6" :class="isDarkMode ? 'text-amber-500' : 'text-amber-700'" />
          {{ formatFieldName(selectedEndpoint) }} Analytics
        </h2>
        <div class="px-4 py-2 rounded-lg text-sm font-medium border"
          :class="isDarkMode ? 'bg-amber-600/20 text-amber-500 border-amber-600/30' : 'bg-amber-100 text-amber-700 border-amber-300'">
          {{ formatFieldName(currentMetric) }}
        </div>
      </div>

      <div v-if="loading" class="flex items-center justify-center h-96">
        <div class="flex flex-col items-center gap-4">
          <div class="animate-spin rounded-full h-12 w-12 border-4"
            :class="isDarkMode ? 'border-amber-900/30 border-t-amber-500' : 'border-amber-900/30 border-t-amber-600'">
          </div>
          <div class="font-medium" :class="isDarkMode ? 'text-gray-400' : 'text-gray-600'">Loading data...</div>
        </div>
      </div>

      <CustomExplorerChart v-else
        v-model:chartType="chartType"
        v-model:stacked="isStacked"
        :chartData="chartData"
        :series="chartSeries"
        :seriesLabels="chartSeriesLabels"
        :isDarkMode="isDarkMode"
      />
    </div>

    <!-- Table Section -->
    <div v-if="!isDashboardMode" class="rounded-lg shadow-xl p-6 border"
      :class="isDarkMode ? 'bg-black border-transparent' : 'bg-white border-transparent'">
      <div class="flex flex-wrap items-center justify-between gap-3 mb-4">
        <h2 class="text-2xl font-bold flex items-center gap-2"
          :class="isDarkMode ? 'text-gray-100' : 'text-gray-900'">
          <i-mdi-table class="w-6 h-6" :class="isDarkMode ? 'text-amber-500' : 'text-amber-700'" />
          Data Table
        </h2>
        <div class="flex flex-wrap items-center gap-3">
          <!-- Sort control -->
          <div class="flex items-center gap-1 text-xs" :class="isDarkMode ? 'text-gray-400' : 'text-gray-600'">
            <span class="font-medium mr-1">Sort:</span>
            <button @click="sortBy = 'name'" class="px-2 py-1 rounded"
              :class="sortBy === 'name'
                ? (isDarkMode ? 'bg-amber-600 text-white' : 'bg-amber-700 text-white')
                : (isDarkMode ? 'bg-gray-700 text-gray-400' : 'bg-gray-100 text-gray-600')">
              Name
            </button>
            <button @click="sortBy = 'total'" class="px-2 py-1 rounded"
              :class="sortBy === 'total'
                ? (isDarkMode ? 'bg-amber-600 text-white' : 'bg-amber-700 text-white')
                : (isDarkMode ? 'bg-gray-700 text-gray-400' : 'bg-gray-100 text-gray-600')">
              Total
            </button>
          </div>

          <!-- Value function -->
          <div class="flex items-center gap-1 text-xs" :class="isDarkMode ? 'text-gray-400' : 'text-gray-600'">
            <span class="font-medium mr-1">Show:</span>
            <button v-for="vf in valueFnOptions" :key="vf.value" @click="valueFn = vf.value"
              class="px-2 py-1 rounded"
              :class="valueFn === vf.value
                ? (isDarkMode ? 'bg-amber-600 text-white' : 'bg-amber-700 text-white')
                : (isDarkMode ? 'bg-gray-700 text-gray-400' : 'bg-gray-100 text-gray-600')">
              {{ vf.label }}
            </button>
          </div>

          <!-- Export buttons -->
          <button v-if="tableData.length > 0" @click="exportCSV"
            class="px-3 py-2 rounded-lg text-xs font-medium transition-all duration-200 flex items-center gap-1.5 border"
            :class="isDarkMode
              ? 'bg-neutral-800 text-gray-300 border-neutral-700 hover:border-amber-500 hover:text-amber-400'
              : 'bg-gray-50 text-gray-600 border-gray-200 hover:border-amber-500 hover:text-amber-700'">
            <i-mdi-file-delimited-outline class="w-4 h-4" />
            CSV
          </button>
          <button v-if="tableData.length > 0" @click="exportXLSX"
            class="px-3 py-2 rounded-lg text-xs font-medium transition-all duration-200 flex items-center gap-1.5 border"
            :class="isDarkMode
              ? 'bg-neutral-800 text-gray-300 border-neutral-700 hover:border-green-500 hover:text-green-400'
              : 'bg-gray-50 text-gray-600 border-gray-200 hover:border-green-500 hover:text-green-700'">
            <i-mdi-microsoft-excel class="w-4 h-4" />
            XLSX
          </button>
        </div>
      </div>

      <div v-if="loading" class="flex items-center justify-center h-64">
        <div class="flex flex-col items-center gap-4">
          <div class="animate-spin rounded-full h-12 w-12 border-4"
            :class="isDarkMode ? 'border-amber-900/30 border-t-amber-500' : 'border-amber-900/30 border-t-amber-600'">
          </div>
          <div class="font-medium" :class="isDarkMode ? 'text-gray-400' : 'text-gray-600'">Loading data...</div>
        </div>
      </div>

      <div v-else-if="tableData.length === 0" class="flex items-center justify-center h-64">
        <div class="text-center">
          <i-mdi-table class="mx-auto h-16 w-16" :class="isDarkMode ? 'text-gray-600' : 'text-gray-400'" />
          <p class="mt-4 font-medium" :class="isDarkMode ? 'text-gray-400' : 'text-gray-600'">No data available</p>
          <p class="mt-2 text-sm" :class="isDarkMode ? 'text-gray-500' : 'text-gray-500'">
            Select time period and filters to view data
          </p>
        </div>
      </div>

      <div v-else class="overflow-x-auto rounded-lg">
        <table class="min-w-full divide-y" :class="isDarkMode ? 'divide-gray-700' : 'divide-gray-200'">
          <thead :class="isDarkMode ? 'bg-black/60' : 'bg-gray-50'">
            <tr>
              <th v-for="(filter, idx) in selectedYAxis" :key="'filter-' + idx"
                class="px-6 py-4 text-left text-xs font-bold uppercase tracking-wider"
                :class="isDarkMode ? 'text-gray-300' : 'text-gray-700'">
                {{ formatFieldName(filter) }}
              </th>
              <th v-for="period in tableTimePeriods" :key="'period-' + period"
                class="px-6 py-4 text-center text-xs font-bold uppercase tracking-wider"
                :class="isDarkMode ? 'text-gray-300 bg-amber-900/20' : 'text-gray-700 bg-amber-50'">
                {{ period }}
              </th>
              <th class="px-6 py-4 text-center text-xs font-bold uppercase tracking-wider"
                :class="isDarkMode ? 'text-amber-500 bg-amber-900/30' : 'text-amber-700 bg-amber-100'">
                Total
              </th>
            </tr>
          </thead>
          <tbody class="divide-y" :class="isDarkMode ? 'bg-black divide-gray-700' : 'bg-white divide-gray-200'">
            <tr v-for="(row, rowIdx) in tableData" :key="'row-' + rowIdx" class="transition-colors"
              :class="isDarkMode ? 'hover:bg-gray-700/30' : 'hover:bg-gray-50'">
              <td v-for="(filter, filterIdx) in selectedYAxis" :key="'cell-filter-' + filterIdx"
                class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                <span class="inline-flex items-center px-3 py-1 rounded-lg"
                  :class="isDarkMode ? 'bg-gray-700 text-gray-300' : 'bg-gray-100 text-gray-700'">
                  {{ row.filters[filterIdx] || '-' }}
                </span>
              </td>
              <td v-for="(count, periodIdx) in row.displayCounts" :key="'cell-count-' + periodIdx"
                class="px-6 py-4 whitespace-nowrap text-sm text-center font-medium"
                :class="isDarkMode ? 'text-gray-300' : 'text-gray-700'">
                {{ count }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-center font-bold"
                :class="isDarkMode ? 'text-amber-500 bg-amber-900/20' : 'text-amber-700 bg-amber-50'">
                {{ row.displayTotal }}
              </td>
            </tr>
            <tr class="font-bold" :class="isDarkMode ? 'bg-black/60' : 'bg-gray-100'">
              <td :colspan="selectedYAxis.length" class="px-6 py-4 whitespace-nowrap text-sm uppercase"
                :class="isDarkMode ? 'text-gray-100' : 'text-gray-900'">Total</td>
              <td v-for="(total, idx) in displayColumnTotals" :key="'total-' + idx"
                class="px-6 py-4 whitespace-nowrap text-sm text-center"
                :class="isDarkMode ? 'text-gray-100' : 'text-gray-900'">
                {{ total }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-center"
                :class="isDarkMode ? 'text-amber-500 bg-amber-900/30' : 'text-amber-700 bg-amber-100'">
                {{ displayGrandTotal }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, inject } from 'vue'
import { useCaseStore } from '@/stores/cases'
import { useCallStore } from '@/stores/calls'
import { useQAStore } from '@/stores/qas'
import CustomExplorerChart from './CustomExplorerChart.vue'
import WebsiteStats from './WebsiteStats.vue'

const props = defineProps({
  /** If set, locks the data source to this endpoint ('calls', 'cases', 'qa') */
  endpoint: { type: String, default: null }
})

const isDarkMode = inject('isDarkMode')

const caseStore = useCaseStore()
const callStore = useCallStore()
const qaStore = useQAStore()

const lockedEndpoint = computed(() => !!props.endpoint)
const selectedEndpoint = ref(props.endpoint || 'qa')
watch(() => props.endpoint, (val) => { if (val) selectedEndpoint.value = val })

const xAxis = ref('')
const selectedYAxis = ref([])
const loading = ref(false)
const rawData = ref([])
const chartType = ref('bar')
const isStacked = ref(false)
const sortBy = ref('total')    // 'name' | 'total'
const valueFn = ref('count')   // 'count' | 'pct' | 'cumul' | 'cumulpct'

const valueFnOptions = [
  { label: 'Count',  value: 'count'    },
  { label: '%',      value: 'pct'      },
  { label: 'Cumul',  value: 'cumul'    },
  { label: 'Cumul%', value: 'cumulpct' }
]

const timePeriods = [
  { label: 'Hour',  value: 'h'  },
  { label: 'Day',   value: 'dt' },
  { label: 'Week',  value: 'wk' },
  { label: 'Month', value: 'mn' },
  { label: 'Year',  value: 'yr' }
]

const endpointConfig = {
  qa: {
    store: qaStore,
    dataKey: 'qas',
    yAxisFields: ['Extension'],
    metric: 'qa_count'
  },
  cases: {
    store: caseStore,
    dataKey: 'cases',
    yAxisFields: [
      'Case', 'Reporter', 'Client', 'Perpetrator', 'Services', 'Referrals',
      'Main Category', 'SubCategory 1', 'SubCategory 2', 'SubCategory 3',
      'GBV Related', 'Case Source', 'Priority', 'Status', 'Created By',
      'Escalated To', 'Escalated By', 'Case Assessment', 'Status in the Justice System'
    ],
    metric: 'case_count'
  },
  calls: {
    store: callStore,
    dataKey: 'calls',
    yAxisFields: ['Direction', 'Extension', 'Hangup Status', 'SLA Band', 'Disposition'],
    metric: 'call_count'
  },
  websiteStatistics: {
    mode: 'dashboard',
    metric: 'dashboard'
  }
}

const isDashboardMode = computed(() => endpointConfig[selectedEndpoint.value]?.mode === 'dashboard')
const availableYAxisFields = computed(() => endpointConfig[selectedEndpoint.value]?.yAxisFields || [])
const currentMetric = computed(() => endpointConfig[selectedEndpoint.value]?.metric || '')

watch(selectedEndpoint, () => {
  selectedYAxis.value = []
  xAxis.value = ''
  rawData.value = []
})

function selectTimePeriod(period) {
  xAxis.value = period
  if (selectedYAxis.value.length > 0) fetchData()
}

function toggleYAxis(field) {
  if (!selectedYAxis.value.includes(field)) {
    selectedYAxis.value.push(field)
    if (xAxis.value) fetchData()
  }
}

function removeYAxis(index) {
  selectedYAxis.value.splice(index, 1)
  if (selectedYAxis.value.length > 0 && xAxis.value) {
    fetchData()
  } else {
    rawData.value = []
  }
}

function clearAllFilters() {
  selectedYAxis.value = []
  rawData.value = []
}

async function fetchData() {
  if (!selectedYAxis.value.length || !xAxis.value) return
  loading.value = true
  try {
    const config = endpointConfig[selectedEndpoint.value]
    const params = {
      xaxis: xAxis.value,
      yaxis: selectedYAxis.value.join(','),
      metrics: config.metric
    }
    const data = await config.store.getAnalytics(params)
    rawData.value = data[config.dataKey] || []
  } catch (err) {
    console.error('[CustomExplorer] fetchData error', err)
    rawData.value = []
  } finally {
    loading.value = false
  }
}

// ---------------------------------------------------------------------------
// Data Processing
// ---------------------------------------------------------------------------

const baseTableRows = computed(() => {
  if (!rawData.value?.length) return { rows: [], periods: [] }

  const groups = {}
  const periods = new Set()

  rawData.value.forEach(row => {
    if (!Array.isArray(row) || !row.length) return
    const timePeriod = String(row[0])
    const count = Number(row[row.length - 1]) || 0
    const filterValues = []
    for (let i = 1; i < row.length - 1; i++) filterValues.push(String(row[i] || ''))
    const filterKey = filterValues.join('|')
    periods.add(timePeriod)
    if (!groups[filterKey]) groups[filterKey] = { filters: filterValues, periodCounts: {} }
    groups[filterKey].periodCounts[timePeriod] = (groups[filterKey].periodCounts[timePeriod] || 0) + count
  })

  const sortedPeriods = Array.from(periods).sort((a, b) => {
    const na = Number(a), nb = Number(b)
    return (!isNaN(na) && !isNaN(nb)) ? na - nb : a.localeCompare(b)
  })

  const rows = Object.values(groups).map(group => {
    const counts = sortedPeriods.map(p => group.periodCounts[p] || 0)
    const total = counts.reduce((s, v) => s + v, 0)
    return { filters: group.filters, counts, total }
  })

  return { rows, periods: sortedPeriods }
})

const tableTimePeriods = computed(() => baseTableRows.value.periods.map(p => formatLabel(p)))

const columnTotals = computed(() => {
  const { rows } = baseTableRows.value
  if (!rows.length) return []
  const numCols = rows[0].counts.length
  const totals = new Array(numCols).fill(0)
  rows.forEach(r => r.counts.forEach((c, i) => { totals[i] += c }))
  return totals
})

const grandTotal = computed(() => columnTotals.value.reduce((s, v) => s + v, 0))

const tableData = computed(() => {
  const { rows } = baseTableRows.value
  if (!rows.length) return []

  const sorted = [...rows].sort((a, b) => {
    if (sortBy.value === 'name') return String(a.filters[0] || '').localeCompare(String(b.filters[0] || ''))
    return b.total - a.total
  })

  const gt = grandTotal.value || 1
  const colTotals = columnTotals.value.map(t => t || 1)
  const runningCount = sorted.length ? new Array(sorted[0].counts.length).fill(0) : []
  let runningTotal = 0

  return sorted.map(row => {
    let displayCounts, displayTotal

    if (valueFn.value === 'count') {
      displayCounts = row.counts
      displayTotal = row.total
    } else if (valueFn.value === 'pct') {
      displayCounts = row.counts.map((c, i) => `${((c / colTotals[i]) * 100).toFixed(1)}%`)
      displayTotal = `${((row.total / gt) * 100).toFixed(1)}%`
    } else if (valueFn.value === 'cumul') {
      row.counts.forEach((c, i) => { runningCount[i] += c })
      runningTotal += row.total
      displayCounts = [...runningCount]
      displayTotal = runningTotal
    } else {
      // cumulpct
      row.counts.forEach((c, i) => { runningCount[i] += c })
      runningTotal += row.total
      displayCounts = runningCount.map((c, i) => `${((c / colTotals[i]) * 100).toFixed(1)}%`)
      displayTotal = `${((runningTotal / gt) * 100).toFixed(1)}%`
    }

    return { ...row, displayCounts, displayTotal }
  })
})

const displayColumnTotals = computed(() => {
  if (valueFn.value === 'count' || valueFn.value === 'cumul') return columnTotals.value
  return columnTotals.value.map(() => '100%')
})

const displayGrandTotal = computed(() => {
  if (valueFn.value === 'count' || valueFn.value === 'cumul') return grandTotal.value
  return '100%'
})

// ---------------------------------------------------------------------------
// Chart Data
// ---------------------------------------------------------------------------

const chartData = computed(() => {
  if (selectedYAxis.value.length !== 1 || !rawData.value?.length) return []
  const groups = {}
  rawData.value.forEach(row => {
    if (!Array.isArray(row) || !row.length) return
    const tp = String(row[0])
    const value = Number(row[row.length - 1]) || 0
    groups[tp] = (groups[tp] || 0) + value
  })
  return Object.entries(groups)
    .sort((a, b) => {
      const na = Number(a[0]), nb = Number(b[0])
      return (!isNaN(na) && !isNaN(nb)) ? na - nb : a[0].localeCompare(b[0])
    })
    .map(([label, value]) => ({ label: formatLabel(label), value }))
})

const chartSeries = computed(() => {
  if (selectedYAxis.value.length <= 1) return []
  const { rows } = baseTableRows.value
  return rows.map(row => ({
    label: row.filters.join(' / ') || 'Unknown',
    data: row.counts
  }))
})

const chartSeriesLabels = computed(() => {
  if (selectedYAxis.value.length <= 1) return []
  return baseTableRows.value.periods.map(p => formatLabel(p))
})

// ---------------------------------------------------------------------------
// Formatting helpers
// ---------------------------------------------------------------------------

function formatLabel(label) {
  if (xAxis.value === 'h') return label
  const d = new Date(Number(label) * 1000)
  switch (xAxis.value) {
    case 'dt': return d.toLocaleDateString('en-US', { day: '2-digit', month: 'short', year: 'numeric' })
    case 'wk': {
      const ws = new Date(d)
      ws.setDate(d.getDate() - d.getDay())
      return `W${getWeekNumber(d)} (${ws.toLocaleDateString('en-US', { month: 'short', day: '2-digit' })})`
    }
    case 'mn': return d.toLocaleDateString('en-US', { month: 'short', year: 'numeric' })
    case 'yr': return String(d.getFullYear())
    default: return label
  }
}

function getWeekNumber(d) {
  const date = new Date(Date.UTC(d.getFullYear(), d.getMonth(), d.getDate()))
  const dayNum = date.getUTCDay() || 7
  date.setUTCDate(date.getUTCDate() + 4 - dayNum)
  const yearStart = new Date(Date.UTC(date.getUTCFullYear(), 0, 1))
  return Math.ceil((((date - yearStart) / 86400000) + 1) / 7)
}

function formatFieldName(field) {
  if (!field) return ''
  return field.split('_').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ')
}

// ---------------------------------------------------------------------------
// Styling
// ---------------------------------------------------------------------------

function getTimePeriodButtonClass(isActive) {
  const base = 'flex-1 px-4 py-3 rounded-lg text-sm font-medium transition-all duration-200'
  if (isActive) {
    return `${base} ${isDarkMode.value
      ? 'bg-amber-600 text-white shadow-lg shadow-amber-900/50'
      : 'bg-amber-700 text-white shadow-lg shadow-amber-900/30'}`
  }
  return `${base} ${isDarkMode.value
    ? 'bg-gray-700 text-gray-300 border border-transparent hover:border-amber-600 hover:text-amber-500'
    : 'bg-gray-100 text-gray-700 border border-transparent hover:border-amber-600 hover:text-amber-700'}`
}

function getYAxisButtonClass(isDisabled) {
  const base = 'px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200'
  if (isDisabled) {
    return `${base} ${isDarkMode.value
      ? 'bg-gray-700 text-gray-500 cursor-not-allowed'
      : 'bg-gray-200 text-gray-400 cursor-not-allowed'}`
  }
  return `${base} ${isDarkMode.value
    ? 'bg-black text-gray-300 border border-transparent hover:border-amber-600 hover:bg-amber-900/20 cursor-pointer'
    : 'bg-white text-gray-700 border border-transparent hover:border-amber-600 hover:bg-amber-50 cursor-pointer'}`
}

// ---------------------------------------------------------------------------
// Export
// ---------------------------------------------------------------------------

function exportCSV() {
  if (!tableData.value.length) return
  const filterHeaders = selectedYAxis.value.map(f => formatFieldName(f))
  const headers = [...filterHeaders, ...tableTimePeriods.value, 'Total']
  const rows = tableData.value.map(row => {
    const filterCells = row.filters.map(f => `"${f || ''}"`)
    return [...filterCells, ...row.displayCounts, row.displayTotal].join(',')
  })
  const totalRow = [
    ...selectedYAxis.value.map((_, i) => i === 0 ? '"Total"' : '""'),
    ...displayColumnTotals.value,
    displayGrandTotal.value
  ].join(',')
  const csv = [headers.join(','), ...rows, totalRow].join('\n')
  const blob = new Blob([csv], { type: 'text/csv' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `${formatFieldName(selectedEndpoint.value)}_report_${new Date().toISOString().slice(0, 10)}.csv`
  a.click()
  URL.revokeObjectURL(url)
}

async function exportXLSX() {
  try {
    const XLSX = await import('xlsx')
    const filterHeaders = selectedYAxis.value.map(f => formatFieldName(f))
    const headers = [...filterHeaders, ...tableTimePeriods.value, 'Total']
    const rows = tableData.value.map(row => [...row.filters, ...row.displayCounts, row.displayTotal])
    const totalRow = [
      ...selectedYAxis.value.map((_, i) => i === 0 ? 'Total' : ''),
      ...displayColumnTotals.value,
      displayGrandTotal.value
    ]
    const ws = XLSX.utils.aoa_to_sheet([headers, ...rows, totalRow])
    const wb = XLSX.utils.book_new()
    XLSX.utils.book_append_sheet(wb, ws, formatFieldName(selectedEndpoint.value))
    XLSX.writeFile(wb, `${formatFieldName(selectedEndpoint.value)}_report_${new Date().toISOString().slice(0, 10)}.xlsx`)
  } catch {
    exportCSV()
  }
}
</script>
