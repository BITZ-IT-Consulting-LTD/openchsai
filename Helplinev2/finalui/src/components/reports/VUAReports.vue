<template>
  <div class="space-y-8 animate-in fade-in duration-500 pb-16">
    <!-- Header / Controls -->
    <div class="bg-white dark:bg-black border dark:border-gray-800 rounded-lg p-6 shadow-sm sticky top-0 z-10 backdrop-blur-md bg-opacity-90 dark:bg-opacity-90">
      <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h2 class="text-xl font-bold dark:text-white">VUA Quarterly Report (OCSEA Compliance)</h2>
          <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">
            Official reporting format for Voice Up Africa.
          </p>
        </div>
        
        <!-- Date Filter -->
        <div class="flex flex-col items-end gap-1">
          <div class="flex items-center gap-2">
            <select 
              v-model="timeRange" 
              class="px-3 py-2 bg-gray-50 dark:bg-gray-800 border-none rounded-lg text-sm focus:ring-2 focus:ring-amber-500"
            >
              <option value="month">This Month</option>
              <option value="prev_month">Previous Month</option>
              <option value="quarter">This Quarter</option>
              <option value="prev_quarter">Previous Quarter</option>
              <option value="year">This Year</option>
              <option value="prev_year">Previous Year</option>
              <option value="custom">Custom Range</option>
            </select>
            <button 
              @click="refreshData"
              class="p-2 text-amber-600 hover:bg-amber-50 dark:hover:bg-amber-900/20 rounded-lg transition-colors"
            >
              <i-mdi-refresh class="w-5 h-5" :class="{ 'animate-spin': loading }" />
            </button>
          </div>
          <div class="text-xs text-gray-400 font-mono">{{ dateRangeDisplay }}</div>
        </div>
      </div>
    </div>

    <!-- A. Reporting Context -->
    <div>
        <h3 class="text-lg font-semibold text-gray-800 dark:text-gray-200 mb-4 px-1">A. Reporting Context</h3>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <!-- 1. Reporting Period -->
            <div class="bg-gray-50 dark:bg-gray-900 border dark:border-gray-800 p-4 rounded-lg">
                <div class="text-xs text-gray-500 uppercase">Reporting Period</div>
                <div class="text-lg font-bold dark:text-white">{{ timeRange.replace('_', ' ').toUpperCase() }}</div>
                <div class="text-xs text-gray-400 font-mono">{{ dateRangeDisplay }}</div>
            </div>
            <!-- 2. Country/Helpline -->
            <div class="bg-gray-50 dark:bg-gray-900 border dark:border-gray-800 p-4 rounded-lg">
                <div class="text-xs text-gray-500 uppercase">Helpline</div>
                <div class="text-lg font-bold dark:text-white">National Child Helpline</div>
                <div class="text-xs text-gray-400">Tanzania (116)</div>
            </div>
            <!-- 3. System Version -->
            <div class="bg-gray-50 dark:bg-gray-900 border dark:border-gray-800 p-4 rounded-lg">
                <div class="text-xs text-gray-500 uppercase">System Version</div>
                <div class="text-lg font-bold dark:text-white">v2.5.0 (Live)</div>
                <div class="text-xs text-gray-400">OpenCHS: AI-Enhanced</div>
            </div>
            <!-- 4. Generation Date -->
            <div class="bg-gray-50 dark:bg-gray-900 border dark:border-gray-800 p-4 rounded-lg">
                <div class="text-xs text-gray-500 uppercase">Generated On</div>
                <div class="text-lg font-bold dark:text-white">{{ new Date().toLocaleDateString() }}</div>
                <div class="text-xs text-gray-400">{{ new Date().toLocaleTimeString() }}</div>
            </div>
        </div>
    </div>

    <!-- B. Contact Volume -->
    <div>
        <h3 class="text-lg font-semibold text-gray-800 dark:text-gray-200 mb-4 px-1">B. Contact Volume</h3>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <!-- 5. Total Contacts -->
            <div class="bg-white dark:bg-black border dark:border-gray-800 p-6 rounded-lg shadow-sm">
                <div class="flex justify-between items-center mb-2">
                    <span class="text-sm font-medium text-gray-500">Total Contacts</span>
                    <i-mdi-phone-in-talk class="text-blue-500" />
                </div>
                <div class="text-3xl font-bold dark:text-white">{{ totalContacts }}</div>
                <p class="text-xs text-gray-400 mt-1">All incoming, regardless of outcome</p>
            </div>
             <!-- 6. Counselling Contacts -->
            <div class="bg-white dark:bg-black border dark:border-gray-800 p-6 rounded-lg shadow-sm">
                <div class="flex justify-between items-center mb-2">
                    <span class="text-sm font-medium text-gray-500">Counselling</span>
                    <i-mdi-hand-heart class="text-green-500" />
                </div>
                <div class="text-3xl font-bold dark:text-white">{{ counsellingStats.Total }}</div>
                 <p class="text-xs text-gray-400 mt-1">Direct assistance provided</p>
            </div>
             <!-- 7. Non-Counselling Contacts -->
            <div class="bg-white dark:bg-black border dark:border-gray-800 p-6 rounded-lg shadow-sm">
                <div class="flex justify-between items-center mb-2">
                    <span class="text-sm font-medium text-gray-500">Non-Counselling</span>
                    <i-mdi-phone-hangup class="text-gray-400" />
                </div>
                <div class="text-3xl font-bold dark:text-white">{{ totalContacts - counsellingStats.Total }}</div>
                 <p class="text-xs text-gray-400 mt-1">Silent, Prank, Missed, Info</p>
            </div>
        </div>
    </div>

    <!-- C. Counselling vs Non-Counselling Breakdown -->
    <div>
        <h3 class="text-lg font-semibold text-gray-800 dark:text-gray-200 mb-4 px-1">C. Breakdown (Counselling vs Non)</h3>
         <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
             <!-- 8 & 9. Counselling Demographics -->
             <div class="bg-white dark:bg-black border dark:border-gray-800 p-6 rounded-lg shadow-sm">
                 <h4 class="font-medium text-sm text-green-600 mb-4 uppercase">Counselling Contacts Profile</h4>
                 <!-- Gender -->
                 <div class="mb-4">
                     <div class="flex justify-between text-xs mb-1">
                         <span>Boys: {{ counsellingStats.Male }}</span>
                         <span>Girls: {{ counsellingStats.Female }}</span>
                         <span>Unknown: {{ counsellingStats.Unknown }}</span>
                     </div>
                     <div class="h-2 bg-gray-100 rounded-full flex overflow-hidden">
                         <div class="bg-blue-400 h-full" :style="{ width: (counsellingStats.Male / (counsellingStats.Total||1) * 100) + '%' }"></div>
                         <div class="bg-pink-400 h-full" :style="{ width: (counsellingStats.Female / (counsellingStats.Total||1) * 100) + '%' }"></div>
                         <div class="bg-gray-300 h-full" :style="{ width: (counsellingStats.Unknown / (counsellingStats.Total||1) * 100) + '%' }"></div>
                     </div>
                 </div>
                 <!-- Age Group Placeholder -->
                 <div class="text-xs text-gray-400 italic text-center py-2 border border-dashed rounded">
                     Age Group Breakdown (Card 9) - Data Integration Pending
                 </div>
             </div>

             <!-- 10 & 11. Non-Counselling Profile -->
             <div class="bg-white dark:bg-black border dark:border-gray-800 p-6 rounded-lg shadow-sm">
                 <h4 class="font-medium text-sm text-gray-500 mb-4 uppercase">Non-Counselling Profile</h4>
                 <!-- Type Breakdown (Call Stats) -->
                 <div class="space-y-2">
                     <div v-for="(count, status) in callStats" :key="status" class="flex justify-between text-sm items-center">
                         <span class="text-gray-600 dark:text-gray-400 capitalize">{{ status.toLowerCase() }}</span>
                         <span class="font-mono font-bold">{{ count }}</span>
                     </div>
                 </div>
                 <div class="mt-4 text-xs text-gray-400 italic text-center py-2 border border-dashed rounded">
                     Gender Breakdown of Non-Counselling (Card 10) - Pending
                 </div>
             </div>
         </div>
    </div>

    <!-- D. Violence Related -->
    <div>
        <h3 class="text-lg font-semibold text-gray-800 dark:text-gray-200 mb-4 px-1">D. Violence Related</h3>
        <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
            <!-- 12. Total Violence -->
            <div class="bg-red-50 dark:bg-red-900/20 border border-red-100 dark:border-red-900/30 p-6 rounded-lg">
                <div class="text-sm font-medium text-red-600 dark:text-red-400 mb-2">Total Violence</div>
                <div class="text-3xl font-bold text-red-700 dark:text-red-500">{{ totalViolence }}</div>
            </div>
            
            <!-- 13. Gender Split -->
            <div class="bg-white dark:bg-black border dark:border-gray-800 p-6 rounded-lg">
                 <div class="text-xs text-gray-500 uppercase mb-2">By Gender</div>
                 <div class="text-center text-gray-400 italic text-sm py-4">Data Pending</div>
            </div>

            <!-- 14. Age Group -->
            <div class="bg-white dark:bg-black border dark:border-gray-800 p-6 rounded-lg">
                 <div class="text-xs text-gray-500 uppercase mb-2">By Age Group</div>
                 <div class="text-center text-gray-400 italic text-sm py-4">Data Pending</div>
            </div>

            <!-- 16. Online vs Offline -->
             <div class="bg-white dark:bg-black border dark:border-gray-800 p-6 rounded-lg">
                 <div class="text-xs text-gray-500 uppercase mb-2">Online vs Offline</div>
                 <div class="flex justify-between items-end">
                     <div>
                         <div class="text-xl font-bold dark:text-white">{{ totalOCSEA }}</div>
                         <div class="text-xs text-amber-500">Online (OCSEA)</div>
                     </div>
                     <div class="text-right">
                         <div class="text-xl font-bold dark:text-white">{{ totalViolence - totalOCSEA }}</div>
                         <div class="text-xs text-gray-500">Offline</div>
                     </div>
                 </div>
            </div>
        </div>
        
        <!-- 15. Violence Breakdown -->
        <div class="mt-6 bg-white dark:bg-black border dark:border-gray-800 p-6 rounded-lg">
             <h4 class="font-medium text-sm text-gray-500 mb-4 uppercase">15. Violence Type Breakdown</h4>
             <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
                 <div v-for="(count, type) in violenceBreakdown" :key="type" class="p-3 bg-gray-50 dark:bg-gray-900 rounded border dark:border-gray-800">
                     <div class="text-xs text-gray-500 truncate" :title="type">{{ type }}</div>
                     <div class="text-lg font-bold dark:text-white">{{ count }}</div>
                 </div>
             </div>
        </div>
    </div>

    <!-- E. OCSEA Core -->
    <div>
        <h3 class="text-lg font-semibold text-gray-800 dark:text-gray-200 mb-4 px-1">E. OCSEA Core</h3>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <!-- 17. Total OCSEA -->
            <div class="bg-amber-50 dark:bg-amber-900/20 border border-amber-100 dark:border-amber-900/30 p-6 rounded-lg">
                 <div class="text-sm font-medium text-amber-600 dark:text-amber-400 mb-2">Total OCSEA</div>
                 <div class="text-3xl font-bold text-amber-700 dark:text-amber-500">{{ totalOCSEA }}</div>
            </div>

            <!-- 18. By Gender -->
            <div class="bg-white dark:bg-black border dark:border-gray-800 p-6 rounded-lg">
                 <div class="text-xs text-gray-500 uppercase mb-2">By Gender</div>
                 <div class="flex justify-between text-sm">
                     <div class="text-center">
                         <div class="font-bold">{{ ocseaStats.Male }}</div>
                         <div class="text-xs text-blue-500">Boys</div>
                     </div>
                     <div class="text-center">
                         <div class="font-bold">{{ ocseaStats.Female }}</div>
                         <div class="text-xs text-pink-500">Girls</div>
                     </div>
                     <div class="text-center">
                         <div class="font-bold">{{ ocseaStats.Unknown }}</div>
                         <div class="text-xs text-gray-400">Unknown</div>
                     </div>
                 </div>
            </div>

             <!-- 19 & 20 Placeholders -->
             <div class="bg-white dark:bg-black border dark:border-gray-800 p-6 rounded-lg flex flex-col gap-2">
                 <div class="text-xs text-gray-400 border-b pb-2 flex justify-between">
                     <span>19. By Age Group</span>
                     <span class="italic">Pending</span>
                 </div>
                 <div class="text-xs text-gray-400 pt-1 flex justify-between">
                     <span>20. By Method</span>
                     <span class="italic">Pending</span>
                 </div>
             </div>
        </div>
    </div>

    <!-- F. OCSEA Sub-Types -->
    <div class="bg-white dark:bg-black border dark:border-gray-800 p-6 rounded-lg">
        <h3 class="font-semibold text-lg mb-4 dark:text-white">F. OCSEA Sub-Types (21-30)</h3>
        <div class="overflow-x-auto">
             <table class="w-full text-sm text-left">
                 <thead class="bg-gray-50 dark:bg-gray-900 text-xs uppercase font-bold text-gray-500">
                     <tr>
                         <th class="px-4 py-2">Sub-Type</th>
                         <th class="px-4 py-2 text-right">Count</th>
                         <th class="px-4 py-2 text-right">% of OCSEA</th>
                     </tr>
                 </thead>
                 <tbody class="divide-y dark:divide-gray-800">
                     <tr v-for="(count, type) in ocseaBreakdown" :key="type">
                         <td class="px-4 py-2">{{ type }}</td>
                         <td class="px-4 py-2 text-right font-bold">{{ count }}</td>
                         <td class="px-4 py-2 text-right text-gray-500">{{ ((count / (totalOCSEA || 1)) * 100).toFixed(1) }}%</td>
                     </tr>
                     <tr v-if="Object.keys(ocseaBreakdown).length === 0">
                         <td colspan="3" class="text-center py-4 text-gray-400 italic">No specific sub-types detected</td>
                     </tr>
                 </tbody>
             </table>
        </div>
    </div>

    <!-- G. Cyberbullying -->
    <div>
        <h3 class="text-lg font-semibold text-gray-800 dark:text-gray-200 mb-4 px-1">G. Cyberbullying</h3>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
             <div class="bg-white dark:bg-black border dark:border-gray-800 p-6 rounded-lg">
                 <div class="text-xs text-gray-500 uppercase mb-2">31. Non-Sexual Cyberbullying</div>
                 <div class="text-2xl font-bold dark:text-white">0</div>
                 <div class="text-xs text-gray-400 italic">Placeholder</div>
             </div>
             <div class="bg-white dark:bg-black border dark:border-gray-800 p-6 rounded-lg opacity-50">
                 <div class="text-xs text-gray-500 uppercase mb-2">32. By Gender</div>
                 <div class="text-sm italic">Pending</div>
             </div>
             <div class="bg-white dark:bg-black border dark:border-gray-800 p-6 rounded-lg opacity-50">
                 <div class="text-xs text-gray-500 uppercase mb-2">33. By Age Group</div>
                 <div class="text-sm italic">Pending</div>
             </div>
        </div>
    </div>

    <!-- H. Demographic Cards -->
    <div class="bg-white dark:bg-black border dark:border-gray-800 p-6 rounded-lg">
        <h3 class="font-semibold text-lg mb-4 dark:text-white">H. Demographics (34-36)</h3>
        
        <!-- 36. Matrix (Existing) -->
        <h4 class="text-xs font-bold text-gray-500 uppercase mb-3">36. Age x Gender Matrix</h4>
        <div class="overflow-x-auto">
         <table class="w-full text-sm text-left">
           <thead class="bg-gray-50 dark:bg-gray-900 text-xs uppercase font-bold text-gray-500 dark:text-gray-400">
             <tr>
               <th class="px-4 py-3 rounded-tl-lg">Age Group</th>
               <th class="px-4 py-3 text-center">Boys (M)</th>
               <th class="px-4 py-3 text-center">Girls (F)</th>
               <th class="px-4 py-3 text-center">Other/Unknown</th>
               <th class="px-4 py-3 text-right rounded-tr-lg">Total</th>
             </tr>
           </thead>
           <tbody class="divide-y dark:divide-gray-800">
             <tr v-for="age in ageGroups" :key="age" class="hover:bg-gray-50 dark:hover:bg-gray-900/50">
               <td class="px-4 py-3 font-medium dark:text-gray-200">{{ age }}</td>
               <td class="px-4 py-3 text-center text-gray-600 dark:text-gray-400">{{ getMatrixValue(age, 'Male') }}</td>
               <td class="px-4 py-3 text-center text-gray-600 dark:text-gray-400">{{ getMatrixValue(age, 'Female') }}</td>
               <td class="px-4 py-3 text-center text-gray-600 dark:text-gray-400">{{ getMatrixValue(age, 'Other') }}</td>
               <td class="px-4 py-3 text-right font-bold dark:text-white">{{ getMatrixRowTotal(age) }}</td>
             </tr>
             <tr class="bg-gray-50 dark:bg-gray-900 font-bold border-t-2 dark:border-gray-800">
               <td class="px-4 py-3">Total</td>
               <td class="px-4 py-3 text-center">{{ getMatrixColTotal('Male') }}</td>
               <td class="px-4 py-3 text-center">{{ getMatrixColTotal('Female') }}</td>
               <td class="px-4 py-3 text-center">{{ getMatrixColTotal('Other') }}</td>
               <td class="px-4 py-3 text-right text-amber-600 dark:text-amber-500">{{ totalContacts }}</td>
             </tr>
           </tbody>
         </table>
        </div>
    </div>

    <!-- I. Method of Contact -->
    <div>
        <h3 class="text-lg font-semibold text-gray-800 dark:text-gray-200 mb-4 px-1">I. Method of Contact</h3>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
             <!-- 37. All Methods -->
             <div class="bg-white dark:bg-black border dark:border-gray-800 p-6 rounded-lg">
                 <div class="text-xs text-gray-500 uppercase mb-2">37. All Contacts</div>
                 <div class="text-center text-gray-400 italic text-sm py-4">Pending</div>
             </div>
             <!-- 38. Counselling -->
             <div class="bg-white dark:bg-black border dark:border-gray-800 p-6 rounded-lg">
                 <div class="text-xs text-gray-500 uppercase mb-2">38. Counselling Only</div>
                 <div class="text-center text-gray-400 italic text-sm py-4">Pending</div>
             </div>
             <!-- 39. OCSEA -->
             <div class="bg-white dark:bg-black border dark:border-gray-800 p-6 rounded-lg">
                 <div class="text-xs text-gray-500 uppercase mb-2">39. OCSEA Sources</div>
                 <div class="text-center text-gray-400 italic text-sm py-4">Pending</div>
             </div>
        </div>
    </div>

    <!-- J, K, L, M Sections (Placeholders) -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <!-- J. Trends -->
        <div class="bg-white dark:bg-black border dark:border-gray-800 p-6 rounded-lg opacity-60">
             <h3 class="font-semibold mb-2">J. Trend & Comparisons</h3>
             <ul class="list-disc list-inside text-xs text-gray-500">
                 <li>40. QoQ Volume Change</li>
                 <li>41. QoQ OCSEA Change</li>
                 <li>42. Channel Shift</li>
             </ul>
        </div>
        <!-- K. Narrative -->
        <div class="bg-white dark:bg-black border dark:border-gray-800 p-6 rounded-lg opacity-60">
             <h3 class="font-semibold mb-2">K. Narrative & Qualitative</h3>
             <textarea class="w-full text-xs p-2 border rounded resize-none h-20 bg-gray-50" placeholder="43. Enter Quarter Summary..."></textarea>
        </div>
        <!-- L. Data Quality -->
        <div class="bg-white dark:bg-black border dark:border-gray-800 p-6 rounded-lg opacity-60">
             <h3 class="font-semibold mb-2">L. Data Quality</h3>
             <div class="grid grid-cols-2 gap-2 text-xs">
                 <div class="p-2 bg-gray-50 rounded">46. Age Missing: 0%</div>
                 <div class="p-2 bg-gray-50 rounded">47. Gender Missing: 0%</div>
             </div>
        </div>
        <!-- M. Export -->
        <div class="bg-white dark:bg-black border dark:border-gray-800 p-6 rounded-lg opacity-60">
             <h3 class="font-semibold mb-2">M. Export & Submission</h3>
             <div class="flex gap-2">
                 <button class="px-3 py-1 bg-blue-50 text-blue-600 text-xs rounded border border-blue-100">CSV</button>
                 <button class="px-3 py-1 bg-red-50 text-red-600 text-xs rounded border border-red-100">PDF</button>
             </div>
        </div>
    </div>

  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useCaseStore } from '@/stores/cases'
