<template>
    <div class="rounded-xl border p-5 shadow-sm transition-all hover:shadow-md"
        :class="isDarkMode ? 'bg-neutral-800/50 border-neutral-700' : 'bg-white border-gray-100'">

        <!-- Header -->
        <div class="flex items-center justify-between mb-4">
            <div class="flex items-center gap-2">
                <span class="px-2.5 py-1 rounded-md text-[10px] font-bold uppercase tracking-widest border"
                    :class="isDarkMode ? 'bg-indigo-900/30 text-indigo-300 border-indigo-800' : 'bg-indigo-50 text-indigo-600 border-indigo-100'">
                    Case Insights
                </span>
                <span class="text-xs font-mono" :class="isDarkMode ? 'text-gray-500' : 'text-gray-400'">{{ formatTime(prediction.created_on) }}</span>
            </div>
            <div class="flex gap-2">
                <div v-if="uiMetadata.alert_type"
                    class="px-2 py-1 rounded text-[10px] font-black uppercase flex items-center gap-1 shadow-sm"
                    :class="uiMetadata.alert_type === 'critical' ? 'bg-red-500 text-white' : 'bg-amber-500 text-white'">
                    <i-mdi-alert-circle class="w-3 h-3" />
                    {{ uiMetadata.alert_type }}
                </div>
                <div v-if="riskLevel" class="px-2 py-1 rounded text-[10px] font-black uppercase"
                    :class="getRiskColor(riskLevel)">
                    {{ riskLevel }} Risk
                </div>
            </div>
        </div>

        <div class="space-y-4">

            <!-- Safety Alert Banner -->
            <div v-if="decisionPanel.immediate_safety_alert"
                class="p-3 rounded-lg border-2 flex items-center gap-2 border-red-500 bg-red-500/10">
                <i-mdi-alert-octagon class="w-5 h-5 text-red-500 flex-shrink-0" />
                <div>
                    <div class="text-xs font-black uppercase text-red-500">Immediate Safety Alert</div>
                    <div v-if="decisionPanel.safety_alert_reason" class="text-sm mt-0.5"
                        :class="isDarkMode ? 'text-red-300' : 'text-red-700'">
                        {{ decisionPanel.safety_alert_reason }}
                    </div>
                </div>
            </div>

            <!-- AI Decision Panel -->
            <div v-if="hasDecisionPanel" class="p-4 rounded-xl border space-y-3"
                :class="isDarkMode ? 'bg-indigo-950/30 border-indigo-900/50' : 'bg-indigo-50/50 border-indigo-100'">
                <div class="text-[10px] uppercase font-bold tracking-wider"
                    :class="isDarkMode ? 'text-indigo-400' : 'text-indigo-600'">AI Decision Panel</div>

                <div v-if="decisionPanel.case_headline" class="text-sm font-bold"
                    :class="isDarkMode ? 'text-white' : 'text-gray-900'">
                    {{ decisionPanel.case_headline }}
                </div>

                <div v-if="decisionPanel.recommended_next_step" class="p-3 rounded-lg border"
                    :class="isDarkMode ? 'bg-neutral-900 border-neutral-700' : 'bg-white border-gray-200'">
                    <div class="text-[10px] uppercase font-bold tracking-wider mb-1"
                        :class="isDarkMode ? 'text-gray-400' : 'text-gray-500'">Recommended Next Step</div>
                    <div class="text-sm font-semibold" :class="isDarkMode ? 'text-white' : 'text-gray-900'">
                        {{ decisionPanel.recommended_next_step }}
                    </div>
                    <div v-if="decisionPanel.recommended_timeframe"
                        class="text-[10px] mt-1 font-bold uppercase"
                        :class="decisionPanel.recommended_timeframe === 'Immediate' ? 'text-red-500' : (isDarkMode ? 'text-amber-400' : 'text-amber-600')">
                        {{ decisionPanel.recommended_timeframe }}
                    </div>
                </div>

                <!-- Survivor-Centred Guidance -->
                <div v-if="decisionPanel.survivor_centred_guidance?.length">
                    <div class="text-[10px] uppercase font-bold tracking-wider mb-2"
                        :class="isDarkMode ? 'text-gray-400' : 'text-gray-500'">Counsellor Guidance</div>
                    <ul class="space-y-1.5">
                        <li v-for="(tip, idx) in decisionPanel.survivor_centred_guidance" :key="idx"
                            class="flex items-start gap-2 text-xs"
                            :class="isDarkMode ? 'text-gray-300' : 'text-gray-700'">
                            <i-mdi-check-circle class="w-3.5 h-3.5 text-emerald-500 flex-shrink-0 mt-0.5" />
                            {{ tip }}
                        </li>
                    </ul>
                </div>
            </div>

            <!-- Rationale / Case Overview -->
            <div v-if="caseOverview.rationale_summary" class="text-sm leading-relaxed"
                :class="isDarkMode ? 'text-gray-300' : 'text-gray-700'">
                <p>{{ caseOverview.rationale_summary }}</p>
            </div>

            <!-- Classification -->
            <div v-if="classification.primary_category" class="p-4 rounded-xl border space-y-3"
                :class="isDarkMode ? 'bg-neutral-900/50 border-neutral-700' : 'bg-gray-50 border-gray-100'">
                <div class="text-[10px] uppercase font-bold tracking-wider"
                    :class="isDarkMode ? 'text-gray-400' : 'text-gray-500'">Classification</div>
                <div class="grid grid-cols-2 gap-3">
                    <div>
                        <div class="text-[10px] uppercase" :class="isDarkMode ? 'text-gray-500' : 'text-gray-400'">Category</div>
                        <div class="text-sm font-bold" :class="isDarkMode ? 'text-white' : 'text-gray-900'">{{ classification.primary_category }}</div>
                    </div>
                    <div v-if="classification.sub_category">
                        <div class="text-[10px] uppercase" :class="isDarkMode ? 'text-gray-500' : 'text-gray-400'">Sub-Category</div>
                        <div class="text-sm font-bold" :class="isDarkMode ? 'text-white' : 'text-gray-900'">{{ classification.sub_category }}</div>
                    </div>
                    <div v-if="classification.intervention">
                        <div class="text-[10px] uppercase" :class="isDarkMode ? 'text-gray-500' : 'text-gray-400'">Intervention</div>
                        <div class="text-xs font-semibold px-2 py-0.5 rounded-md inline-block mt-1"
                            :class="isDarkMode ? 'bg-indigo-900/40 text-indigo-300' : 'bg-indigo-100 text-indigo-700'">
                            {{ classification.intervention }}
                        </div>
                    </div>
                    <div v-if="classification.priority">
                        <div class="text-[10px] uppercase" :class="isDarkMode ? 'text-gray-500' : 'text-gray-400'">Priority</div>
                        <div class="text-sm font-bold" :class="isDarkMode ? 'text-white' : 'text-gray-900'">{{ classification.priority }}</div>
                    </div>
                </div>
            </div>

            <!-- VAC Incident Profile -->
            <div v-if="hasIncidentProfile" class="p-4 rounded-xl border space-y-3"
                :class="isDarkMode ? 'bg-neutral-900/50 border-neutral-700' : 'bg-gray-50 border-gray-100'">
                <div class="text-[10px] uppercase font-bold tracking-wider"
                    :class="isDarkMode ? 'text-gray-400' : 'text-gray-500'">Incident Profile</div>
                <div class="grid grid-cols-2 gap-3">
                    <div v-if="incidentProfile.violence_type">
                        <div class="text-[10px] uppercase" :class="isDarkMode ? 'text-gray-500' : 'text-gray-400'">Violence Type</div>
                        <div class="text-sm font-bold" :class="isDarkMode ? 'text-white' : 'text-gray-900'">{{ incidentProfile.violence_type }}</div>
                    </div>
                    <div v-if="incidentProfile.incident_setting">
                        <div class="text-[10px] uppercase" :class="isDarkMode ? 'text-gray-500' : 'text-gray-400'">Setting</div>
                        <div class="text-sm font-bold" :class="isDarkMode ? 'text-white' : 'text-gray-900'">{{ incidentProfile.incident_setting }}</div>
                    </div>
                    <div v-if="incidentProfile.perpetrator_relationship">
                        <div class="text-[10px] uppercase" :class="isDarkMode ? 'text-gray-500' : 'text-gray-400'">Perpetrator Relationship</div>
                        <div class="text-sm font-bold" :class="isDarkMode ? 'text-white' : 'text-gray-900'">{{ incidentProfile.perpetrator_relationship }}</div>
                    </div>
                </div>
                <!-- Danger Indicators -->
                <div class="flex flex-wrap gap-2">
                    <span v-if="incidentProfile.child_in_immediate_danger"
                        class="text-[10px] px-2 py-0.5 rounded-full font-bold bg-red-500/15 text-red-500 border border-red-500/25">
                        Child in Immediate Danger
                    </span>
                    <span v-if="incidentProfile.incident_reported_as_ongoing"
                        class="text-[10px] px-2 py-0.5 rounded-full font-bold bg-amber-500/15 text-amber-500 border border-amber-500/25">
                        Ongoing Incident
                    </span>
                </div>
            </div>

            <!-- Safeguarding Flags -->
            <div v-if="activeFlags.length" class="p-4 rounded-xl border space-y-3"
                :class="isDarkMode ? 'bg-neutral-900/50 border-neutral-700' : 'bg-gray-50 border-gray-100'">
                <div class="text-[10px] uppercase font-bold tracking-wider"
                    :class="isDarkMode ? 'text-gray-400' : 'text-gray-500'">Safeguarding Flags</div>
                <div class="flex flex-wrap gap-2">
                    <span v-for="flag in activeFlags" :key="flag"
                        class="text-[10px] px-2 py-1 rounded-md font-bold border flex items-center gap-1"
                        :class="getFlagColor(flag)">
                        <i-mdi-flag class="w-3 h-3" />
                        {{ flag }}
                    </span>
                </div>
            </div>

            <!-- Persons Involved -->
            <div v-if="hasPersonsInvolved" class="p-4 rounded-xl border space-y-3"
                :class="isDarkMode ? 'bg-neutral-900/50 border-neutral-700' : 'bg-gray-50 border-gray-100'">
                <div class="text-[10px] uppercase font-bold tracking-wider"
                    :class="isDarkMode ? 'text-gray-400' : 'text-gray-500'">Persons Involved</div>
                <!-- Survivors -->
                <div v-if="personsInvolved.survivors?.length">
                    <div class="text-[10px] uppercase mb-1.5" :class="isDarkMode ? 'text-blue-400' : 'text-blue-600'">Survivors</div>
                    <div v-for="(s, idx) in personsInvolved.survivors" :key="'s-'+idx"
                        class="text-xs mb-1 flex items-center gap-2"
                        :class="isDarkMode ? 'text-gray-300' : 'text-gray-700'">
                        <i-mdi-account class="w-3.5 h-3.5 flex-shrink-0" :class="isDarkMode ? 'text-blue-400' : 'text-blue-500'" />
                        <span>{{ s.name || 'Unknown' }}</span>
                        <span v-if="s.age" class="text-[10px]" :class="isDarkMode ? 'text-gray-500' : 'text-gray-400'">Age: {{ s.age }}</span>
                        <span v-if="s.gender" class="text-[10px]" :class="isDarkMode ? 'text-gray-500' : 'text-gray-400'">{{ s.gender }}</span>
                    </div>
                </div>
                <!-- Alleged Perpetrators -->
                <div v-if="personsInvolved.alleged_perpetrators?.length">
                    <div class="text-[10px] uppercase mb-1.5" :class="isDarkMode ? 'text-red-400' : 'text-red-600'">Alleged Perpetrators</div>
                    <div v-for="(p, idx) in personsInvolved.alleged_perpetrators" :key="'p-'+idx"
                        class="text-xs mb-1 flex items-center gap-2"
                        :class="isDarkMode ? 'text-gray-300' : 'text-gray-700'">
                        <i-mdi-account-alert class="w-3.5 h-3.5 flex-shrink-0" :class="isDarkMode ? 'text-red-400' : 'text-red-500'" />
                        <span>{{ p.name || 'Unknown' }}</span>
                        <span v-if="p.relationship_to_survivor" class="text-[10px] px-1.5 py-0.5 rounded border"
                            :class="isDarkMode ? 'bg-neutral-800 border-neutral-600 text-gray-400' : 'bg-gray-100 border-gray-200 text-gray-500'">
                            {{ p.relationship_to_survivor }}
                        </span>
                    </div>
                </div>
            </div>

            <!-- Service & Referral Plan -->
            <div v-if="hasReferralPlan" class="p-4 rounded-xl border space-y-3"
                :class="isDarkMode ? 'bg-neutral-900/50 border-neutral-700' : 'bg-gray-50 border-gray-100'">
                <div class="text-[10px] uppercase font-bold tracking-wider"
                    :class="isDarkMode ? 'text-gray-400' : 'text-gray-500'">Service & Referral Plan</div>
                <!-- Alert tags -->
                <div class="flex flex-wrap gap-2">
                    <span v-if="referralPlan.immediate_referral_needed"
                        class="text-[10px] px-2 py-0.5 rounded-full font-bold bg-red-500/15 text-red-500 border border-red-500/25">
                        Immediate Referral Needed
                    </span>
                    <span v-if="referralPlan.mandatory_reporting_required"
                        class="text-[10px] px-2 py-0.5 rounded-full font-bold bg-amber-500/15 text-amber-500 border border-amber-500/25">
                        Mandatory Reporting Required
                    </span>
                    <span v-if="referralPlan.follow_up_required"
                        class="text-[10px] px-2 py-0.5 rounded-full font-bold bg-blue-500/15 text-blue-500 border border-blue-500/25">
                        Follow-up Required
                    </span>
                </div>
                <!-- Referrals -->
                <div v-if="referralPlan.recommended_referrals?.length">
                    <div class="text-[10px] uppercase mb-1.5" :class="isDarkMode ? 'text-gray-500' : 'text-gray-400'">Recommended Referrals</div>
                    <div class="flex flex-wrap gap-1.5">
                        <span v-for="ref in referralPlan.recommended_referrals" :key="ref"
                            class="text-[11px] px-2 py-0.5 rounded-md font-medium border"
                            :class="isDarkMode ? 'bg-neutral-800 border-neutral-600 text-gray-300' : 'bg-white border-gray-200 text-gray-700'">
                            {{ ref }}
                        </span>
                    </div>
                </div>
                <!-- Services -->
                <div v-if="referralPlan.recommended_services?.length">
                    <div class="text-[10px] uppercase mb-1.5" :class="isDarkMode ? 'text-gray-500' : 'text-gray-400'">Recommended Services</div>
                    <div class="flex flex-wrap gap-1.5">
                        <span v-for="svc in referralPlan.recommended_services" :key="svc"
                            class="text-[11px] px-2 py-0.5 rounded-md font-medium border"
                            :class="isDarkMode ? 'bg-neutral-800 border-neutral-600 text-gray-300' : 'bg-white border-gray-200 text-gray-700'">
                            {{ svc }}
                        </span>
                    </div>
                </div>
            </div>

            <!-- Extracted Entities -->
            <div v-if="hasEntities"
                class="p-4 rounded-xl border space-y-3"
                :class="isDarkMode ? 'bg-neutral-900/50 border-neutral-700' : 'bg-gray-50 border-gray-100'">
                <div class="text-[10px] uppercase font-bold tracking-wider"
                    :class="isDarkMode ? 'text-gray-400' : 'text-gray-500'">Extracted Entities</div>
                <div class="space-y-2">
                    <div v-if="flattenedNames.length" class="flex flex-wrap gap-2">
                        <span v-for="(name, idx) in flattenedNames" :key="'n-' + idx"
                            class="text-[11px] px-2 py-0.5 rounded-full border bg-blue-500/10 border-blue-500/20 text-blue-400">
                            {{ name }}
                        </span>
                    </div>
                    <div v-if="flattenedLocations.length" class="flex flex-wrap gap-2">
                        <span v-for="(loc, idx) in flattenedLocations" :key="'l-' + idx"
                            class="text-[11px] px-2 py-1 rounded-full border bg-emerald-500/10 border-emerald-500/20 text-emerald-400 flex items-center gap-1.5">
                            <i-mdi-map-marker class="w-3 h-3 flex-shrink-0" />
                            {{ loc }}
                        </span>
                    </div>
                    <div v-if="flattenedOrganizations.length" class="flex flex-wrap gap-2">
                        <span v-for="(org, idx) in flattenedOrganizations" :key="'o-' + idx"
                            class="text-[11px] px-2 py-0.5 rounded-full border bg-purple-500/10 border-purple-500/20 text-purple-400">
                            {{ org }}
                        </span>
                    </div>
                </div>
            </div>

            <!-- Disposition -->
            <div v-if="caseOverview.suggested_disposition" class="p-3 rounded-lg border text-sm"
                :class="isDarkMode ? 'bg-neutral-900 border-neutral-700' : 'bg-gray-50 border-gray-100'">
                <div class="text-[10px] uppercase font-bold tracking-wider mb-1"
                    :class="isDarkMode ? 'text-gray-400' : 'text-gray-500'">Suggested Disposition</div>
                <div class="font-medium" :class="isDarkMode ? 'text-white' : 'text-gray-900'">{{ caseOverview.suggested_disposition }}</div>
            </div>

            <!-- Metrics -->
            <div class="grid grid-cols-2 gap-3">
                <div v-if="classification.classifier_confidence || insights.confidence_score" class="p-3 rounded-lg border"
                    :class="isDarkMode ? 'bg-neutral-900 border-neutral-700' : 'bg-gray-50 border-gray-100'">
                    <div class="text-[10px] uppercase font-bold tracking-wider mb-1"
                        :class="isDarkMode ? 'text-gray-400' : 'text-gray-500'">Confidence</div>
                    <div class="font-mono text-lg font-bold" :class="isDarkMode ? 'text-gray-200' : 'text-gray-900'">
                        {{ formatPercent(classification.classifier_confidence || insights.confidence_score) }}
                    </div>
                </div>
                <div v-if="classification.priority || props.payload.priority" class="p-3 rounded-lg border"
                    :class="isDarkMode ? 'bg-neutral-900 border-neutral-700' : 'bg-gray-50 border-gray-100'">
                    <div class="text-[10px] uppercase font-bold tracking-wider mb-1"
                        :class="isDarkMode ? 'text-gray-400' : 'text-gray-500'">Priority</div>
                    <div class="font-mono text-lg font-bold" :class="isDarkMode ? 'text-gray-200' : 'text-gray-900'">
                        {{ classification.priority || props.payload.priority || 'N/A' }}
                    </div>
                </div>
            </div>

            <!-- Data Quality -->
            <div v-if="hasDataQuality" class="p-3 rounded-lg border"
                :class="isDarkMode ? 'bg-neutral-900/50 border-neutral-700' : 'bg-gray-50/50 border-gray-100'">
                <div class="flex items-center justify-between mb-2">
                    <div class="text-[10px] uppercase font-bold tracking-wider"
                        :class="isDarkMode ? 'text-gray-400' : 'text-gray-500'">Data Quality</div>
                    <span class="text-[10px] font-bold px-1.5 py-0.5 rounded"
                        :class="dataQuality.information_completeness === 'Complete'
                            ? 'bg-emerald-500/15 text-emerald-500'
                            : 'bg-amber-500/15 text-amber-500'">
                        {{ dataQuality.information_completeness }}
                    </span>
                </div>
                <div v-if="dataQuality.missing_information?.length" class="flex flex-wrap gap-1.5">
                    <span class="text-[10px]" :class="isDarkMode ? 'text-gray-500' : 'text-gray-400'">Missing:</span>
                    <span v-for="item in dataQuality.missing_information" :key="item"
                        class="text-[10px] px-1.5 py-0.5 rounded border font-medium"
                        :class="isDarkMode ? 'bg-neutral-800 border-neutral-600 text-gray-400' : 'bg-white border-gray-200 text-gray-500'">
                        {{ item }}
                    </span>
                </div>
            </div>
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

    // The full insights object (nested under payload.insights or flat in payload)
    const insights = computed(() => {
        return props.payload.insights || props.payload || {}
    })

    // Sub-sections with safe fallbacks
    const decisionPanel = computed(() => insights.value.ai_decision_panel || {})
    const caseOverview = computed(() => insights.value.case_overview || {})
    const classification = computed(() => insights.value.classification || insights.value.category_suggestions || {})
    const incidentProfile = computed(() => insights.value.vac_incident_profile || {})
    const safeguardingFlags = computed(() => insights.value.safeguarding_flags || {})
    const personsInvolved = computed(() => insights.value.persons_involved || {})
    const referralPlan = computed(() => insights.value.service_and_referral_plan || {})
    const dataQuality = computed(() => insights.value.data_quality || {})
    const entities = computed(() => insights.value.extracted_entities || {})

    // Risk level: try multiple sources
    const riskLevel = computed(() => {
        return caseOverview.value.risk_level || insights.value.risk_level || props.payload.risk_level || null
    })

    // Section visibility checks
    const hasDecisionPanel = computed(() => {
        const dp = decisionPanel.value
        return dp.recommended_next_step || dp.case_headline || dp.survivor_centred_guidance?.length
    })

    const hasIncidentProfile = computed(() => {
        const ip = incidentProfile.value
        return ip.violence_type || ip.incident_setting || ip.perpetrator_relationship
            || ip.child_in_immediate_danger || ip.incident_reported_as_ongoing
    })

    const hasPersonsInvolved = computed(() => {
        const pi = personsInvolved.value
        const hasSurvivors = pi.survivors?.some(s => s.name || s.age || s.gender)
        const hasPerps = pi.alleged_perpetrators?.some(p => p.name || p.relationship_to_survivor)
        return hasSurvivors || hasPerps
    })

    const hasReferralPlan = computed(() => {
        const rp = referralPlan.value
        return rp.immediate_referral_needed || rp.mandatory_reporting_required
            || rp.recommended_referrals?.length || rp.recommended_services?.length
            || rp.follow_up_required
    })

    const hasDataQuality = computed(() => {
        const dq = dataQuality.value
        return dq.information_completeness || dq.missing_information?.length
    })

    // Active safeguarding flags
    const FLAG_LABELS = {
        physical_violence_flag: 'Physical Violence',
        sexual_violence_flag: 'Sexual Violence',
        emotional_psychological_flag: 'Emotional/Psychological',
        neglect_flag: 'Neglect',
        exploitation_flag: 'Exploitation',
        trafficking_flag: 'Trafficking',
        harmful_practice_flag: 'Harmful Practice',
        self_harm_suicide_flag: 'Self-Harm/Suicide'
    }

    const activeFlags = computed(() => {
        const flags = safeguardingFlags.value
        return Object.entries(FLAG_LABELS)
            .filter(([key]) => flags[key] === true)
            .map(([, label]) => label)
    })

    const getFlagColor = (flag) => {
        if (flag === 'Sexual Violence' || flag === 'Self-Harm/Suicide' || flag === 'Trafficking')
            return isDarkMode.value ? 'bg-red-900/30 border-red-800 text-red-400' : 'bg-red-50 border-red-200 text-red-600'
        if (flag === 'Physical Violence')
            return isDarkMode.value ? 'bg-orange-900/30 border-orange-800 text-orange-400' : 'bg-orange-50 border-orange-200 text-orange-600'
        return isDarkMode.value ? 'bg-amber-900/30 border-amber-800 text-amber-400' : 'bg-amber-50 border-amber-200 text-amber-600'
    }

    // Flatten entity arrays — handles both strings and objects
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

    const flattenedNames = computed(() => (entities.value.names || []).map(flattenEntity).filter(Boolean))
    const flattenedLocations = computed(() => (entities.value.locations || []).map(flattenEntity).filter(Boolean))
    const flattenedOrganizations = computed(() => (entities.value.organizations || []).map(flattenEntity).filter(Boolean))

    const hasEntities = computed(() => flattenedNames.value.length || flattenedLocations.value.length || flattenedOrganizations.value.length)

    const uiMetadata = computed(() => {
        return props.prediction.raw_row?.ui_metadata || props.payload.ui_metadata || {}
    })

    const formatTime = (ts) => {
        if (!ts) return ''
        return new Date(ts * 1000).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    }

    const formatPercent = (val) => {
        if (typeof val === 'number') return (val * 100).toFixed(0) + '%'
        return val || 'N/A'
    }

    const getRiskColor = (level) => {
        const l = (level || '').toLowerCase()
        if (l === 'high' || l === 'critical') return isDarkMode.value ? 'bg-red-900/50 text-red-400' : 'bg-red-100 text-red-700'
        if (l === 'medium') return isDarkMode.value ? 'bg-amber-900/50 text-amber-400' : 'bg-amber-100 text-amber-700'
        return isDarkMode.value ? 'bg-green-900/50 text-green-400' : 'bg-green-100 text-green-700'
    }
</script>
