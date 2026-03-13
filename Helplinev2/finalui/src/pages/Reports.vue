<template>
  <div class="space-y-6">
    <div class="max-w-7xl mx-auto">

      <!-- Tab Navigation -->
      <div class="flex border-b mb-6 dark:border-gray-800 overflow-x-auto">
        <button @click="activeTab = 'chi'"
          class="px-6 py-3 font-medium text-sm border-b-2 transition-colors flex items-center gap-2 whitespace-nowrap"
          :class="activeTab === 'chi'
            ? (isDarkMode ? 'border-amber-500 text-amber-500' : 'border-amber-600 text-amber-700')
            : 'border-transparent text-gray-500 hover:text-gray-700'">
          CHI Standard Reports
        </button>
        <button @click="activeTab = 'vua'"
          class="px-6 py-3 font-medium text-sm border-b-2 transition-colors flex items-center gap-2 whitespace-nowrap"
          :class="activeTab === 'vua'
            ? (isDarkMode ? 'border-amber-500 text-amber-500' : 'border-amber-600 text-amber-700')
            : 'border-transparent text-gray-500 hover:text-gray-700'">
          <i-mdi-file-document-outline class="w-4 h-4" />
          VUA Quarterly (OCSEA)
        </button>
        <button @click="activeTab = 'webstats'"
          class="px-6 py-3 font-medium text-sm border-b-2 transition-colors flex items-center gap-2 whitespace-nowrap"
          :class="activeTab === 'webstats'
            ? (isDarkMode ? 'border-amber-500 text-amber-500' : 'border-amber-600 text-amber-700')
            : 'border-transparent text-gray-500 hover:text-gray-700'">
          Website Statistics
        </button>
        <button @click="activeTab = 'custom'"
          class="px-6 py-3 font-medium text-sm border-b-2 transition-colors flex items-center gap-2 whitespace-nowrap"
          :class="activeTab === 'custom'
            ? (isDarkMode ? 'border-amber-500 text-amber-500' : 'border-amber-600 text-amber-700')
            : 'border-transparent text-gray-500 hover:text-gray-700'">
          Custom Explorer
        </button>
      </div>

      <div v-if="activeTab === 'chi'">
        <CHIReports />
      </div>

      <div v-if="activeTab === 'vua'">
        <VUAReports />
      </div>

      <div v-if="activeTab === 'webstats'">
        <WebsiteStats />
      </div>

      <div v-if="activeTab === 'custom'">
        <CustomExplorer />
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, inject } from 'vue'
import CHIReports from '@/components/reports/CHIReports.vue'
import VUAReports from '@/components/reports/VUAReports.vue'
import WebsiteStats from '@/components/reports/WebsiteStats.vue'
import CustomExplorer from '@/components/reports/CustomExplorer.vue'

const isDarkMode = inject('isDarkMode')
const activeTab = ref('chi')
</script>