import { useCallStore } from '@/stores/calls'
import { VUA_MAPPING, getOCSEAType, getViolenceType } from '@/config/vua_taxonomy_map'

const store = useCaseStore()
const callStore = useCallStore()
const loading = ref(false)
const timeRange = ref('quarter')

// State
const rawData = ref([]) // Stores the flat list of cases with categories
const demographicsData = ref([])
const categorySexData = ref([])
const counsellingStats = ref({ Male: 0, Female: 0, Unknown: 0, Total: 0 })
const ocseaStats = ref({ Male: 0, Female: 0, Unknown: 0, Total: 0 })
const callStats = reactive({})
const totalCalls = ref(0)

// Metrics
const totalContacts = ref(0)
const totalViolence = ref(0)
const totalOCSEA = ref(0)
const violenceBreakdown = reactive({})
const ocseaBreakdown = reactive({})

// Demographics Helpers
const ageGroups = ['0-5', '6-9', '10-12', '13-15', '16-18', '19-24', 'Adult', 'Unknown']

const getMatrixValue = (age, gender) => {
   const match = demographicsData.value.find(r => r.ageGroup === age && r.gender === gender)
   return match ? match.count : 0
}

const getMatrixRowTotal = (age) => {
   return demographicsData.value
      .filter(r => r.ageGroup === age)
      .reduce((sum, r) => sum + r.count, 0)
}

