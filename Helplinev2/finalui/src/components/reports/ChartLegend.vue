<template>
  <div v-if="series.length > 0" class="flex flex-wrap gap-3 mt-4 pt-4 border-t"
    :class="isDarkMode ? 'border-gray-800' : 'border-gray-200'">
    <div v-for="(s, i) in series" :key="s.key ?? i"
      class="flex items-center gap-2 px-3 py-2 rounded-lg border text-xs font-medium transition-all"
      :class="s.visible
        ? (isDarkMode ? 'border-gray-700 bg-gray-900' : 'border-gray-200 bg-white')
        : (isDarkMode ? 'border-gray-800 bg-black opacity-50' : 'border-gray-100 bg-gray-50 opacity-50')">
      <!-- Color swatch -->
      <div class="w-3 h-3 rounded-full flex-shrink-0" :style="{ backgroundColor: s.color }"></div>

      <!-- Label -->
      <span :class="isDarkMode ? 'text-gray-300' : 'text-gray-700'">{{ s.label }}</span>

      <!-- Hide/Show toggle -->
      <button @click="toggleVisible(i)" class="px-2 py-0.5 rounded text-xs transition-colors"
        :class="s.visible
          ? (isDarkMode ? 'text-gray-500 hover:text-red-400' : 'text-gray-400 hover:text-red-600')
          : (isDarkMode ? 'text-green-400' : 'text-green-600')">
        {{ s.visible ? 'Hide' : 'Show' }}
      </button>

      <!-- Line/Bar toggle (only meaningful when visible) -->
      <button v-if="s.visible" @click="toggleLine(i)" class="px-2 py-0.5 rounded text-xs transition-colors"
        :class="s.asLine
          ? (isDarkMode ? 'text-amber-400 bg-amber-900/30' : 'text-amber-600 bg-amber-50')
          : (isDarkMode ? 'text-gray-500 hover:text-amber-400' : 'text-gray-400 hover:text-amber-600')">
        {{ s.asLine ? 'Line ✓' : 'Line' }}
      </button>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  series: { type: Array, default: () => [] },
  isDarkMode: { type: Boolean, default: false }
})

const emit = defineEmits(['update:series'])

function toggleVisible(i) {
  emit('update:series', props.series.map((s, idx) => idx === i ? { ...s, visible: !s.visible } : s))
}

function toggleLine(i) {
  emit('update:series', props.series.map((s, idx) => idx === i ? { ...s, asLine: !s.asLine } : s))
}
</script>
