<template>
  <div class="relative">
    <!-- Chart type selector toolbar -->
    <div class="flex items-center justify-between mb-4">
      <div class="flex gap-1">
        <button
          v-for="type in ['bar', 'line', 'pie', 'doughnut']"
          :key="type"
          @click="$emit('update:chartType', type)"
          class="px-3 py-1.5 text-xs font-medium rounded-lg transition-all"
          :class="
            chartType === type
              ? isDarkMode
                ? 'bg-amber-600 text-white'
                : 'bg-amber-700 text-white'
              : isDarkMode
              ? 'bg-gray-800 text-gray-400 hover:text-amber-400'
              : 'bg-gray-100 text-gray-600 hover:text-amber-700'
          "
        >
          {{ type.charAt(0).toUpperCase() + type.slice(1) }}
        </button>
      </div>

      <div class="flex items-center gap-3">
        <!-- Stacked toggle (only for bar/line) -->
        <label
          v-if="chartType === 'bar' || chartType === 'line'"
          class="flex items-center gap-2 text-xs cursor-pointer select-none"
          :class="isDarkMode ? 'text-gray-400' : 'text-gray-600'"
        >
          <input
            type="checkbox"
            :checked="stacked"
            @change="$emit('update:stacked', $event.target.checked)"
            class="rounded accent-amber-600"
          />
          Stacked
        </label>

        <!-- Download PNG -->
        <button
          @click="downloadPNG"
          class="px-3 py-1.5 rounded-lg text-xs font-medium border transition-all flex items-center gap-1.5"
          :class="
            isDarkMode
              ? 'bg-neutral-800 text-gray-300 border-neutral-700 hover:border-amber-500 hover:text-amber-400'
              : 'bg-gray-50 text-gray-600 border-gray-200 hover:border-amber-500 hover:text-amber-700'
          "
        >
          <i-mdi-image-outline class="w-4 h-4" />
          PNG
        </button>
      </div>
    </div>

    <!-- Chart canvas -->
    <div
      class="relative rounded-lg overflow-hidden border"
      :class="isDarkMode ? 'bg-black border-transparent' : 'bg-gray-50 border-transparent'"
      style="height: 400px"
    >
      <canvas ref="canvasRef"></canvas>

      <!-- No data overlay -->
      <div
        v-if="!chartData.length && !series.length"
        class="absolute inset-0 flex flex-col items-center justify-center"
      >
        <i-mdi-chart-bar
          class="w-16 h-16"
          :class="isDarkMode ? 'text-gray-700' : 'text-gray-300'"
        />
        <p
          class="mt-4 text-sm font-medium"
          :class="isDarkMode ? 'text-gray-500' : 'text-gray-400'"
        >
          Select time period and filters to view analytics
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted, onBeforeUnmount } from 'vue'
import { Chart, registerables } from 'chart.js'

Chart.register(...registerables)

// ---------------------------------------------------------------------------
// Props & Emits
// ---------------------------------------------------------------------------
const props = defineProps({
  /** Single-series data: Array of { label: string, value: number } */
  chartData: { type: Array, default: () => [] },
  /** 'bar' | 'line' | 'pie' | 'doughnut' */
  chartType: { type: String, default: 'bar' },
  /** Stack series on bar/line charts */
  stacked: { type: Boolean, default: false },
  /** Multi-series: Array of { label: string, data: number[], color?: string } */
  series: { type: Array, default: () => [] },
  /** X-axis labels shared across all series */
  seriesLabels: { type: Array, default: () => [] },
  /** Dark mode palette */
  isDarkMode: { type: Boolean, default: false }
})

const emit = defineEmits(['update:chartType', 'update:stacked', 'download'])

// ---------------------------------------------------------------------------
// Color palette
// ---------------------------------------------------------------------------
const CHART_COLORS = [
  '#f59e0b', '#10b981', '#3b82f6', '#ef4444', '#8b5cf6',
  '#ec4899', '#6366f1', '#14b8a6', '#f97316', '#84cc16',
  '#06b6d4', '#a855f7', '#e11d48', '#0ea5e9', '#d97706'
]

function generateColor(label) {
  let hash = 0
  for (let i = 0; i < label.length; i++) hash = label.charCodeAt(i) + ((hash << 5) - hash)
  return CHART_COLORS[Math.abs(hash) % CHART_COLORS.length]
}

// ---------------------------------------------------------------------------
// Chart instance
// ---------------------------------------------------------------------------
const canvasRef = ref(null)
let chartInstance = null