const getMatrixColTotal = (gender) => {
   return demographicsData.value
      .filter(r => r.gender === gender)
      .reduce((sum, r) => sum + r.count, 0)
}

// Helper to get Date Objects based on selection
const getDateRange = () => {
    const now = new Date()
    let start = new Date()
    let end = new Date() // Default end is now
    
    start.setHours(0, 0, 0, 0)
    end.setHours(23, 59, 59, 999) // Ensure end captures full day
    
    if (timeRange.value === 'month') {
        start.setDate(1) // First day of current month
    } else if (timeRange.value === 'prev_month') {
        start.setMonth(start.getMonth() - 1)
        start.setDate(1)
        
        // End is last day of previous month
        end = new Date(start.getFullYear(), start.getMonth() + 1, 0)
        end.setHours(23, 59, 59, 999)
    } else if (timeRange.value === 'quarter') {
        const currentMonth = now.getMonth()
        const quarterStartMonth = Math.floor(currentMonth / 3) * 3
        start.setMonth(quarterStartMonth)
        start.setDate(1)
    } else if (timeRange.value === 'prev_quarter') {
        const currentMonth = now.getMonth()
        const currentQuarterStart = Math.floor(currentMonth / 3) * 3
        
        // Go back 3 months for start of prev quarter
        start.setMonth(currentQuarterStart - 3)
        start.setDate(1)
        
        // End is last day of prev quarter (day before current quarter start)
        end = new Date(now.getFullYear(), currentQuarterStart, 0)
        end.setHours(23, 59, 59, 999)
    } else if (timeRange.value === 'year') {
        start.setMonth(0)
        start.setDate(1)
    } else if (timeRange.value === 'prev_year') {
        start.setFullYear(start.getFullYear() - 1)
        start.setMonth(0)
        start.setDate(1)
        
        end.setFullYear(end.getFullYear() - 1)
        end.setMonth(11)
        end.setDate(31)
    } else {
        // Default to month if unknown
        start.setDate(1)
    }
    
    return { start, end }
}

