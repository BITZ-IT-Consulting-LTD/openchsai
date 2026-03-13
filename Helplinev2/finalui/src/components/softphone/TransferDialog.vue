<template>
    <Transition enter-active-class="transform transition ease-in-out duration-300" enter-from-class="translate-x-full"
        enter-to-class="translate-x-0" leave-active-class="transform transition ease-in-out duration-300"
        leave-from-class="translate-x-0" leave-to-class="translate-x-full">
        <div v-if="isOpen"
            class="fixed inset-y-0 right-0 w-[360px] z-[110] flex shadow-2xl bg-white dark:bg-neutral-900 border-l border-gray-200 dark:border-neutral-800">
            <div class="flex flex-col w-full h-full">
                <div class="p-6 border-b dark:border-neutral-800 flex justify-between items-center">
                    <h2 class="text-lg font-black dark:text-white">Transfer Call</h2>
                    <button @click="$emit('close')"
                        class="p-2 hover:bg-gray-100 dark:hover:bg-neutral-800 rounded-full">
                        <i-mdi-close class="w-5 h-5 dark:text-gray-400" />
                    </button>
                </div>

                <div class="p-6 flex-1 space-y-4">
                    <p class="text-sm dark:text-gray-400">Enter the extension or number to transfer to:</p>

                    <input v-model="target" type="text" placeholder="Extension or number..."
                        class="w-full px-4 py-3 rounded-xl border text-sm focus:ring-2 focus:ring-amber-500 focus:border-transparent outline-none dark:bg-neutral-800 dark:border-neutral-700 dark:text-white"
                        @keydown.enter="handleTransfer" />
                </div>

                <div class="p-6 border-t dark:border-neutral-800">
                    <button @click="handleTransfer" :disabled="!target.trim()"
                        class="w-full py-3 bg-amber-600 hover:bg-amber-500 text-white rounded-xl font-bold uppercase tracking-widest shadow-lg disabled:opacity-50 disabled:cursor-not-allowed">
                        Transfer
                    </button>
                </div>
            </div>
        </div>
    </Transition>

    <div v-if="isOpen" @click="$emit('close')" class="fixed inset-0 bg-black/20 z-[105] backdrop-blur-sm"></div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
    isOpen: Boolean
})

const emit = defineEmits(['close', 'transfer'])

const target = ref('')

const handleTransfer = () => {
    if (target.value.trim()) {
        emit('transfer', target.value.trim())
        target.value = ''
    }
}
</script>
