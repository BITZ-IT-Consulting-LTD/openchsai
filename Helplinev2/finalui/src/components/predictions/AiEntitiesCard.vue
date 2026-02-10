<template>
    <div class="rounded-xl border p-5 shadow-sm transition-all hover:shadow-md"
        :class="isDarkMode ? 'bg-neutral-800/50 border-neutral-700' : 'bg-white border-gray-100'">

        <div class="flex items-center gap-2 mb-4">
            <span class="px-2.5 py-1 rounded-md text-[10px] font-bold uppercase tracking-widest border"
                :class="isDarkMode ? 'bg-teal-900/30 text-teal-300 border-teal-800' : 'bg-teal-50 text-teal-600 border-teal-100'">
                Named Entities
            </span>
            <span class="text-xs font-mono" :class="isDarkMode ? 'text-gray-500' : 'text-gray-400'">{{ formatTime(prediction.created_on) }}</span>
        </div>

        <!-- Grouped Entities -->
        <div v-if="hasEntities" class="space-y-4">
            <div v-for="(entities, type) in groupedEntities" :key="type" class="border-b last:border-0 pb-3 last:pb-0"
                :class="isDarkMode ? 'border-neutral-700' : 'border-gray-100'">
                <div class="text-xs font-bold uppercase tracking-wider mb-2"
                    :class="isDarkMode ? 'text-gray-400' : 'text-gray-500'">{{ type }}</div>
                <div class="flex flex-wrap gap-2">
                    <span v-for="(entity, idx) in entities" :key="idx"
                        class="px-2.5 py-1 rounded-md text-sm border font-medium"
                        :class="isDarkMode ? 'bg-neutral-900 border-neutral-700 text-gray-300' : 'bg-gray-50 border-gray-200 text-gray-700'">
                        {{ entity }}
                    </span>
                </div>
            </div>
        </div>
        <div v-else class="text-sm italic" :class="isDarkMode ? 'text-gray-500' : 'text-gray-400'">
            No specific entities detected.
        </div>

        <AiFeedbackWidget :call-id="prediction.src_callid" :task-type="prediction.notification_type" />
    </div>
</template>

<script setup>
    import { inject, computed } from 'vue'
    import AiFeedbackWidget from './AiFeedbackWidget.vue'

    const props = defineProps({
        prediction: Object,
        payload: Object
    })

    const isDarkMode = inject('isDarkMode')

    // Convert an entity value (string or object) to a display string
    const flattenEntity = (val) => {
        if (typeof val === 'string') return val
        if (typeof val === 'object' && val !== null) {
            if (val.name) {
                const parts = [val.name]
                if (val.district && val.district !== val.name) parts.push(val.district)
                if (val.region && val.region !== val.name && val.region !== val.district) parts.push(val.region)
                return parts.join(', ')
            }
            if (val.text) return val.text
            if (val.value) return val.value
            return Object.values(val).filter(v => typeof v === 'string').join(', ')
        }
        return String(val)
    }

    const groupedEntities = computed(() => {
        const raw = props.payload.entities || props.payload
        const groups = {}

        if (Array.isArray(raw)) {
            raw.forEach(e => {
                const label = e.label || e.type || 'Other'
                const text = e.text || e.value || e
                if (!groups[label]) groups[label] = []
                const display = typeof text === 'string' ? text : flattenEntity(text)
                if (display) groups[label].push(display)
            })
        } else if (typeof raw === 'object') {
            Object.keys(raw).forEach(key => {
                if (Array.isArray(raw[key])) {
                    groups[key] = raw[key].map(flattenEntity).filter(Boolean)
                }
            })
        }

        return groups
    })

    const hasEntities = computed(() => Object.keys(groupedEntities.value).length > 0)

    const formatTime = (ts) => {
        if (!ts) return ''
        return new Date(ts * 1000).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    }
</script>