const dateRangeDisplay = computed(() => {
    const { start, end } = getDateRange()
    const options = { year: 'numeric', month: 'short', day: 'numeric' }
    return `${start.toLocaleDateString(undefined, options)} - ${end.toLocaleDateString(undefined, options)}`
})

// Helper to get date range parameters for API
const getTimeRangeParams = () => {
    const { start, end } = getDateRange()
    
    // Convert to Unix timestamps (seconds)
    const startTs = Math.floor(start.getTime() / 1000)
    const endTs = Math.floor(end.getTime() / 1000)
    
    // Format: "start;end"
    return `${startTs};${endTs}`
}

// Data Fetching
const refreshData = async () => {
   loading.value = true
   
   // Reset
   totalContacts.value = 0
   totalViolence.value = 0
   totalOCSEA.value = 0
   
   // Clear reactive objects
   Object.keys(violenceBreakdown).forEach(k => delete violenceBreakdown[k])
   Object.keys(ocseaBreakdown).forEach(k => delete ocseaBreakdown[k])
   
   try {
      const dateFilter = getTimeRangeParams()

      // 1. Fetch Granular Category Data (Primary Analysis)
      // We request key fields to enable client-side mapping
      const catRes = await store.getAnalytics({ 
          xaxis: '-', 
          yaxis: 'cat_0,cat_1,cat_2,cat_3', // Fetch full category path
          metrics: 'case_count', 
          created_on: dateFilter,
          _c: 9999 
      })
      
      const rawCategories = catRes.cases || []
      
      rawCategories.forEach(row => {
          // Expected: [timestamp, cat0, cat1, cat2, cat3, count]
          // Note: The position depends on backend response structure.
          // Usually: [date, col1, col2..., count]
          const count = parseInt(row[row.length - 1] || 0)
          
          // Extract categories (assuming they follow date at index 0)
          const c0 = String(row[1] || '')
          const c1 = String(row[2] || '')
          const c2 = String(row[3] || '')
          const c3 = String(row[4] || '') // Might not exist if backend limits depth
          
          totalContacts.value += count

          // 1. Check for Violence (Broad)
          const isViolence = VUA_MAPPING.VIOLENCE_CATEGORIES.some(v => c0.includes(v))
          
          if (isViolence) {
              totalViolence.value += count
              
              // 2. Classify Violence Type
              const vType = getViolenceType(c0, c1, c2)
              if (vType) {
                  violenceBreakdown[vType] = (violenceBreakdown[vType] || 0) + count
              }
          }

          // 3. Check for OCSEA (Specific) - MOVED to dedicated fetch below
          // We now use specific IDs (385350, 385440) in Step 4 to populate OCSEA data
      })

      // 2. Fetch Demographics (Specific VUA/CHI Endpoint)
      // Using the exact parameters provided by the user to get the Age x Sex matrix
      const demoRes = await store.getAnalytics({ 
          xaxis: 'clients^contact_age_group,clients^contact_sex',
          yaxis: '-', 
          metrics: 'case_count', 
          type: 'bar',
          stacked: 'stacked',
          case_rpt_vw_t: 2,
          case_rpt_vw_tv: 2,
          created_on: dateFilter,
          _c: 9999 
      })

      const rawDemo = demoRes.cases || []
      const matrixMap = []

      rawDemo.forEach(row => {
          // Row format: ["^AgeGroup", "^Gender", "Count"] (based on user sample)
          // We strip the leading '^' if present
          let ageVal = String(row[0] || '').replace(/^\^/, '')
          let sexVal = String(row[1] || '').replace(/^\^/, '')
          const count = parseInt(row[2] || 0)
          
          if (!ageVal) ageVal = 'Unknown'
          if (!sexVal) sexVal = 'Unknown'

          // Map Sex
          let gender = 'Other'
          const s = sexVal.toLowerCase()
          if (s === 'male' || s === 'm' || s === 'boy') gender = 'Male'
          else if (s === 'female' || s === 'f' || s === 'girl') gender = 'Female'
          
          // Map Age (Normalize disparate backend buckets to VUA standards)
          let ageGroup = 'Unknown'
          
          // Check for exact ranges first
          if (ageVal.includes('Unborn') || ageVal === '0-03' || ageVal === '0-3') {
             ageGroup = '0-5'
          } else if (ageVal === '0-5' || ageVal === '0-4' || ageVal === '0-04') {
             ageGroup = '0-5'
          } else if (ageVal === '04-06') {
             ageGroup = '0-5' // Lean lower
          } else if (ageVal === '05-09' || ageVal === '06-10' || ageVal === '4-6') {
             ageGroup = '6-9'
          } else if (ageVal === '07-09' || ageVal === '07-10') {
             ageGroup = '6-9'
          } else if (ageVal === '10-12') {
             ageGroup = '10-12'
          } else if (ageVal === '11-14' || ageVal === '11-15') {
             ageGroup = '13-15' // Split decision: 11-15 spans both, mapped to older for safety or younger? 
             // Logic: 11,12 are in 10-12. 13,14,15 are in 13-15. 
             // If range is broad '11-15', it's ambiguous. Let's map to 13-15.
          } else if (ageVal === '13-15') {
             ageGroup = '13-15'
          } else if (ageVal === '15-17' || ageVal === '16-17') {
             ageGroup = '16-18'
          } else if (ageVal === '18+' || ageVal === '18-24' || ageVal === '18-25') {
             ageGroup = '19-24' // VUA typically separates 19-24 and Adult (25+)
          } else if (ageVal === '25+') {
             ageGroup = 'Adult'
          } else {
             // Numeric fallback
             const ageNum = parseInt(ageVal)
             if (!isNaN(ageNum)) {
                if (ageNum <= 5) ageGroup = '0-5'
                else if (ageNum <= 9) ageGroup = '6-9'
                else if (ageNum <= 12) ageGroup = '10-12'
                else if (ageNum <= 15) ageGroup = '13-15'
                else if (ageNum <= 18) ageGroup = '16-18'
                else if (ageNum <= 24) ageGroup = '19-24'
                else ageGroup = 'Adult'
             }
          }

          // Aggregate into matrix
          const existing = matrixMap.find(m => m.ageGroup === ageGroup && m.gender === gender)
          if (existing) {
             existing.count += count
          } else {
             matrixMap.push({ ageGroup, gender, count })
          }
      })
      demographicsData.value = matrixMap

      // 3. Fetch Category x Sex Breakdown (Counselling Contacts)
      const catSexRes = await store.getAnalytics({ 
          xaxis: 'cat_0,clients^contact_sex',
          yaxis: '-',
          metrics: 'case_count',
          type: 'bar',
          stacked: 'stacked',
          case_rpt_vw_t: 2,
          case_rpt_vw_tv: 2,
          created_on: dateFilter,
          _c: 9999
      })

      const rawCatSex = catSexRes.cases || []
      const catSexMap = []

      rawCatSex.forEach(row => {
          // Row: ["Category", "^Gender", "Count"]
          const category = String(row[0] || 'Unknown')
          let sexVal = String(row[1] || '').replace(/^\^/, '')
          const count = parseInt(row[2] || 0)

          // Normalize Sex
          let gender = 'Unknown'
          const s = sexVal.toLowerCase()
          if (s === 'male' || s === 'm' || s === 'boy') gender = 'Male'
          else if (s === 'female' || s === 'f' || s === 'girl') gender = 'Female'
          
          // Find or create category row
          let catRow = catSexMap.find(c => c.category === category)
          if (!catRow) {
              catRow = { category, Male: 0, Female: 0, Unknown: 0, Total: 0 }
              catSexMap.push(catRow)
          }

          if (gender === 'Male') catRow.Male += count
          else if (gender === 'Female') catRow.Female += count
          else catRow.Unknown += count
          
          catRow.Total += count
      })
      
      // Sort by Total Descending
      categorySexData.value = catSexMap.sort((a,b) => b.Total - a.Total)

      // Calculate Total Counselling (Everything except Information?)
      counsellingStats.value = catSexMap.reduce((acc, row) => {
          if (row.category !== 'Information') {
              acc.Male += row.Male
              acc.Female += row.Female
              acc.Unknown += row.Unknown
              acc.Total += row.Total
          }
          return acc
      }, { Male: 0, Female: 0, Unknown: 0, Total: 0 })

      // 4. Fetch Specific OCSEA Data (Source of Truth)
      // ID provided: 385440 (OCSEA Specific Root)
      // breakdown by Type (cat_1) and Gender
      const ocseaRes = await store.getAnalytics({ 
          xaxis: 'cat_1,clients^contact_sex',
          yaxis: '-',
          metrics: 'case_count',
          case_category_id: '385440',
          type: 'bar',
          stacked: 'stacked',
          case_rpt_vw_t: 2,
          case_rpt_vw_tv: 2,
          created_on: dateFilter,
          _c: 9999
      })

      const rawOcsea = ocseaRes.cases || []
      // Reset OCSEA counters
      totalOCSEA.value = 0
      Object.keys(ocseaBreakdown).forEach(k => delete ocseaBreakdown[k])
      
      // Reset Stats
      ocseaStats.value = { Male: 0, Female: 0, Unknown: 0, Total: 0 }

      rawOcsea.forEach(row => {
          // Row format: ["Cat1", "^Gender", "Count"] (based on xaxis)
          
          const cat = String(row[0] || 'Unspecified')
          let sexVal = String(row[1] || '').replace(/^\^/, '')
          const count = parseInt(row[2] || 0)

          totalOCSEA.value += count
          
          // 1. Poplate Breakdown (by Type)
          ocseaBreakdown[cat] = (ocseaBreakdown[cat] || 0) + count

          // 2. Populate Gender Stats
          let gender = 'Unknown'
          const s = sexVal.toLowerCase()
          if (s === 'male' || s === 'm') gender = 'Male'
          else if (s === 'female' || s === 'f') gender = 'Female'
          
          if (gender === 'Male') ocseaStats.value.Male += count
          else if (gender === 'Female') ocseaStats.value.Female += count
          else ocseaStats.value.Unknown += count
          
          ocseaStats.value.Total += count
      })

      // 5. Fetch Call Statistics (Hangup Status)
      const callRes = await callStore.getAnalytics({
          xaxis: 'hangup_status_txt',
          yaxis: '-',
          metrics: 'call_count',
          type: 'bar',
          stacked: 'stacked',
          rpt: 'call_count',
          chan_ts: dateFilter, // Use date filter for calls
          _c: 9999
      })

      const rawCalls = callRes.calls || []
      const callCtx = callRes.calls_ctx || []
      const callMeta = callRes.calls_k || {}
      
      // Get Total Calls from Context (Source of Truth)
      if (callCtx.length > 0 && callCtx[0] && callCtx[0][4]) {
          totalCalls.value = parseInt(callCtx[0][4])
      } else {
          totalCalls.value = 0
      }

      // Reset Stats
      Object.keys(callStats).forEach(k => delete callStats[k])
      
      // Determine if response is Raw List or Aggregated
      // If calls_k has 'hangup_status_txt', it's likely a raw list with column mapping
      let statusIdx = 0
      let countIdx = 1
      let isRaw = false

      if (callMeta && callMeta.hangup_status_txt) {
          isRaw = true
          statusIdx = parseInt(callMeta.hangup_status_txt[0])
          // count is always 1 for raw rows
      }

      let sumFromRows = 0

      rawCalls.forEach(row => {
          let status = 'Unknown'
          let count = 0

          if (isRaw) {
              status = String(row[statusIdx] || 'Unknown')
              count = 1
          } else {
              // Aggregated
              status = String(row[0] || 'Unknown')
              count = parseInt(row[1] || 0)
          }

          callStats[status] = (callStats[status] || 0) + count
          sumFromRows += count
      })
      
      // Fallback if context total was missing
      if (totalCalls.value === 0 && sumFromRows > 0) {
          totalCalls.value = sumFromRows
      }

   } catch (e) {
      console.error('VUA Reports Error:', e)
   } finally {
      loading.value = false
   }
}

onMounted(() => {
   refreshData()
})
</script>
