<template>
    <div class="relative" v-if="canSupervise">
        <button @click="isOpen = !isOpen"
            class="px-2 py-1 text-xs font-medium rounded-lg transition-colors"
            :class="isDarkMode
                ? 'bg-neutral-800 text-gray-300 hover:bg-neutral-700'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'">
            <i-mdi-dots-vertical class="w-4 h-4" />
        </button>

        <Transition enter-active-class="transition ease-out duration-100"
            enter-from-class="transform opacity-0 scale-95"
            enter-to-class="transform opacity-100 scale-100"
            leave-active-class="transition ease-in duration-75"
            leave-from-class="transform opacity-100 scale-100"
            leave-to-class="transform opacity-0 scale-95">
            <div v-if="isOpen"
                class="absolute right-0 top-full mt-1 w-44 rounded-xl shadow-xl border z-50 py-1 overflow-hidden"
                :class="isDarkMode
                    ? 'bg-neutral-900 border-neutral-800'
                    : 'bg-white border-gray-200'">

                <button v-for="action in actions" :key="action.code"
                    @click="handleAction(action)"
                    class="w-full px-4 py-2.5 text-left text-xs font-medium flex items-center gap-3 transition-colors"
                    :class="isDarkMode
                        ? 'text-gray-300 hover:bg-neutral-800'
                        : 'text-gray-700 hover:bg-gray-50'"
                    :disabled="loading">
                    <component :is="action.icon" class="w-4 h-4" :class="action.color" />
                    {{ action.label }}
                </button>
            </div>
        </Transition>
    </div>
</template>

<script setup>
import { ref, inject, computed, onMounted, onUnmounted } from 'vue'
import { toast } from 'vue-sonner'
import { useRealtimeStore } from '@/stores/realtime'
import { useAuthStore } from '@/stores/auth'

const props = defineProps({
    channel: { type: String, required: true },
    agentName: { type: String, default: '' }
})

const isDarkMode = inject('isDarkMode')
const realtimeStore = useRealtimeStore()
const authStore = useAuthStore()

const isOpen = ref(false)
const loading = ref(false)

const canSupervise = computed(() => {
    return authStore.isSupervisor || authStore.isAdministrator
})

const actions = [
    { code: 2, label: 'Spy (Listen)', icon: 'i-mdi-ear-hearing', color: 'text-blue-500' },
    { code: 3, label: 'Whisper', icon: 'i-mdi-account-voice', color: 'text-amber-500' },
    { code: 4, label: 'Barge In', icon: 'i-mdi-phone-plus', color: 'text-emerald-500' },
    { code: 9, label: 'Force Logout', icon: 'i-mdi-account-off', color: 'text-red-500' }
]

const handleAction = async (action) => {
    loading.value = true
    isOpen.value = false
    try {
        await realtimeStore.supervisorAction(action.code, props.channel)
        toast.success(`${action.label} initiated${props.agentName ? ' for ' + props.agentName : ''}`)
    } catch (e) {
        toast.error(`${action.label} failed`, { description: e.message })
    } finally {
        loading.value = false
    }
}

// Close on outside click
const closeOnOutsideClick = (e) => {
    if (!e.target.closest('.relative')) isOpen.value = false
}
onMounted(() => document.addEventListener('click', closeOnOutsideClick))
onUnmounted(() => document.removeEventListener('click', closeOnOutsideClick))
</script>
