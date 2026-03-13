<template>
  <div class="divide-y" :class="isDarkMode ? 'divide-neutral-800' : 'divide-gray-100'">
    <div v-if="!categories || categories.length === 0" class="p-8 text-center text-sm"
      :class="isDarkMode ? 'text-gray-500' : 'text-gray-400'">
      No categories found
    </div>

    <div v-for="(cat, idx) in parsedCategories" :key="cat.id">
      <div class="flex items-center gap-3 px-4 py-3 cursor-pointer transition-colors hover:bg-gray-50 dark:hover:bg-neutral-800/50"
        :style="{ paddingLeft: `${(depth * 24) + 16}px` }">

        <button v-if="cat.hasChildren !== false" @click="toggleExpand(cat)"
          class="w-6 h-6 flex items-center justify-center rounded transition-colors"
          :class="isDarkMode ? 'hover:bg-neutral-700 text-gray-400' : 'hover:bg-gray-200 text-gray-500'">
          <svg class="w-4 h-4 transition-transform" :class="{ 'rotate-90': expandedIds.has(cat.id) }"
            xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
            <path d="M10 6L8.59 7.41 13.17 12l-4.58 4.59L10 18l6-6z"/>
          </svg>
        </button>
        <div v-else class="w-6"></div>

        <div class="flex-1 min-w-0">
          <span class="text-sm font-medium" :class="isDarkMode ? 'text-gray-200' : 'text-gray-900'">{{ cat.name }}</span>
          <span class="ml-2 text-xs" :class="isDarkMode ? 'text-gray-500' : 'text-gray-400'">#{{ cat.id }}</span>
        </div>

        <div class="flex items-center gap-2 shrink-0">
          <button @click.stop="$emit('add-child', cat)" class="px-2 py-1 text-xs rounded transition-colors"
            :class="isDarkMode ? 'text-amber-500 hover:bg-neutral-800' : 'text-amber-700 hover:bg-amber-50'">
            + Child
          </button>
          <button @click.stop="$emit('edit', cat)" class="px-2 py-1 text-xs rounded transition-colors"
            :class="isDarkMode ? 'text-blue-400 hover:bg-neutral-800' : 'text-blue-600 hover:bg-blue-50'">
            Edit
          </button>
          <button @click.stop="$emit('toggle-active', cat)" class="px-2 py-1 text-xs rounded transition-colors"
            :class="cat.is_active === '0'
              ? 'text-emerald-500 hover:bg-emerald-50 dark:hover:bg-neutral-800'
              : 'text-red-500 hover:bg-red-50 dark:hover:bg-neutral-800'">
            {{ cat.is_active === '0' ? 'Activate' : 'Deactivate' }}
          </button>
        </div>
      </div>

      <!-- Children (expanded) -->
      <div v-if="expandedIds.has(cat.id) && childrenMap[cat.id]">
        <CategoryTree :categories="childrenMap[cat.id].items" :keys="childrenMap[cat.id].keys" :depth="depth + 1"
          @edit="(c) => $emit('edit', c)" @add-child="(c) => $emit('add-child', c)"
          @toggle-active="(c) => $emit('toggle-active', c)" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, inject, reactive } from 'vue'
import { useTaxonomyStore } from '@/stores/taxonomy'

const props = defineProps({
  categories: { type: Array, default: () => [] },
  keys: { type: Object, default: () => ({}) },
  depth: { type: Number, default: 0 }
})

defineEmits(['edit', 'add-child', 'toggle-active'])

const isDarkMode = inject('isDarkMode')
const taxonomyStore = useTaxonomyStore()

const expandedIds = reactive(new Set())
const childrenMap = ref({})

const parsedCategories = computed(() => {
  if (!props.categories || !props.keys) return []
  const k = props.keys
  const idIdx = Number(k.id?.[0] ?? 0)
  const nameIdx = Number(k.name?.[0] ?? 5)
  const activeIdx = Number(k.is_active?.[0] ?? -1)

  return props.categories.map(row => ({
    id: String(row[idIdx]),
    name: row[nameIdx] || `Category ${row[idIdx]}`,
    is_active: activeIdx >= 0 ? String(row[activeIdx]) : '1',
    hasChildren: null,
    _raw: row
  }))
})

const toggleExpand = async (cat) => {
  if (expandedIds.has(cat.id)) {
    expandedIds.delete(cat.id)
    return
  }

  // Fetch children if not cached
  if (!childrenMap.value[cat.id]) {
    try {
      const data = await taxonomyStore.viewCategory(cat.id)
      if (data && data.items && data.items.length > 0) {
        childrenMap.value[cat.id] = {
          items: data.items,
          keys: data.keys
        }
      }
    } catch (e) {
      console.error('Failed to load children:', e)
    }
  }

  expandedIds.add(cat.id)
}
</script>
