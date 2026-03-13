<template>
    <Transition enter-active-class="transform transition ease-in-out duration-300" enter-from-class="translate-x-full"
        enter-to-class="translate-x-0" leave-active-class="transform transition ease-in-out duration-300"
        leave-from-class="translate-x-0" leave-to-class="translate-x-full">
        <div v-if="isOpen"
            class="fixed inset-y-0 right-0 w-[500px] z-[110] flex shadow-2xl border-l overflow-y-auto"
            :class="isDarkMode ? 'bg-neutral-900 border-neutral-800' : 'bg-white border-gray-200'">
            <div class="flex flex-col w-full h-full">
                <!-- Header -->
                <div class="p-6 border-b flex justify-between items-center sticky top-0 z-10"
                    :class="isDarkMode ? 'bg-neutral-900 border-neutral-800' : 'bg-white border-gray-200'">
                    <div>
                        <h2 class="text-lg font-black" :class="isDarkMode ? 'text-white' : 'text-gray-900'">QA Review</h2>
                        <p class="text-xs mt-0.5" :class="isDarkMode ? 'text-gray-400' : 'text-gray-500'">Read-only view</p>
                    </div>
                    <button @click="$emit('close')"
                        class="p-2 rounded-full transition-colors"
                        :class="isDarkMode ? 'hover:bg-neutral-800' : 'hover:bg-gray-100'">
                        <i-mdi-close class="w-5 h-5" :class="isDarkMode ? 'text-gray-400' : 'text-gray-600'" />
                    </button>
                </div>

                <!-- Content -->
                <div class="p-6 flex-1 overflow-y-auto space-y-6">
                    <!-- Loading -->
                    <div v-if="loading" class="flex justify-center py-12">
                        <div class="w-8 h-8 border-3 border-amber-500 border-t-transparent rounded-full animate-spin"></div>
                    </div>

                    <template v-else-if="qaData">
                        <!-- Score Summary -->
                        <div class="p-4 rounded-xl border text-center"
                            :class="isDarkMode ? 'bg-neutral-800 border-neutral-700' : 'bg-amber-50 border-amber-200'">
                            <div class="text-3xl font-black" :class="isDarkMode ? 'text-amber-500' : 'text-amber-700'">
                                {{ qaData.totalScore }}%
                            </div>
                            <div class="text-xs font-semibold uppercase tracking-wider mt-1"
                                :class="isDarkMode ? 'text-gray-400' : 'text-gray-600'">
                                Total Score
                            </div>
                        </div>

                        <!-- Meta Info -->
                        <div class="grid grid-cols-2 gap-4">
                            <div v-for="field in metaFields" :key="field.label">
                                <label class="block text-[10px] font-bold uppercase tracking-wider mb-1"
                                    :class="isDarkMode ? 'text-gray-500' : 'text-gray-400'">{{ field.label }}</label>
                                <div class="text-sm font-medium" :class="isDarkMode ? 'text-gray-200' : 'text-gray-800'">
                                    {{ field.value || '-' }}
                                </div>
                            </div>
                        </div>

                        <!-- QA Section Scores -->
                        <div v-for="section in qaData.sections" :key="section.title">
                            <h3 class="text-sm font-bold uppercase tracking-wider mb-3"
                                :class="isDarkMode ? 'text-gray-400' : 'text-gray-600'">{{ section.title }}
                                <span class="ml-2 text-xs font-semibold px-2 py-0.5 rounded-full"
                                    :class="section.scorePercent >= 75
                                        ? 'bg-emerald-100 text-emerald-700 dark:bg-emerald-900/30 dark:text-emerald-400'
                                        : section.scorePercent >= 50
                                            ? 'bg-amber-100 text-amber-700 dark:bg-amber-900/30 dark:text-amber-400'
                                            : 'bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400'">
                                    {{ section.scorePercent }}%
                                </span>
                            </h3>
                            <div class="space-y-2">
                                <div v-for="field in section.fields" :key="field.label"
                                    class="flex justify-between items-center p-3 rounded-lg"
                                    :class="isDarkMode ? 'bg-neutral-800' : 'bg-gray-50'">
                                    <span class="text-sm" :class="isDarkMode ? 'text-gray-300' : 'text-gray-700'">
                                        {{ field.label }}
                                    </span>
                                    <span class="text-sm font-bold"
                                        :class="field.value === '2'
                                            ? 'text-emerald-500'
                                            : field.value === '1'
                                                ? 'text-amber-500'
                                                : 'text-red-500'">
                                        {{ getRatingLabel(field.value) }}
                                    </span>
                                </div>
                            </div>
                            <!-- Section comment -->
                            <div v-if="section.comment" class="mt-2 p-3 rounded-lg text-sm whitespace-pre-wrap"
                                :class="isDarkMode ? 'bg-neutral-800/60 text-gray-400' : 'bg-gray-50/80 text-gray-500'">
                                <span class="text-[10px] font-bold uppercase tracking-wider block mb-1"
                                    :class="isDarkMode ? 'text-gray-500' : 'text-gray-400'">Comment</span>
                                {{ section.comment }}
                            </div>
                        </div>

                        <!-- Overall Feedback -->
                        <div v-if="qaData.feedback">
                            <h3 class="text-sm font-bold uppercase tracking-wider mb-2"
                                :class="isDarkMode ? 'text-gray-400' : 'text-gray-600'">Overall Feedback</h3>
                            <div class="p-3 rounded-lg text-sm whitespace-pre-wrap"
                                :class="isDarkMode ? 'bg-neutral-800 text-gray-300' : 'bg-gray-50 text-gray-700'">
                                {{ qaData.feedback }}
                            </div>
                        </div>
                    </template>

                    <div v-else class="text-center py-12 text-sm"
                        :class="isDarkMode ? 'text-gray-500' : 'text-gray-400'">
                        No QA data available
                    </div>
                </div>
            </div>
        </div>
    </Transition>

    <div v-if="isOpen" @click="$emit('close')" class="fixed inset-0 bg-black/20 z-[105] backdrop-blur-sm"></div>