function buildConfig() {
  const isDark = props.isDarkMode
  const gridColor = isDark ? 'rgba(75,85,99,0.3)' : 'rgba(209,213,219,0.5)'
  const tickColor = isDark ? '#9ca3af' : '#6b7280'
  const isMultiSeries = props.series && props.series.length > 0

  let labels, datasets

  if (isMultiSeries) {
    labels = props.seriesLabels
    datasets = props.series.map(s => ({
      label: s.label,
      data: s.data,
      backgroundColor: s.color || generateColor(s.label),
      borderColor: s.color || generateColor(s.label),
      borderWidth: props.chartType === 'line' ? 2 : 0,
      fill: false,
      tension: 0.3,
      pointRadius: props.chartType === 'line' ? 3 : 0,
      pointHoverRadius: props.chartType === 'line' ? 5 : 0
    }))
  } else {
    labels = props.chartData.map(d => d.label)
    const values = props.chartData.map(d => d.value)
    const colors = props.chartData.map((_, i) => CHART_COLORS[i % CHART_COLORS.length])
    const isCategorical = props.chartType === 'pie' || props.chartType === 'doughnut'

    datasets = [{
      label: 'Count',
      data: values,
      backgroundColor: isCategorical ? colors : (isDark ? '#d97706' : '#b45309'),
      borderColor: isCategorical ? colors.map(() => 'transparent') : (isDark ? '#fbbf24' : '#f59e0b'),
      borderWidth: props.chartType === 'line' ? 2 : 0,
      fill: false,
      tension: 0.3,
      pointRadius: props.chartType === 'line' ? 3 : 0,
      pointHoverRadius: props.chartType === 'line' ? 5 : 0,
      hoverBackgroundColor: isCategorical ? colors.map(c => c + 'cc') : (isDark ? '#f59e0b' : '#d97706')
    }]
  }

  const type = props.chartType === 'pie' ? 'pie'
    : props.chartType === 'doughnut' ? 'doughnut'
    : props.chartType

  const config = {
    type,
    data: { labels, datasets },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      animation: { duration: 300 },
      plugins: {
        legend: {
          display: props.chartType === 'pie' || props.chartType === 'doughnut' || isMultiSeries,
          labels: { color: tickColor, padding: 16, usePointStyle: true, font: { size: 12 } }
        },
        tooltip: {
          mode: 'index',
          intersect: false,
          backgroundColor: isDark ? 'rgba(17,24,39,0.95)' : 'rgba(255,255,255,0.95)',
          titleColor: isDark ? '#f3f4f6' : '#111827',
          bodyColor: isDark ? '#d1d5db' : '#374151',
          borderColor: isDark ? '#374151' : '#e5e7eb',
          borderWidth: 1,
          padding: 10,
          cornerRadius: 8
        }
      }
    },
    plugins: [{
      id: 'customBackground',
      beforeDraw(chart) {
        const ctx = chart.canvas.getContext('2d')
        ctx.save()
        ctx.globalCompositeOperation = 'destination-over'
        ctx.fillStyle = isDark ? '#000000' : '#ffffff'
        ctx.fillRect(0, 0, chart.width, chart.height)
        ctx.restore()
      }
    }]
  }

  if (type === 'bar' || type === 'line') {
    config.options.scales = {
      x: {
        stacked: props.stacked,
        grid: { display: false },
        border: { display: false },
        ticks: { color: tickColor, maxRotation: 45, font: { size: 11 } }
      },
      y: {
        stacked: props.stacked,
        beginAtZero: true,
        grid: { color: gridColor },
        border: { display: false },
        ticks: { color: tickColor, font: { size: 11 } }
      }
    }
  }

  return config
}

function initChart() {
  if (!canvasRef.value) return
  if (chartInstance) { chartInstance.destroy(); chartInstance = null }
  if (!props.chartData.length && !props.series.length) return
  chartInstance = new Chart(canvasRef.value, buildConfig())
}

onMounted(() => initChart())
onBeforeUnmount(() => { if (chartInstance) { chartInstance.destroy(); chartInstance = null } })

watch(
  () => [props.chartData, props.chartType, props.stacked, props.series, props.seriesLabels, props.isDarkMode],
  () => initChart(),
  { deep: true }
)

// ---------------------------------------------------------------------------
// PNG download
// ---------------------------------------------------------------------------
function downloadPNG() {
  if (!canvasRef.value) return
  const url = canvasRef.value.toDataURL('image/png')
  const a = document.createElement('a')
  a.href = url
  a.download = `chart_${new Date().toISOString().slice(0, 10)}.png`
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  emit('download')
}
</script>
