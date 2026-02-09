<template>
  <div class="flex min-h-screen" :class="isDarkMode ? 'bg-[#0B1120]' : 'bg-gray-50'">
    <!-- Fixed Sidebar - Only show when NOT on login page -->
    <Sidebar v-if="showSidebar" :isDarkMode="isDarkMode" @toggle-theme="toggleTheme" />
    
    <!-- Main Content Area with conditional left margin -->
    <div 
      class="flex-1 flex flex-col min-h-screen relative" 
      :class="[
        showSidebar ? 'ml-64' : '',
        isDarkMode ? 'bg-[#0B1120]' : 'bg-gray-50'
      ]"
    >
      <!-- Static Navbar -->
      <Navbar v-if="showSidebar" :isDarkMode="isDarkMode" />

      <!-- Main Content Container -->
      <main class="flex-1 overflow-auto p-6">
        <RouterView />
      </main>
    </div>

    <!-- Global Active Call Toolbar -->
    <ActiveCallToolbar />
  </div>
</template>

<script setup>
import { computed, provide, watch, onMounted, onBeforeUnmount } from 'vue'
import { useRoute } from 'vue-router'
import { useTheme } from '@/composables/useTheme'
import { useAuthStore } from '@/stores/auth'
import { useRealtimeStore } from '@/stores/realtime'
import { useActiveCallStore } from '@/stores/activeCall'
import Sidebar from '@/components/layout/Sidebar.vue'
import Navbar from '@/components/layout/Navbar.vue'
import ActiveCallToolbar from '@/components/softphone/ActiveCallToolbar.vue'

const route = useRoute()
const { isDarkMode, toggleTheme } = useTheme()
const authStore = useAuthStore()
const realtimeStore = useRealtimeStore()
const activeCallStore = useActiveCallStore()

// Provide theme to all child components
provide('isDarkMode', isDarkMode)
provide('toggleTheme', toggleTheme)

// Hide sidebar and navbar on login page
const showSidebar = computed(() => {
  return route.path !== '/login'
})

// ── Global Real-Time Connections ────────────────────────────────
onMounted(() => {
  if (authStore.isAuthenticated && route.path !== '/login') {
    realtimeStore.connect()
  }
})

// React to auth changes (login/logout)
watch(() => authStore.isAuthenticated, (isAuth) => {
  if (isAuth) {
    realtimeStore.connect()
  } else {
    realtimeStore.disconnect()
  }
})

onBeforeUnmount(() => {
  realtimeStore.disconnect()
})

// ── AMI → activeCall Enrichment Bridge ──────────────────────────
// When a call is active, find its AMI channel and sync UniqueID
watch(
  () => realtimeStore.amiChannelsList,
  (channels) => {
    if (!['ringing', 'active', 'calling'].includes(activeCallStore.callState)) return
    if (activeCallStore.src_uid) return // Already have it

    const ext = authStore.profile?.extension || authStore.profile?.exten
    if (!ext) return

    const match = channels.find(ch =>
      ch.CHAN_EXTEN === String(ext) ||
      ch.CHAN_CALLERID_NUM === activeCallStore.callerNumber
    )

    if (match?.CHAN_UNIQUEID) {
      console.log('[Realtime] AMI enrichment: syncing UniqueID', match.CHAN_UNIQUEID)
      activeCallStore.setAmiUniqueId(match.CHAN_UNIQUEID)
    }
  }
)
</script>