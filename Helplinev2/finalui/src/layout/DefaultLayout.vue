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
import { computed, provide, watch, ref, onMounted, onBeforeUnmount } from 'vue'
import { useRoute } from 'vue-router'
import { useTheme } from '@/composables/useTheme'
import { useAuthStore } from '@/stores/auth'
import { useRealtimeStore } from '@/stores/realtime'
import { useActiveCallStore } from '@/stores/activeCall'
import axiosInstance from '@/utils/axios'
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
// When a call is active, find its AMI channel and sync UniqueID + BridgeID
watch(
  () => realtimeStore.amiChannelsList,
  (channels) => {
    if (!['ringing', 'active', 'calling'].includes(activeCallStore.callState)) return

    const ext = authStore.profile?.extension || authStore.profile?.exten
    if (!ext) return

    const match = channels.find(ch =>
      ch.CHAN_EXTEN === String(ext) ||
      ch.CHAN_CALLERID_NUM === activeCallStore.callerNumber
    )

    if (match) {
      if (!activeCallStore.src_uid && match.CHAN_UNIQUEID) {
        console.log('[Realtime] AMI enrichment: syncing UniqueID', match.CHAN_UNIQUEID)
        activeCallStore.setAmiUniqueId(match.CHAN_UNIQUEID)
      }
      if (match.CHAN_BRIDGE_ID) {
        activeCallStore.setBridgeId(match.CHAN_BRIDGE_ID)
      }
    }
  }
)

// ── ATI → activeCall AI Insights Bridge ─────────────────────────
// Monitors ATI text channel for AI notifications (src='aii', context='trunk')
// and matches them against the active call via bridge_id or uniqueid, then
// fetches the full insight payloads from the predictions API.
//
// Key: The AI service sends notifications with ATI_BRIDGE_ID = call UniqueID
// (e.g. "1770654584.401"), NOT the Asterisk bridge UUID. Also, insights arrive
// AFTER the call ends (20-120s processing), so we must keep matching even
// during case-creation after wrapup.
const _aiFetchInProgress = ref(false)
const _lastCallUniqueId = ref('')
const _fetchedCallIds = new Set() // Calls we've already fetched insights for
let _retryTimer = null

// Persist the call's UniqueID so it survives wrapup/idle transitions
watch(() => activeCallStore.src_uid, (uid) => {
  if (uid) {
    console.log('[AI Panel] Tracking call UniqueID:', uid)
    _lastCallUniqueId.value = uid
  }
})

// Core function: fetch all individual AI messages for a call via two-step API
async function fetchAiInsightsForCall(queryCallId) {
  if (_aiFetchInProgress.value) return
  _aiFetchInProgress.value = true

  try {
    console.log('[AI Panel] Fetching insights for call_id:', queryCallId)

    // Step 1: Get conversation list to find the pmessage ID
    const { data: listData } = await axiosInstance.get('api/pmessages/', {
      params: { src_callid: queryCallId, src: 'aii', _c: 30 },
      headers: { 'Session-Id': authStore.sessionId }
    })

    const conversations = listData.pmessages || []
    const listKeys = listData.pmessages_k || {}

    if (!conversations.length || !listKeys.id) {
      console.log('[AI Panel] No conversations found for call_id:', queryCallId)
      return
    }

    const idIdx = listKeys.id[0]

    // Step 2: For each conversation, fetch ALL individual messages
    for (const conv of conversations) {
      const pmessageId = conv[idIdx]
      if (!pmessageId) continue

      console.log('[AI Panel] Fetching message details for pmessage:', pmessageId)

      const { data: detailData } = await axiosInstance.get(`api/pmessages/${pmessageId}?`, {
        headers: { 'Session-Id': authStore.sessionId }
      })

      // Step 3: Parse individual messages from the detail response
      if (detailData.messages && detailData.messages_k) {
        const msgKeys = detailData.messages_k
        const srcMsgIdx = msgKeys.src_msg ? msgKeys.src_msg[0] : -1

        if (srcMsgIdx === -1) continue

        let added = 0
        for (const row of detailData.messages) {
          const rawMsg = row[srcMsgIdx]
          if (!rawMsg) continue

          try {
            const decoded = JSON.parse(atob(rawMsg))
            if (decoded && decoded.notification_type) {
              activeCallStore.addAiInsight(decoded)
              added++
            }
          } catch (e) {
            // Skip non-JSON or invalid base64 entries
          }
        }
        console.log(`[AI Panel] Decoded ${added} insights from pmessage ${pmessageId} (${detailData.messages.length} total messages)`)
      }
    }
  } catch (err) {
    console.warn('[AI Panel] Failed to fetch AI insights:', err.message)
  } finally {
    _aiFetchInProgress.value = false
  }
}

watch(
  () => realtimeStore.aiNotifications,
  async (notifications) => {
    if (!notifications.length) return

    // Allow processing during active call, wrapup, OR while on case-creation page
    const isActiveCall = ['active', 'wrapup'].includes(activeCallStore.callState)
    const isCaseCreation = route.path.includes('case-creation')

    if (!isActiveCall && !isCaseCreation) return

    // Collect all possible IDs to match against ATI_BRIDGE_ID
    const callIds = new Set()
    if (activeCallStore.bridge_id) callIds.add(activeCallStore.bridge_id)
    if (activeCallStore.src_uid) callIds.add(activeCallStore.src_uid)
    if (_lastCallUniqueId.value) callIds.add(_lastCallUniqueId.value)
    if (route.query.uniqueid) callIds.add(route.query.uniqueid)

    if (callIds.size === 0) return

    // Find matching notification
    const matchedNotif = notifications.find(n => callIds.has(n.ATI_BRIDGE_ID))
    if (!matchedNotif) return

    const queryCallId = matchedNotif.ATI_BRIDGE_ID

    // Already fetched for this call — skip
    if (_fetchedCallIds.has(queryCallId)) return

    // Prevent concurrent fetches
    if (_aiFetchInProgress.value) return

    console.log('[AI Panel] ATI notification matched call_id:', queryCallId)

    // Mark as fetched so we don't re-trigger on every ATI poll
    _fetchedCallIds.add(queryCallId)

    // Immediate fetch
    await fetchAiInsightsForCall(queryCallId)

    // Schedule a retry after 15s to catch any late-arriving insights
    // (AI pipeline may still be writing messages)
    if (_retryTimer) clearTimeout(_retryTimer)
    _retryTimer = setTimeout(() => {
      console.log('[AI Panel] Retry fetch for late-arriving insights:', queryCallId)
      fetchAiInsightsForCall(queryCallId)
    }, 15000)
  },
  { deep: true }
)
</script>