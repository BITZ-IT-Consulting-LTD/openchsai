<template>
  <div class="flex flex-col h-full bg-gray-50 dark:bg-black p-4 gap-4">
    <!-- Header -->
    <div class="flex flex-col md:flex-row gap-4 items-start md:items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold text-gray-900 dark:text-white mb-2">Extension History</h1>
        <p class="text-gray-500 text-sm">View detailed call history per extension.</p>
      </div>
    </div>

    <!-- Filters -->
    <ExtsFilter @filter="applyFilters" />

    <!-- Main Content -->
    <div class="flex-1 flex flex-col gap-4 min-h-0">
      <!-- View Toggle and Actions -->
      <div class="flex flex-wrap items-center justify-between gap-4">
        <div class="flex gap-3">
          <button @click="activeView = 'list'" :class="getViewButtonClass(activeView === 'list')">
            <i-mdi-table class="w-5 h-5" />
            List
          </button>

          <button @click="activeView = 'reports'" :class="getViewButtonClass(activeView === 'reports')">
            <i-mdi-chart-bar class="w-5 h-5" />
            Reports
          </button>

          <button
            @click="refreshData"
            :disabled="extsStore.loading"
            :class="[
              'px-5 py-2.5 rounded-xl font-medium transition-all duration-200 flex items-center gap-2 text-sm border disabled:opacity-50 disabled:cursor-not-allowed',
              isDarkMode
                ? 'bg-black text-gray-300 border-transparent hover:border-green-500 hover:text-green-400'
                : 'bg-white text-gray-700 border-transparent hover:border-green-600 hover:text-green-600'
            ]"
          >
            <i-mdi-refresh class="w-5 h-5" />
            Refresh
          </button>

          <button v-if="authStore.canExport" @click="handleDownload"
            :disabled="extsStore.loading || extsStore.exts.length === 0" :class="[
              'px-5 py-2.5 rounded-xl font-medium transition-all duration-200 flex items-center gap-2 text-sm border disabled:opacity-50 disabled:cursor-not-allowed',
              isDarkMode
                ? 'bg-black text-gray-300 border-transparent hover:border-amber-500 hover:text-amber-400'
                : 'bg-white text-gray-700 border-transparent hover:border-amber-600 hover:text-amber-700'
            ]">
            <i-mdi-file-excel-outline class="w-5 h-5 text-green-500" />
            Download
          </button>
        </div>
      </div>

      <!-- List View -->
      <div v-if="activeView === 'list'">
        <ExtsTable :exts="extsStore.exts" :exts-store="extsStore" />
      </div>

      <!-- Reports View -->
      <div v-if="activeView === 'reports'">
        <div class="rounded-xl shadow-xl p-6 border" :class="isDarkMode
          ? 'bg-black border-transparent'
          : 'bg-white border-transparent'">

          <!-- Loading state -->
          <div v-if="reportLoading" class="flex items-center justify-center py-12">
            <i-mdi-loading class="w-8 h-8 animate-spin" :class="isDarkMode ? 'text-amber-400' : 'text-amber-600'" />
            <span class="ml-3 text-sm" :class="isDarkMode ? 'text-gray-400' : 'text-gray-600'">Loading report...</span>
          </div>

          <!-- Report data -->
          <div v-else-if="reportData">
            <h3 class="text-lg font-semibold mb-4" :class="isDarkMode ? 'text-white' : 'text-gray-900'">
              Pivot Report
            </h3>
            <div class="overflow-auto">
              <table class="min-w-full text-sm text-left">
                <thead class="border-b" :class="isDarkMode ? 'bg-black/60 border-transparent' : 'bg-gray-50 border-transparent'">
                  <tr>
                    <th v-for="(header, hIdx) in reportHeaders" :key="hIdx"
                      class="px-4 py-3 text-xs font-semibold uppercase tracking-wider"
                      :class="isDarkMode ? 'text-gray-300' : 'text-gray-700'">
                      {{ header }}
                    </th>
                  </tr>
                </thead>
                <tbody class="divide-y" :class="isDarkMode ? 'divide-gray-700' : 'divide-gray-200'">
                  <tr v-for="(row, rIdx) in reportRows" :key="rIdx"
                    :class="isDarkMode ? 'hover:bg-gray-700/30' : 'hover:bg-gray-50'">
                    <td v-for="(cell, cIdx) in row" :key="cIdx" class="px-4 py-3"
                      :class="isDarkMode ? 'text-gray-300' : 'text-gray-700'">
                      {{ cell }}
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <!-- Empty state -->
          <div v-else class="text-center py-12">
            <i-mdi-chart-box-outline class="w-12 h-12 mx-auto mb-3" :class="isDarkMode ? 'text-gray-600' : 'text-gray-400'" />
            <p class="text-sm" :class="isDarkMode ? 'text-gray-500' : 'text-gray-500'">
              No report data available. Apply filters and click Refresh to generate a report.
            </p>
          </div>
        </div>
      </div>

      <!-- Pagination Controls -->
      <Pagination v-if="activeView === 'list'" :paginationInfo="extsStore.paginationInfo"
        :hasNextPage="extsStore.hasNextPage" :hasPrevPage="extsStore.hasPrevPage" :loading="extsStore.loading"
        :pageSize="selectedPageSize" @prev="goToPrevPage" @next="goToNextPage" @goToPage="goToPage"
        @changePageSize="changePageSize" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, inject } from "vue"