</template>

<script setup>
import { ref, computed, inject, watch } from 'vue'

const props = defineProps({
    isOpen: Boolean,
    qaRecord: {
        type: Array,
        default: null
    },
    qas_k: {
        type: Object,
        default: () => ({})
    }
})

const emit = defineEmits(['close'])
const isDarkMode = inject('isDarkMode')

const loading = ref(false)

// Helper to get field value from array using key mapping
const getFieldValue = (fieldName) => {
    if (!props.qaRecord || !props.qas_k[fieldName]) return ''
    const index = props.qas_k[fieldName][0]
    return index !== undefined ? props.qaRecord[index] : ''
}

// Rating label
const getRatingLabel = (value) => {
    if (value === '2') return 'Yes (1)'
    if (value === '1') return 'Partial (0.5)'
    if (value === '0') return 'No (0)'
    return 'N/A'
}

// Format timestamp
const formatTimestamp = (timestamp) => {
    if (!timestamp || timestamp === '0') return '-'
    let ts = Number(timestamp)
    if (ts < 10000000000) ts *= 1000
    const date = new Date(ts)
    return date.toLocaleString('en-GB', {
        day: '2-digit',
        month: 'short',
        year: 'numeric',
        hour: 'numeric',
        minute: '2-digit',
    })
}

// Section definitions (mirroring CreateQA structure)
const sectionDefs = [
    {
        title: 'Opening Phrase',
        fields: [{ key: 'opening_phrase', label: 'Opening Phrase Rating' }],
        commentKey: 'opening_phrase_comments'
    },
    {
        title: 'Listening Skills',
        fields: [
            { key: 'non_interrupting', label: 'Non Interrupting' },
            { key: 'empathy', label: 'Empathy' },
            { key: 'paraphrasing', label: 'Paraphrasing' }
        ],
        commentKey: 'listening_comments'
    },
    {
        title: 'Communication Skills',
        fields: [
            { key: 'courteous', label: 'Courteous' },
            { key: 'grammar', label: 'Grammar' },
            { key: 'nonhesitant', label: 'Non Hesitant' },
            { key: 'educative', label: 'Educative' }
        ],
        commentKey: null
    },
    {
        title: 'Proactive Approach',
        fields: [
            { key: 'procedure_adherance', label: 'Procedure Adherence' },
            { key: 'extra_mile_willingness', label: 'Extra Mile Willingness' },
            { key: 'consults', label: 'Consults' },
            { key: 'follows_up_on_case_updates', label: 'Follows Up On Case Updates' }
        ],
        commentKey: 'pro_active_comments'
    },
    {
        title: 'Resolution',
        fields: [
            { key: 'accuracy', label: 'Accuracy' },
            { key: 'confirms_client_satisfaction', label: 'Confirms Client Satisfaction' }
        ],
        commentKey: 'resolution_comments'
    },
    {
        title: 'Hold Management',
        fields: [
            { key: 'notifies_hold', label: 'Notifies Hold' },
            { key: 'updates_hold', label: 'Updates Hold' }
        ],
        commentKey: 'hold_comments'
    },
    {
        title: 'Call Closing',
        fields: [{ key: 'call_closing_coutesy', label: 'Call Closing Courtesy' }],
        commentKey: 'call_closing_comments'
    }
]

// Compute QA data from raw record
const qaData = computed(() => {
    if (!props.qaRecord || !props.qas_k) return null

    // Calculate section scores
    const sections = sectionDefs.map(def => {
        let totalPoints = 0
        let maxPoints = def.fields.length

        const fields = def.fields.map(f => {
            const value = getFieldValue(f.key)
            if (value === '2') totalPoints += 1
            else if (value === '1') totalPoints += 0.5
            return { label: f.label, value: String(value) }
        })

        const scorePercent = maxPoints > 0 ? Math.round((totalPoints / maxPoints) * 100) : 0
        const comment = def.commentKey ? getFieldValue(def.commentKey) : ''

        return {
            title: def.title,
            fields,
            scorePercent,
            comment
        }
    })

    // Calculate total score
    const allFields = sectionDefs.flatMap(s => s.fields)
    let totalPoints = 0
    allFields.forEach(f => {
        const value = getFieldValue(f.key)
        if (value === '2') totalPoints += 1
        else if (value === '1') totalPoints += 0.5
    })
    const totalScore = allFields.length > 0 ? Math.round((totalPoints / allFields.length) * 100) : 0

    return {
        totalScore,
        sections,
        feedback: getFieldValue('feedback'),
        agentName: getFieldValue('chan_user_name'),
        evaluator: getFieldValue('created_by'),
        callDate: formatTimestamp(getFieldValue('chan_chan_ts')),
        createdOn: formatTimestamp(getFieldValue('created_on')),
        callId: getFieldValue('chan_uniqueid')
    }
})

const metaFields = computed(() => {
    if (!qaData.value) return []
    return [
        { label: 'Agent', value: qaData.value.agentName },
        { label: 'Evaluator', value: qaData.value.evaluator },
        { label: 'Call Date', value: qaData.value.callDate },
        { label: 'Created On', value: qaData.value.createdOn },
        { label: 'Call ID', value: qaData.value.callId },
    ]
})
</script>
