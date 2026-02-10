<template>
  <div class="space-y-6">
    <!-- AI Title Badge -->
    <div class="rounded-xl shadow-lg border p-5 transition-all duration-200"
      :class="isDarkMode ? 'bg-gray-900 border-gray-800' : 'bg-white border-gray-100'">
      <div class="flex items-center gap-3">
        <div class="w-8 h-8 rounded-lg flex items-center justify-center shrink-0 transition-colors"
          :class="isDarkMode ? 'bg-amber-500/10 text-amber-500' : 'bg-amber-600/10 text-amber-600'">
          <i-mdi-robot class="w-5 h-5" />
        </div>
        <div>
          <h3 class="text-sm font-bold leading-none mb-1" :class="isDarkMode ? 'text-[#2DD4BF]' : 'text-[#003366]'">
            Caseworker Support
          </h3>
          <p class="text-[10px] font-medium text-gray-500 leading-none">
            {{ hasRealtimeInsights ? 'Live AI analysis' : (isProcessing ? processingStatus : 'Supportive insight — human review required') }}
          </p>
        </div>
        <!-- Live Indicator -->
        <div v-if="hasRealtimeInsights" class="ml-auto flex items-center gap-1.5">
          <span class="w-2 h-2 bg-emerald-500 rounded-full animate-pulse"></span>
          <span class="text-[10px] font-black text-emerald-500 uppercase tracking-widest">Live</span>
        </div>
        <!-- Processing Indicator -->
        <div v-else-if="isProcessing" class="ml-auto">
          <div class="flex gap-1">
            <span class="w-1.5 h-1.5 bg-[#008080] rounded-full animate-bounce" style="animation-delay: 0s"></span>
            <span class="w-1.5 h-1.5 bg-[#008080] rounded-full animate-bounce" style="animation-delay: 0.2s"></span>
            <span class="w-1.5 h-1.5 bg-[#008080] rounded-full animate-bounce" style="animation-delay: 0.4s"></span>
          </div>
        </div>
      </div>
    </div>

    <!-- ═══ REAL-TIME AI INSIGHT CARDS (collapsible accordion) ═══ -->
    <template v-if="hasRealtimeInsights">
      <div class="space-y-2">
        <div v-for="(insight, idx) in sortedRealtimeInsights"
          :key="insight.notification_type + '-' + idx"
          class="rounded-xl border overflow-hidden transition-all duration-200"
          :class="isDarkMode ? 'border-neutral-700' : 'border-gray-200'">

          <!-- Accordion Header (always visible) -->
          <button @click="toggleCard(idx)"
            class="w-full flex items-center gap-2.5 px-4 py-3 text-left transition-colors"
            :class="isDarkMode
              ? 'hover:bg-neutral-800/50'
              : 'hover:bg-gray-50'">
            <div class="w-6 h-6 rounded-md flex items-center justify-center flex-shrink-0"
              :class="getCardIconStyle(insight.notification_type)">
              <i-mdi-lightbulb-on v-if="getCardMeta(insight.notification_type).color === 'indigo'" class="w-3.5 h-3.5" />
              <i-mdi-text-box v-else-if="getCardMeta(insight.notification_type).color === 'amber'" class="w-3.5 h-3.5" />
              <i-mdi-tag-multiple v-else-if="getCardMeta(insight.notification_type).color === 'violet'" class="w-3.5 h-3.5" />
              <i-mdi-shield-check v-else-if="getCardMeta(insight.notification_type).color === 'cyan'" class="w-3.5 h-3.5" />
              <i-mdi-account-search v-else-if="getCardMeta(insight.notification_type).color === 'teal'" class="w-3.5 h-3.5" />
              <i-mdi-translate v-else-if="getCardMeta(insight.notification_type).color === 'purple'" class="w-3.5 h-3.5" />
              <i-mdi-microphone v-else-if="getCardMeta(insight.notification_type).color === 'blue'" class="w-3.5 h-3.5" />
              <i-mdi-check-all v-else-if="getCardMeta(insight.notification_type).color === 'green'" class="w-3.5 h-3.5" />
              <i-mdi-information v-else class="w-3.5 h-3.5" />
            </div>
            <div class="flex-1 min-w-0">
              <div class="text-xs font-bold truncate" :class="isDarkMode ? 'text-gray-200' : 'text-gray-800'">
                {{ getCardLabel(insight.notification_type) }}
              </div>
              <div class="text-[10px] truncate" :class="isDarkMode ? 'text-gray-500' : 'text-gray-400'">
                {{ getCardSummary(insight) }}
              </div>
            </div>
            <i-mdi-chevron-down class="w-4 h-4 transition-transform duration-200 flex-shrink-0"
              :class="[
                expandedCards.has(idx) ? 'rotate-180' : '',
                isDarkMode ? 'text-gray-500' : 'text-gray-400'
              ]" />
          </button>

          <!-- Accordion Body (expandable) -->
          <div v-show="expandedCards.has(idx)" class="border-t"
            :class="isDarkMode ? 'border-neutral-700' : 'border-gray-200'">
            <component
              :is="getInsightComponent(insight.notification_type)"
              :prediction="{ created_on: toUnixTs(insight.timestamp), src_callid: insight.call_metadata?.call_id || activeCallStore.bridge_id, notification_type: insight.notification_type }"
              :payload="insight.payload || insight"
            />
          </div>
        </div>
      </div>
    </template>

    <!-- ═══ FALLBACK: Audio Upload Section (only when no real-time data) ═══ -->
    <div v-else-if="aiEnabled" class="rounded-xl shadow-lg border p-6 transition-all duration-200"
      :class="isDarkMode ? 'bg-gray-900 border-gray-800' : 'bg-white border-gray-100'">
      <div class="flex items-center justify-between mb-4">
        <h3 class="text-sm font-bold" :class="isDarkMode ? 'text-gray-100' : 'text-gray-900'">
          Call Recording
        </h3>
        <span v-if="audioFile" class="text-[10px] font-bold text-emerald-500 flex items-center gap-1">
          <i-mdi-check-circle class="w-3 h-3" />
          FILE READY
        </span>
      </div>

      <!-- Upload State -->
      <div v-if="!audioFile"
        class="group border-2 border-dashed rounded-2xl p-8 text-center transition-all duration-300 relative overflow-hidden"
        :class="[
          isDarkMode
            ? 'border-gray-800 hover:border-amber-500/50 hover:bg-gray-800/30'
            : 'border-gray-200 hover:border-amber-600/50 hover:bg-gray-50',
          isProcessing ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'
        ]" @click="!isProcessing && triggerFileInput()" @dragover.prevent
        @drop.prevent="!isProcessing && handleDrop($event)">
        <input type="file" ref="fileInput" class="hidden" accept="audio/*" @change="handleFileSelect" />
        <div class="relative z-10 flex flex-col items-center gap-2">
          <div
            class="w-12 h-12 rounded-full flex items-center justify-center mb-1 group-hover:scale-110 transition-transform duration-300"
            :class="isDarkMode ? 'bg-gray-800 text-gray-400' : 'bg-gray-100 text-gray-500'">
            <i-mdi-cloud-upload class="w-6 h-6" />
          </div>
          <p class="text-sm font-bold" :class="isDarkMode ? 'text-white' : 'text-gray-900'">
            Upload Call Audio
          </p>
          <p class="text-[11px] text-gray-500 font-medium">
            WAV, MP3 or M4A supported
          </p>
        </div>
      </div>

      <!-- Player State -->
      <div v-else class="space-y-4 animate-in fade-in slide-in-from-top-4 duration-500">
        <div class="flex items-center gap-4 p-4 rounded-xl border relative overflow-hidden"
          :class="isDarkMode ? 'bg-gray-800/40 border-gray-700' : 'bg-gray-50 border-gray-100'">
          <div class="flex-1 min-w-0">
            <p class="text-sm font-bold truncate mb-0.5" :class="isDarkMode ? 'text-white' : 'text-gray-900'">
              {{ audioFile.name }}
            </p>
            <p class="text-[11px] font-medium text-gray-500">
              {{ formatFileSize(audioFile.size) }}
            </p>
          </div>
          <button @click="removeAudio" :disabled="isProcessing"
            class="px-3 py-1.5 text-[11px] font-bold border border-red-500/30 text-red-500 rounded-lg hover:bg-red-500 hover:text-white transition-all shadow-sm active:scale-95 disabled:opacity-50">
            Remove
          </button>
        </div>

        <audio controls class="w-full h-8 opacity-90 custom-audio-player" :src="audioUrl"></audio>
      </div>
    </div>

    <!-- Processing Loader (hidden during real-time mode) -->
    <div v-if="isProcessing && !hasRealtimeInsights"
      class="p-8 rounded-xl border bg-gray-50 dark:bg-gray-900/50 border-dashed border-gray-200 dark:border-gray-800">
      <div class="flex items-center gap-4">
        <div class="relative w-10 h-10 flex-shrink-0">
          <div class="absolute inset-0 border-2 border-amber-500/20 rounded-full"></div>
          <div class="absolute inset-0 border-2 border-amber-500 border-t-transparent rounded-full animate-spin"></div>
        </div>
        <div class="flex-1 min-w-0">
          <div class="flex justify-between items-end mb-1">
            <p class="text-[10px] font-black uppercase tracking-wider text-[#003366]">{{ processingStatus }}</p>
            <p class="text-[10px] font-bold text-gray-500">{{ processingProgress }}%</p>
          </div>
          <div class="h-1 w-full bg-gray-200 dark:bg-gray-800 rounded-full overflow-hidden">
            <div class="h-full bg-[#008080] transition-all duration-500" :style="{ width: processingProgress + '%' }">
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Results Section (audio pipeline results — hidden during real-time mode) -->
    <div v-if="aiEnabled && processedData && !hasRealtimeInsights" v-show="!isProcessing"
      class="rounded-xl shadow-lg border overflow-hidden transition-all duration-500 animate-in fade-in slide-in-from-bottom-8"
      :class="isDarkMode ? 'bg-gray-900 border-gray-800' : 'bg-white border-gray-100'">
      <!-- Tab Switcher -->
      <div class="px-5 pt-5 pb-1">
        <div class="flex p-1 rounded-xl bg-gray-100/50 dark:bg-gray-800/40 gap-1">
          <button @click="activeMode = 'insights'"
            class="flex-1 py-1.5 text-[11px] font-bold transition-all duration-300 rounded-lg uppercase tracking-wider"
            :class="activeMode === 'insights'
              ? (isDarkMode ? 'bg-[#008080] text-white shadow-lg' : 'bg-[#003366] text-white shadow-lg')
              : (isDarkMode ? 'text-gray-400 hover:text-gray-200' : 'text-gray-500 hover:text-gray-700')">
            Insights
          </button>
          <button @click="activeMode = 'feedback'"
            class="flex-1 py-1.5 text-[11px] font-bold transition-all duration-300 rounded-lg uppercase tracking-wider"
            :class="activeMode === 'feedback'
              ? (isDarkMode ? 'bg-[#008080] text-white shadow-lg' : 'bg-[#003366] text-white shadow-lg')
              : (isDarkMode ? 'text-gray-400 hover:text-gray-200' : 'text-gray-500 hover:text-gray-700')">
            Feedback
          </button>
        </div>
      </div>

      <!-- Content Area -->
      <div class="p-6">
        <!-- INSIGHTS TAB -->
        <div v-if="activeMode === 'insights'" class="space-y-8 animate-in fade-in duration-500">

          <div class="space-y-6">
            <!-- Risk & Disposition Header -->
            <div class="flex items-center justify-between">
              <div class="px-3 py-1 rounded-lg border font-black text-[10px] uppercase"
                :class="getRiskColor(processedData.tabs.insights.risk_level)">
                {{ processedData.tabs.insights.risk_level }} RISK
              </div>
              <div class="text-[9px] font-bold text-gray-500 uppercase flex items-center gap-1">
                Confidence: <span class="text-emerald-500">{{ Math.round(processedData.tabs.insights.confidence_score *
                  100) }}%</span>
              </div>
            </div>

            <!-- Summary Section -->
            <div class="p-5 rounded-2xl border-2 border-[#003366]/20 bg-[#003366]/5">
              <span class="text-[9px] font-bold text-[#003366] uppercase block mb-2 tracking-widest">Rationale
                Summary</span>
              <p class="text-[11px] leading-relaxed italic font-medium"
                :class="isDarkMode ? 'text-gray-200' : 'text-gray-900'">
                "{{ processedData.tabs.insights.rationale_summary }}"
              </p>
              <div class="mt-4 pt-4 border-t border-amber-500/10">
                <span class="text-[9px] font-bold text-gray-500 uppercase block mb-1">Suggested Disposition</span>
                <p class="text-xs font-bold" :class="isDarkMode ? 'text-white' : 'text-gray-900'">{{
                  processedData.tabs.insights.suggested_disposition }}</p>
              </div>
            </div>

            <!-- Category Suggestions -->
            <div class="p-4 rounded-xl border bg-gray-50 dark:bg-gray-800/20 border-gray-200 dark:border-gray-700">
              <h4 class="text-[10px] font-black uppercase tracking-widest mb-4 opacity-70">Category Analysis</h4>
              <div class="grid grid-cols-2 gap-4">
                <div>
                  <span class="text-[8px] font-bold text-gray-500 uppercase block mb-1">Primary Category</span>
                  <p class="text-[10px] font-bold">{{ processedData.tabs.insights.category_suggestions.primary_category
                  }}</p>
                </div>
                <div>
                  <span class="text-[8px] font-bold text-gray-500 uppercase block mb-1">Recommended Intervention</span>
                  <p class="text-[10px] font-bold text-amber-500">{{
                    processedData.tabs.insights.category_suggestions.intervention }}</p>
                </div>
              </div>
            </div>

            <!-- Entities -->
            <div class="space-y-3">
              <span class="text-[9px] font-bold text-gray-500 uppercase block tracking-tighter">Extracted Entities
                Map</span>
              <div class="grid grid-cols-2 gap-3">
                <div class="p-3 rounded-xl border text-[9px]"
                  :class="isDarkMode ? 'bg-gray-950 border-gray-800' : 'bg-gray-50 border-gray-100'">
                  <span class="text-emerald-500 uppercase block mb-1.5 font-bold">Names Found</span>
                  <div class="flex flex-wrap gap-1.5">
                    <span v-for="name in processedData.tabs.insights.extracted_entities.names" :key="name"
                      class="px-1.5 py-0.5 rounded bg-emerald-500/10 text-emerald-500 border border-emerald-500/20 font-bold">{{
                        name }}</span>
                    <span v-if="!processedData.tabs.insights.extracted_entities.names?.length"
                      class="text-gray-600 italic">None</span>
                  </div>
                </div>
                <div class="p-3 rounded-xl border text-[9px]"
                  :class="isDarkMode ? 'bg-gray-950 border-gray-800' : 'bg-gray-50 border-gray-100'">
                  <span class="text-amber-500 uppercase block mb-1.5 font-bold">Locations</span>
                  <div class="flex flex-wrap gap-1.5">
                    <span v-for="loc in processedData.tabs.insights.extracted_entities.locations" :key="loc"
                      class="px-1.5 py-0.5 rounded bg-amber-500/10 text-amber-500 border border-amber-500/20 font-bold">{{
                        loc }}</span>
                    <span v-if="!processedData.tabs.insights.extracted_entities.locations?.length"
                      class="text-gray-600 italic">None</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Download Action -->
          <div class="flex pt-4">
            <button @click="downloadJson"
              class="flex-1 py-2 rounded-xl bg-gray-100 dark:bg-gray-800 text-[10px] font-bold uppercase tracking-widest hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors flex items-center justify-center gap-2">
              <i-mdi-download class="w-3.5 h-3.5" />
              Download JSON Payload
            </button>
          </div>
        </div>

        <!-- FEEDBACK TAB -->
        <div v-if="activeMode === 'feedback'"
          class="space-y-8 animate-in fade-in duration-500 max-h-[500px] overflow-y-auto pr-2 custom-scrollbar">

          <!-- Transcript Section -->
          <section class="space-y-3">
            <h5 class="text-[10px] font-black uppercase tracking-widest text-amber-500">Audio Transcript</h5>
            <div class="p-4 rounded-xl border text-[11px] leading-relaxed italic"
              :class="isDarkMode ? 'bg-gray-950 border-gray-800 text-gray-400 font-mono' : 'bg-gray-50 border-gray-200 text-gray-600'">
              {{ processedData.tabs.feedback.transcript }}
            </div>
          </section>

          <!-- Translation Section -->
          <section class="space-y-3 pt-4 border-t border-dashed"
            :class="isDarkMode ? 'border-gray-800' : 'border-gray-200'">
            <h5 class="text-[10px] font-black uppercase tracking-widest text-amber-600">Machine Translation (EN)</h5>
            <div class="p-4 rounded-xl border text-[11px] leading-relaxed italic"
              :class="isDarkMode ? 'bg-amber-500/5 border-amber-500/20 text-amber-200' : 'bg-amber-50 border-amber-100 text-amber-900'">
              {{ processedData.tabs.feedback.translation }}
            </div>
          </section>

          <!-- Classification Analysis -->
          <section class="space-y-4 pt-4 border-t border-dashed"
            :class="isDarkMode ? 'border-gray-800' : 'border-gray-200'">
            <h5 class="text-[10px] font-black uppercase tracking-widest text-emerald-500">Classifier Audit</h5>
            <div class="grid grid-cols-2 gap-3">
              <div class="p-3 rounded-xl border bg-gray-950/30 border-gray-800">
                <span class="text-[8px] font-bold text-gray-500 uppercase block mb-1">Sub-Category</span>
                <p class="text-[10px] font-bold text-gray-300">{{
                  processedData.tabs.feedback.classification.sub_category }}</p>
              </div>
              <div class="p-3 rounded-xl border bg-gray-950/30 border-gray-800">
                <span class="text-[8px] font-bold text-gray-500 uppercase block mb-1">Confidence</span>
                <p class="text-[10px] font-bold text-emerald-500">{{
                  Math.round(processedData.tabs.feedback.classification.confidence * 100) }}%</p>
              </div>
            </div>
            <div class="p-3 rounded-xl border border-emerald-500/20 bg-emerald-500/5">
              <span class="text-[8px] font-bold text-emerald-500 uppercase block mb-1">Recommended Intervention</span>
              <p class="text-[10px] font-bold text-emerald-400">{{
                processedData.tabs.feedback.classification.intervention }}</p>
            </div>
          </section>

          <!-- Summary Audit -->
          <section class="space-y-3 pt-4 border-t border-dashed"
            :class="isDarkMode ? 'border-gray-800' : 'border-gray-200'">
            <h5 class="text-[10px] font-black uppercase tracking-widest text-gray-500">Auto-Summarization</h5>
            <div class="p-4 rounded-xl border text-[10px] leading-relaxed font-bold"
              :class="isDarkMode ? 'bg-gray-950 border-gray-800 text-gray-400' : 'bg-white border-gray-100'">
              {{ processedData.tabs.feedback.summary }}
            </div>
          </section>

          <!-- QA Metrics -->
          <section class="p-4 rounded-2xl border bg-gray-950/30 border-gray-800"
            v-if="processedData.tabs.feedback.qa_scores">
            <div class="flex items-center gap-2 mb-4">
              <i-mdi-shield-check class="w-4 h-4 text-emerald-500" />
              <h5 class="text-[10px] font-black uppercase tracking-widest text-emerald-500">Counsellor QA Scores</h5>
            </div>
            <div class="grid grid-cols-3 gap-2">
              <div class="text-center p-2 rounded-lg bg-gray-800 border border-gray-700">
                <span class="text-[8px] font-bold text-gray-500 uppercase block mb-1">Opening</span>
                <span class="text-[11px] font-black text-white">{{ processedData.tabs.feedback.qa_scores.opening
                }}%</span>
              </div>
              <div class="text-center p-2 rounded-lg bg-gray-800 border border-gray-700">
                <span class="text-[8px] font-bold text-gray-500 uppercase block mb-1">Listening</span>
                <span class="text-[11px] font-black text-white">{{ processedData.tabs.feedback.qa_scores.listening
                }}%</span>
              </div>
              <div class="text-center p-2 rounded-lg bg-gray-800 border border-gray-700">
                <span class="text-[8px] font-bold text-gray-500 uppercase block mb-1">Closing</span>
                <span class="text-[11px] font-black text-white">{{ processedData.tabs.feedback.qa_scores.closing
                }}%</span>
              </div>
            </div>
          </section>

        </div>
      </div>
    </div>

    <!-- Empty State (only when no real-time insights and no audio) -->
    <div v-if="aiEnabled && !hasRealtimeInsights && !audioFile && !isProcessing" class="text-center p-12 opacity-50">
      <div
        class="w-16 h-16 rounded-full bg-gray-100 dark:bg-gray-800 flex items-center justify-center mx-auto mb-4 border-2 border-dashed border-gray-300 dark:border-gray-700">
        <i-mdi-microphone-off class="w-8 h-8 text-gray-400" />
      </div>
      <p class="text-xs font-bold uppercase tracking-widest">No audio processed yet</p>
      <p class="text-[10px] mt-1">Upload a recording to start the analysis pipeline</p>
    </div>
  </div>