import { toast } from 'vue-sonner'
import ExtsTable from "@/components/exts/ExtsTable.vue"
import ExtsFilter from "@/components/exts/ExtsFilter.vue"
import Pagination from "@/components/base/Pagination.vue"
import { useExtsStore } from "@/stores/exts"
import { useAuthStore } from "@/stores/auth"

const isDarkMode = inject('isDarkMode')

const extsStore = useExtsStore()
const authStore = useAuthStore()
const activeView = ref("list")
const currentFilters = ref({})
const selectedPageSize = ref(20)
const reportLoading = ref(false)
const reportData = ref(null)
const reportHeaders = ref([])
const reportRows = ref([])

const getViewButtonClass = (isActive) => {
  const baseClasses = 'px-5 py-2.5 rounded-xl font-medium transition-all duration-200 flex items-center gap-2 text-sm'

  if (isActive) {
    return isDarkMode.value
      ? `${baseClasses} bg-amber-600 text-white shadow-lg shadow-blue-900/50`
      : `${baseClasses} bg-amber-700 text-white shadow-lg shadow-amber-900/30`
  } else {
    return isDarkMode.value
      ? `${baseClasses} bg-black text-gray-300 border border-transparent hover:border-amber-600 hover:text-amber-500`
      : `${baseClasses} bg-white text-gray-700 border border-transparent hover:border-amber-600 hover:text-amber-700`
  }
}

onMounted(async () => {
  try {
    await extsStore.listExts({ _o: 0, _c: selectedPageSize.value })
  } catch (err) {
    console.error("Error fetching extension history:", err)
    toast.error('Failed to load extension history data.')
  }
})

async function applyFilters(filters) {
  currentFilters.value = filters
  try {
    extsStore.resetPagination()
    await extsStore.listExts({ ...filters, _o: 0, _c: selectedPageSize.value })

    if (activeView.value === 'reports') {
      await loadReport()
    }
  } catch (err) {
    console.error("Error applying filters:", err)
    toast.error('Failed to apply filters.')
  }
}

async function refreshData() {
  try {
    if (activeView.value === 'reports') {
      await loadReport()
    } else {
      const params = {
        ...currentFilters.value,
        _o: extsStore.pagination.offset,
        _c: extsStore.pagination.limit
      }
      await extsStore.listExts(params)
    }
    toast.success('Data refreshed successfully!')
  } catch (err) {
    console.error("Error refreshing data:", err)
    toast.error('Failed to refresh data.')
  }
}

async function loadReport() {
  reportLoading.value = true
  try {
    const data = await extsStore.getPivotReport(currentFilters.value)
    reportData.value = data

    if (data && data.headers && data.rows) {
      reportHeaders.value = data.headers
      reportRows.value = data.rows
    } else if (data && Array.isArray(data) && data.length > 0) {
      reportHeaders.value = Object.keys(data[0])
      reportRows.value = data.map(item => Object.values(item))
    } else {
      reportHeaders.value = []
      reportRows.value = []
    }
  } catch (err) {
    console.error("Error loading report:", err)
    toast.error('Failed to load report.')
    reportData.value = null
  } finally {
    reportLoading.value = false
  }
}

async function handleDownload() {
  try {
    const blob = await extsStore.downloadCSV(currentFilters.value)
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'extension_history.csv'
    a.click()
    window.URL.revokeObjectURL(url)
    toast.success('Download started!')
  } catch (err) {
    console.error("Error downloading:", err)
    toast.error('Failed to download data.')
  }
}

async function goToNextPage() {
  try {
    await extsStore.nextPage(currentFilters.value)
  } catch (err) {
    toast.error('Failed to load next page.')
  }
}

async function goToPrevPage() {
  try {
    await extsStore.prevPage(currentFilters.value)
  } catch (err) {
    toast.error('Failed to load previous page.')
  }
}

async function goToPage(page) {
  if (page === '...') return
  try {
    await extsStore.goToPage(page, currentFilters.value)
  } catch (err) {
    toast.error('Failed to load page.')
  }
}

async function changePageSize(size) {
  selectedPageSize.value = size
  try {
    await extsStore.setPageSize(size, currentFilters.value)
  } catch (err) {
    toast.error('Failed to change page size.')
  }
}
</script>