</template>

<script setup>
  import { ref, reactive, inject, computed } from 'vue'
  import axios from 'axios'
  import { useActiveCallStore } from '@/stores/activeCall'

  // AI Insight Card Components
  import AiInsightsCard from '@/components/predictions/AiInsightsCard.vue'
  import AiTranscriptCard from '@/components/predictions/AiTranscriptCard.vue'
  import AiTranslationCard from '@/components/predictions/AiTranslationCard.vue'
  import AiClassificationCard from '@/components/predictions/AiClassificationCard.vue'
  import AiEntitiesCard from '@/components/predictions/AiEntitiesCard.vue'
  import AiSummaryCard from '@/components/predictions/AiSummaryCard.vue'
  import AiQaScoringCard from '@/components/predictions/AiQaScoringCard.vue'
  import AiCompleteCard from '@/components/predictions/AiCompleteCard.vue'

  const INSIGHT_COMPONENT_MAP = {
    post_call_transcription: AiTranscriptCard,
    postcall_transcription: AiTranscriptCard,
    post_call_translation: AiTranslationCard,
    postcall_translation: AiTranslationCard,
    post_call_classification: AiClassificationCard,
    postcall_classification: AiClassificationCard,
    post_call_entities: AiEntitiesCard,
    postcall_entities: AiEntitiesCard,
    post_call_summary: AiSummaryCard,
    postcall_summary: AiSummaryCard,
    post_call_summarization: AiSummaryCard,
    postcall_summarization: AiSummaryCard,
    post_call_mistral_insights: AiInsightsCard,
    postcall_mistral_insights: AiInsightsCard,
    post_call_insights: AiInsightsCard,
    postcall_insights: AiInsightsCard,
    post_call_ai_service_insights: AiInsightsCard,
    postcall_ai_service_insights: AiInsightsCard,
    post_call_qa_scoring: AiQaScoringCard,
    postcall_qa_scoring: AiQaScoringCard,
    post_call_complete: AiCompleteCard,
    postcall_complete: AiCompleteCard
  }

  const INSIGHT_PRIORITY = [
    'post_call_ai_service_insights',
    'post_call_mistral_insights',
    'post_call_insights',
    'post_call_summary',
    'post_call_summarization',
    'post_call_classification',
    'post_call_qa_scoring',
    'post_call_entities',
    'post_call_translation',
    'post_call_transcription',
    'post_call_complete'
  ]

  const normalizeNotificationType = (type) => {
    if (!type) return ''
    return type.replace(/^postcall_/, 'post_call_')
  }

  const getInsightComponent = (type) => {
    if (!type) return AiInsightsCard
    const normalized = normalizeNotificationType(type)
    return INSIGHT_COMPONENT_MAP[normalized] || INSIGHT_COMPONENT_MAP[type] || AiInsightsCard
  }

  // Convert ISO string or numeric timestamp to Unix seconds
  const toUnixTs = (ts) => {
    if (!ts) return Math.floor(Date.now() / 1000)
    if (typeof ts === 'number') return ts
    const d = new Date(ts)
    return isNaN(d.getTime()) ? Math.floor(Date.now() / 1000) : Math.floor(d.getTime() / 1000)
  }

  const props = defineProps({
    aiEnabled: {
      type: Boolean,
      default: false
    }
  })

  const activeCallStore = useActiveCallStore()
  const isDarkMode = inject('isDarkMode')
  const activeMode = ref('insights')

  // Real-time AI insights from active call
  const hasRealtimeInsights = computed(() => activeCallStore.aiInsights.length > 0)

  const sortedRealtimeInsights = computed(() => {
    return [...activeCallStore.aiInsights].sort((a, b) => {
      const idxA = INSIGHT_PRIORITY.indexOf(normalizeNotificationType(a.notification_type))
      const idxB = INSIGHT_PRIORITY.indexOf(normalizeNotificationType(b.notification_type))
      if (idxA !== -1 && idxB !== -1) return idxA - idxB
      if (idxA !== -1) return -1
      if (idxB !== -1) return 1
      return 0
    })
  })

  // ── Accordion State ──────────────────────────────────────────────
  const expandedCards = reactive(new Set([0])) // First card (Case Insights) expanded by default

  const toggleCard = (idx) => {
    if (expandedCards.has(idx)) {
      expandedCards.delete(idx)
    } else {
      expandedCards.add(idx)
    }
  }

  // Card metadata for accordion headers
  const CARD_META = {
    post_call_ai_service_insights: { label: 'Case Insights', icon: 'i-mdi-lightbulb-on', color: 'indigo' },
    post_call_insights: { label: 'Case Insights', icon: 'i-mdi-lightbulb-on', color: 'indigo' },
    post_call_mistral_insights: { label: 'Case Insights', icon: 'i-mdi-lightbulb-on', color: 'indigo' },
    post_call_summary: { label: 'Summary', icon: 'i-mdi-text-box', color: 'amber' },
    post_call_summarization: { label: 'Summary', icon: 'i-mdi-text-box', color: 'amber' },
    post_call_classification: { label: 'Classification', icon: 'i-mdi-tag-multiple', color: 'violet' },
    post_call_qa_scoring: { label: 'QA Scoring', icon: 'i-mdi-shield-check', color: 'cyan' },
    post_call_entities: { label: 'Named Entities', icon: 'i-mdi-account-search', color: 'teal' },
    post_call_translation: { label: 'Translation', icon: 'i-mdi-translate', color: 'purple' },
    post_call_transcription: { label: 'Transcript', icon: 'i-mdi-microphone', color: 'blue' },
    post_call_complete: { label: 'Processing Complete', icon: 'i-mdi-check-all', color: 'green' }
  }

  const getCardMeta = (type) => {
    const normalized = normalizeNotificationType(type)
    return CARD_META[normalized] || CARD_META[type] || { label: 'Insight', icon: 'i-mdi-information', color: 'gray' }
  }

  const getCardLabel = (type) => getCardMeta(type).label

  const COLOR_STYLES = {
    indigo: { dark: 'bg-indigo-900/30 text-indigo-400', light: 'bg-indigo-100 text-indigo-600' },
    amber: { dark: 'bg-amber-900/30 text-amber-400', light: 'bg-amber-100 text-amber-600' },
    violet: { dark: 'bg-violet-900/30 text-violet-400', light: 'bg-violet-100 text-violet-600' },
    cyan: { dark: 'bg-cyan-900/30 text-cyan-400', light: 'bg-cyan-100 text-cyan-600' },
    teal: { dark: 'bg-teal-900/30 text-teal-400', light: 'bg-teal-100 text-teal-600' },
    purple: { dark: 'bg-purple-900/30 text-purple-400', light: 'bg-purple-100 text-purple-600' },
    blue: { dark: 'bg-blue-900/30 text-blue-400', light: 'bg-blue-100 text-blue-600' },
    green: { dark: 'bg-green-900/30 text-green-400', light: 'bg-green-100 text-green-600' },
    gray: { dark: 'bg-gray-800 text-gray-400', light: 'bg-gray-100 text-gray-600' }
  }

  const getCardIconStyle = (type) => {
    const color = getCardMeta(type).color
    const styles = COLOR_STYLES[color] || COLOR_STYLES.gray
    return isDarkMode.value ? styles.dark : styles.light
  }

  const getCardSummary = (insight) => {
    const type = normalizeNotificationType(insight.notification_type)
    const p = insight.payload || {}
    if (type === 'post_call_ai_service_insights' || type === 'post_call_insights' || type === 'post_call_mistral_insights') {
      const cls = p.insights?.classification || p.insights?.category_suggestions || p.category_suggestions || {}
      return cls.primary_category ? `${cls.primary_category} — ${cls.sub_category || ''}` : 'AI analysis available'
    }
    if (type === 'post_call_summary' || type === 'post_call_summarization') {
      const s = p.summary || ''
      return s.length > 60 ? s.slice(0, 60) + '...' : s || 'Call summary'
    }
    if (type === 'post_call_classification') {
      const cls = p.classification || {}
      return cls.main_category ? `${cls.main_category} / ${cls.sub_category || ''}` : 'Classification results'
    }
    if (type === 'post_call_qa_scoring') return 'Quality assurance metrics'
    if (type === 'post_call_entities') return 'Extracted names & locations'
    if (type === 'post_call_translation') return p.target_language ? `Translated to ${p.target_language}` : 'Translated text'
    if (type === 'post_call_transcription') return p.language ? `Language: ${p.language}` : 'Audio transcript'
    if (type === 'post_call_complete') return 'All AI tasks finished'
    return 'Tap to expand'
  }

  const isProcessing = ref(false)
  const processingStatus = ref('Ready')
  const processingProgress = ref(0)

  // File Input State
  const fileInput = ref(null)
  const audioFile = ref(null)
  const audioUrl = ref(null)

  // Pipeline Data State
  const processedData = ref(null)

  // Trigger functions
  const triggerFileInput = () => {
    if (fileInput.value) {
      fileInput.value.click()
    }
  }

  const handleFileSelect = (event) => {
    const file = event.target.files[0]
    if (file) {
      processFile(file)
    }
  }

  const handleDrop = (event) => {
    const file = event.dataTransfer.files[0]
    if (file && file.type.startsWith('audio/')) {
      processFile(file)
    }
  }

  const processFile = (file) => {
    audioFile.value = file
    audioUrl.value = URL.createObjectURL(file)
    runAiPipeline(file)
  }

  /**
   * Main AI Pipeline Workflow
   * 1. Upload -> task_id
   * 2. Poll status until completed
   * 3. Render tabs
   */
  const runAiPipeline = async (file) => {
    isProcessing.value = true
    processingStatus.value = 'Uploading audio...'
    processingProgress.value = 10

    try {
      const formData = new FormData()
      formData.append('audio', file)
      formData.append('language', 'sw')
      formData.append('include_translation', 'true')
      formData.append('include_insights', 'true')
      formData.append('background', 'true')

      // Step 1: Submit to processing pipeline
      const uploadResponse = await axios.post('/audio-api/audio/process', formData)
      const { task_id } = uploadResponse.data

      if (!task_id) {
        throw new Error('No task_id received from server')
      }

      processingStatus.value = 'Task queued...'
      processingProgress.value = 25

      // Step 2: Begin Polling
      await pollTaskStatus(task_id)

    } catch (error) {
      console.error('[AI Workflow] Pipeline Error:', error)
      processingStatus.value = 'Processing failed'
      isProcessing.value = false
      alert(`AI Processing Failed: ${error.message}`)
    }
  }

  /**
   * Polling Logic
   * Every 2s for 4 attempts, then 4s. Stop after 5 mins.
   */
  const pollTaskStatus = async (taskId) => {
    let attempts = 0
    const startTime = Date.now()
    const MAX_DURATION = 5 * 60 * 1000 // 5 minutes

    const poll = async () => {
      if (Date.now() - startTime > MAX_DURATION) {
        processingStatus.value = 'Polling timeout'
        isProcessing.value = false
        return
      }

      try {
        const response = await axios.get(`/audio-api/audio/task/${taskId}`)
        const task = response.data

        if (task.status === 'completed') {
          renderResults(task.result.result)
          return
        }

        if (task.status === 'failed') {
          processingStatus.value = `Failed: ${task.error || 'Unknown error'}`
          isProcessing.value = false
          return
        }

        // Update progress if available
        if (task.status === 'processing') {
          processingStatus.value = 'Analysing content...'
          processingProgress.value = Math.min(95, 25 + (attempts * 5))
        } else if (task.status === 'queued') {
          processingStatus.value = 'Waiting in queue...'
          processingProgress.value = 20
        }

        attempts++
        const delay = attempts <= 4 ? 2000 : 4000
        setTimeout(poll, delay)

      } catch (error) {
        console.error('[AI Polling] Error:', error)
        // Retry after delay
        setTimeout(poll, 4000)
      }
    }

    await poll()
  }

  /**
   * Final Rendering Logic
   * Transforms raw pipeline results into UI components
   */
  const renderResults = (raw) => {
    console.log('[AI Workflow] Rendering Results. Raw data:', raw)

    try {
      // Some AI prompts return everything nested under "tabs", others return direct fields.
      // We normalize to a "source" object.
      const source = raw?.tabs ? raw.tabs : raw;

      // Extract Insights with fallbacks for both Step 992 and Step 1006 schemas
      const insightsSource = source?.insights || {};
      const feedbackSource = source?.feedback || {};

      processedData.value = {
        workflow_status: 'completed',
        tabs: {
          insights: {
            risk_level: insightsSource.risk_level || 'Medium',
            suggested_disposition: insightsSource.suggested_disposition || insightsSource.recommended_action || 'Follow-up required',
            rationale_summary: insightsSource.rationale_summary || insightsSource.corrected_summary || source.summary || 'Summary not available.',
            confidence_score: insightsSource.confidence_score || 0.88,
            extracted_entities: {
              names: insightsSource.extracted_entities?.names || insightsSource.entities_to_capture?.child_name || [],
              locations: insightsSource.extracted_entities?.locations || insightsSource.entities_to_capture?.location || []
            },
            category_suggestions: {
              primary_category: insightsSource.category_suggestions?.primary_category || insightsSource.primary_case_type || source.classification?.main_category || 'General Enquiry',
              intervention: insightsSource.category_suggestions?.intervention || insightsSource.recommended_action || source.classification?.intervention || 'Support',
              priority: insightsSource.category_suggestions?.priority || insightsSource.priority || source.classification?.priority || '3'
            }
          },
          feedback: {
            // Handle both string and object formats for components
            transcript: feedbackSource.transcript?.text || feedbackSource.transcript || source.transcript || 'Transcript missing.',
            translation: feedbackSource.translation?.text || feedbackSource.translation || source.translation || 'Translation missing.',
            classification: feedbackSource.classification || source.classification || {},
            summary: feedbackSource.summarization?.corrected_summary || feedbackSource.summary || source.summary || 'Summary missing.',
            qa_scores: feedbackSource.qa_feedback || feedbackSource.qa_scores || source.qa_scores || null
          }
        }
      }

      console.log('[AI Workflow] Processed Data for UI:', processedData.value)
      isProcessing.value = false
      activeMode.value = 'insights'
    } catch (err) {
      console.error('[AI Workflow] Error during rendering:', err)
      isProcessing.value = false
      alert('Failed to render AI results. Check console for details.')
    }
  }

  const removeAudio = () => {
    audioFile.value = null
    audioUrl.value = null
    processedData.value = null
    processingProgress.value = 0
    if (fileInput.value) fileInput.value.value = ''
  }

  const downloadJson = () => {
    if (!processedData.value) return
    const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(processedData.value, null, 2))
    const downloadAnchorNode = document.createElement('a')
    downloadAnchorNode.setAttribute("href", dataStr)
    downloadAnchorNode.setAttribute("download", `ai_analysis_${new Date().getTime()}.json`)
    document.body.appendChild(downloadAnchorNode)
    downloadAnchorNode.click()
    downloadAnchorNode.remove()
  }

  const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 Bytes'
    const k = 1024
    const sizes = ['Bytes', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
  }

  const getRiskColor = (level) => {
    const l = (level || '').toLowerCase()
    if (l === 'high' || l === 'critical' || l === '1') return 'bg-[#003366]/10 text-[#003366] border-[#003366]/20'
    if (l === 'medium' || l === '2') return 'bg-[#008080]/10 text-[#2DD4BF] border-[#2DD4BF]/20'
    return 'bg-gray-100 text-gray-600 border-gray-200'
  }
</script>

<style scoped>
  .custom-audio-player::-webkit-media-controls-enclosure {
    background-color: transparent;
  }

  .custom-scrollbar::-webkit-scrollbar {
    width: 4px;
  }

  .custom-scrollbar::-webkit-scrollbar-track {
    background: transparent;
  }

  .custom-scrollbar::-webkit-scrollbar-thumb {
    background: rgba(155, 155, 155, 0.2);
    border-radius: 10px;
  }

  @keyframes fadeIn {
    from {
      opacity: 0;
      transform: translateY(10px);
    }

    to {
      opacity: 1;
      transform: translateY(0);
    }
  }

  .animate-in {
    animation: fadeIn 0.4s ease-out forwards;
  }
</style>
