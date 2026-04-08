# Helpline V1 → V2 Migration Gap Analysis

Cross-reference of every V1 feature against V2 implementation status.

**Legend:** ✅ Implemented | ⚠️ Partial | ❌ Missing | 🐛 Bug

---

## 1. Authentication & Session

| V1 Feature | V2 Status | Notes |
|---|---|---|
| OTP-based login (email/SMS) | ❌ Missing | V2 uses basic username/password only |
| Password change form (current user) | ❌ Missing | No self-service password change |
| Admin password reset | ✅ | POST `api/resetAuth/{id}`, displays generated password |
| Session timeout (10hr) | ⚠️ Partial | Only 401 response triggers logout; no client-side timer |
| 401 auto-logout | ✅ | Axios interceptor redirects to /login |
| 403 handling | ✅ Fixed | Axios interceptor now handles 403 same as 401 (auto-logout) |
| Role-based route guards | ✅ | `ROLE_PERMISSIONS` matrix in auth store |
| Session logging (audit) | ⚠️ Partial | Server-side; no frontend session log display |

---

## 2. Main Layout & Navigation

| V1 Feature | V2 Status | Notes |
|---|---|---|
| App shell (sidebar + navbar + content) | ✅ | DefaultLayout with Sidebar + Navbar |
| Logo in header | ✅ | OpenCHS branding |
| Agent status in navbar | ✅ | Shows queue/call state with colored dot |
| History/notifications tabs | ✅ | Bell icon + Activities panel in Navbar |
| Dark mode | ✅ | `useTheme` composable with toggle |
| Walk-in activity button | ❌ Missing | V1 toolbar had a "Walk In" quick-action button |

---

## 3. Contact Management

| V1 Feature | V2 Status | Notes |
|---|---|---|
| Standalone contacts list page | ❌ Missing | Contacts only exist within case creation |
| Contact search/autocomplete | ⚠️ Partial | Only reporter search in case creation Step 1 |
| Contact detail popup | ❌ Missing | No standalone contact view |
| Contact filters (name, phone, age, gender, location, etc.) | ❌ Missing | No contact filter panel |
| Shared contact form (reporter/client/perpetrator base) | ✅ | Same fields used across all three entities |
| 7-level location hierarchy (Region→District→County→SubCounty→Parish→Village→Urban/Rural) | ❌ Missing | V2 uses flat TaxonomySelect tree, not cascading 7-level |
| Age ↔ DOB ↔ Age Group auto-calculation | ✅ | `useAgeCalculator` composable |
| Age group ID hardcoded (Tanzania only) | ✅ Fixed | Now uses `taxonomyStore.roots.AGE_GROUP` lookup + dynamic age bracket resolution |
| Contact fields: Name, Age, DOB, Age Group, Sex, Location, Landmark, Nationality, ID Type, ID Number, Language, Refugee status, Tribe, Phone, Alt Phone, Email | ✅ | All present in reporter/client/perpetrator forms |

---

## 4. Reporter Management

| V1 Feature | V2 Status | Notes |
|---|---|---|
| Reporter search by name/phone | ✅ | Step 1 of case creation |
| Reporter create form | ✅ | All contact fields present |
| Reporter detail popup | ❌ Missing | No standalone reporter detail view |
| Reporter compact summary card | ⚠️ Partial | Search results show pills but no full card |
| Follow-up reporter (separate from original) | ❌ Missing | V1 had `case_vw_reporter_uuid_` for follow-up caller |

---

## 5. Client Management

| V1 Feature | V2 Status | Notes |
|---|---|---|
| Client create (multi-step modal) | ✅ | 5-step ClientModal |
| Multiple clients per case | ✅ | Add/remove in Step 3 |
| Reporter's relationship with client + comment | ✅ | Step 3 of ClientModal |
| Household info (adults, type, head occupation, guardian) | ✅ | Step 4 |
| Parent/guardian marital status + ID | ✅ | Step 4 |
| Health status | ✅ | Step 5 |
| HIV status | ✅ | Step 5 |
| Marital status → conditional spouse fields | ✅ | Step 5 with conditional visibility |
| Attending school → conditional school fields | ✅ | Step 5 |
| Not attending → reason field | ✅ | Step 5 |
| Disabled → disability type → special services referral | ✅ | Step 5 |
| Client detail popup (read-only) | ❌ Missing | No read-only client detail view |
| Client delete with undo notification | ❌ Missing | No delete functionality |
| Client edit (in existing case) | ✅ Fixed | EditCaseForm now pre-populates clients, perpetrators, services, attachments from `viewCase()` |

---

## 6. Perpetrator Management

| V1 Feature | V2 Status | Notes |
|---|---|---|
| Perpetrator create (multi-step modal) | ✅ | 4-step PerpetratorModal |
| Multiple perpetrators per case | ✅ | Add/remove in Step 3 |
| Relationship with client | ✅ | Step 3 |
| Shares home with client | ✅ | Step 3 |
| Health status | ✅ | Step 4 |
| Employment/profession | ✅ | Step 4 |
| Marital status → conditional spouse fields | ✅ | Step 4 |
| Guardian name | ✅ | Step 4 |
| Additional details textarea | ✅ | Step 4 |
| Perpetrator detail popup (read-only) | ❌ Missing | No read-only perpetrator detail view |
| Perpetrator delete with notification | ❌ Missing | No delete functionality |
| Perpetrator location_id | ✅ Fixed | Now correctly maps `perpetratorForm.location` |

---

## 7. Case Management

| V1 Feature | V2 Status | Notes |
|---|---|---|
| Case list (my cases) | ✅ | View tab in Cases page, filters by `created_by` |
| Case list (escalated by me) | ✅ | View tab in Cases page, filters by `escalated_by` |
| Case list (escalated to me) | ✅ | View tab in Cases page, filters by `escalated_to` |
| Case list (all cases) | ✅ | Default view tab in Cases page |
| Case list (today's cases) | ✅ | View tab in Cases page, filters by today's date |
| Case create (wizard mode) | ✅ | 4-step wizard |
| Case create (single form / legacy) | ✅ | CaseSingleFormView |
| "Reporter is also a Client" checkbox | ✅ Fixed | Wired to auto-create client from reporter data in legacy form |
| Case category (hierarchical tree select) | ✅ | TaxonomySelect with tree navigation |
| Department toggle (116 / Dept of Labor) | ✅ | Radio buttons |
| Passport field (conditional on Dept of Labor) | ✅ | Shows when dept = labor |
| GBV Related | ✅ | Auto-set to Yes on sexual abuse category |
| Narrative textarea | ✅ | |
| Case Plan textarea | ✅ | |
| Priority (Low/Medium/High) | ✅ | |
| Status (Open/Closed/Escalated) | ✅ | Escalated (value 3) added alongside Open/Closed in forms and filters |
| Escalated To (user dropdown) | ✅ | Role-filtered user list |
| Services Offered (multi-select) | ✅ | TaxonomyOptions |
| Conditional referrals sub-form | ✅ Fixed | Present in wizard and legacy form (referrals payload uncommented + TaxonomyOptions added) |
| Police report details (conditional) | ✅ | In wizard Step 3 |
| Other services details (conditional) | ✅ | In wizard Step 3 |
| "How did you know about 116?" | ✅ | TaxonomySelect in Step 3 |
| Category-conditional: Medical Exam sub-form | ❌ Missing | V1 showed "Received Medical Exam?" for abuse categories |
| Category-conditional: Incidence Details sub-form | ❌ Missing | V1 showed when/where, HIV tested/result, PEP/ART/ECP/Counselling fields |
| Category-conditional: Justice System sub-form | ⚠️ Partial | Justice field exists but not conditionally shown by category |
| Case attachments (file upload) | ✅ | Drag-drop upload in Step 3 |
| Attachment delete | ❌ Missing | Client-side removal only; no DELETE API call |
| Case detail (read-only panel) | ✅ | CaseDetailsPanel sliding panel |
| Case update form (counsellor) | ✅ | UpdateCaseForm with plan, priority, status |
| Case edit form (supervisor full edit) | ✅ Fixed | EditCaseForm now pre-populates clients, perpetrators, services, attachments from `viewCase()` |
| Case history / audit trail | ✅ | CaseHistoryView with timeline |
| Case history field-level changes display | ❌ Missing | V1 showed "Field Name → Previous Value → New Value" per change |
| Case reports (by category, GBV, source, priority, etc.) | ✅ | Custom Explorer + CHI Reports |
| Case CSV export | ✅ | `casesStore.downloadCSV()` |

---

## 8. Call Records

| V1 Feature | V2 Status | Notes |
|---|---|---|
| Call list with pagination | ✅ | CallsTable |
| Call list columns (date, direction, phone, ext, wait, talk, hangup, QA, disposition) | ✅ | All present |
| Call detail modal | ❌ Missing | V1 had a full detail popup; V2 only has inline audio |
| Call recording playback | ✅ | Inline audio in table rows |
| Call filters - Call tab (date, direction, phone, ext, wait, talk, hangup) | ✅ | CallsFilter |
| Call filters - Case tab (Case ID) | ✅ | Collapsible "Case Filters" section in CallsFilter with Case ID field |
| Call filters - Reporter tab (name, phone, age, sex, location, etc.) | ✅ | Collapsible "Reporter Filters" section with Name, Phone, Age, Sex, Location, Nationality, Language, Tribe using TaxonomySelect |
| Call reports (count, percent, unique/repeat callers, avg times) | ⚠️ Partial | Custom Explorer has count/percent; unique/repeat callers not shown |
| Call XLSX export | ✅ | `useCallDownload` |
| QA eligibility check (no QA for zero-duration calls) | ❌ Missing | Not enforced in V2 |

---

## 9. Telephony / CTI

| V1 Feature | V2 Status | Notes |
|---|---|---|
| SIP/WebRTC phone (dial, answer, hangup) | ✅ | `useSipStore` with SIP.js |
| Call state machine (idle→ringing→active→wrapup) | ✅ | `useActiveCallStore` |
| Active call toolbar (caller info, timer, end button) | ✅ | ActiveCallToolbar |
| Incoming call popup | ✅ | IncomingCallPopup |
| Auto-answer toggle | ✅ | Navbar profile dropdown |
| Join/Leave queue | ✅ | POST `api/agent/` |
| Queue sync (AMI presence check) | ✅ | 10-second polling in activeCallStore |
| **Hold/Unhold** | ✅ | `sipStore.holdCall()`/`unholdCall()` via SIP re-INVITE + Hold button in ActiveCallToolbar |
| **Mute/Unmute** | ✅ | `sipStore.toggleMute()` via RTP track manipulation + Mute button in ActiveCallToolbar |
| **Call Transfer (blind/attended)** | ✅ | `sipStore.blindTransfer()` via SIP REFER + TransferDialog slide-in panel |
| **Conference / Add-to-call** | ❌ Missing | Not implemented |
| **DTMF keypad during call** | ✅ | Dialpad switches to in-call DTMF mode when call active, sends via `sipStore.sendDtmf()` |
| Outbound dialing | ✅ | Dialpad component |
| Agent login/logout (SIP) | ✅ | Connect/Disconnect in Dialpad |
| Ringtone on incoming call | ✅ | `/sounds/ringtone.mp3` |
| Audio device detection | ❌ Missing | V1 had `DetectDevices()` |

---

## 10. Supervisor Features

| V1 Feature | V2 Status | Notes |
|---|---|---|
| **Spy on agent call** | ✅ | SupervisorActions dropdown → POST `api/sup/` with action code 2 |
| **Whisper to agent** | ✅ | SupervisorActions dropdown → POST `api/sup/` with action code 3 |
| **Barge into call** | ✅ | SupervisorActions dropdown → POST `api/sup/` with action code 4 |
| **Force logout agent** | ✅ | SupervisorActions dropdown → POST `api/sup/` with action code 9 |
| Supervisor action dropdown on wallboard | ✅ | SupervisorActions component on each CounsellorsTable row (visible for supervisor/admin) |

---

## 11. Wallboard

| V1 Feature | V2 Status | Notes |
|---|---|---|
| Live agent status display | ✅ | CounsellorsTable with status badges |
| Live caller queue display | ✅ | CallersTable |
| Agent status (On Call/Ringing/In Queue/Available) | ✅ | Color-coded badges |
| Call duration timer | ✅ | Live timer per agent |
| Case metric tiles | ✅ | 6 KPI tiles |
| Wallboard-only mode | ❌ Missing | V1 had `te["wallonly"]` for TV display |
| AMI/ATI iframe bridge | ✅ Replaced | V2 uses WebSocket + HTTP polling (better) |

---

## 12. Non-Voice Channels (ATI)

| V1 Feature | V2 Status | Notes |
|---|---|---|
| WhatsApp session management | ✅ | Via ATI polling + Messages page |
| SMS session management | ⚠️ Partial | Listed in channel pills but behavior same as WhatsApp |
| Chat session management | ⚠️ Partial | Same |
| Facebook/Twitter/WENI sessions | ⚠️ Partial | Listed as sources |
| Sidebar session list (with unread badges) | ❌ Missing | V1 showed active sessions in left sidebar with unread counts |
| Audio notification on new message | ❌ Missing | V1 played `new_msg.ogg` |
| Chat bubble UI (message thread) | ✅ | ChatPanel with directional bubbles |
| Preset replies dropdown | ✅ | ChatPanel "Quick Replies" button with 8 preset helpline responses |
| File attachment in message reply | ✅ | MessageInput paperclip button with file input (image, PDF, doc, txt) emits `file-selected` |
| End chat / close session | ✅ | Posts `*closed*` message |
| Send message | ✅ Fixed | Removed "Service Not Available" block; messages now flow through to API |
| Real-time unread count in navbar | ⚠️ Partial | Notification bell exists but not ATI unread count |

---

## 13. Message Sessions (Historical)

| V1 Feature | V2 Status | Notes |
|---|---|---|
| Message session list | ✅ | MessagesTable |
| Session list columns (date, direction, phone, source, counts, disposition) | ⚠️ Partial | Extension shows `---`; Replies hardcoded to 0 |
| Session detail with message thread | ✅ | ChatPanel |
| Date range filter | ❌ Missing | Only channel pill filters |
| Reporter demographic filters (3-tab: message/case/reporter) | ❌ Missing | No filter panel |
| Message reports (count, percent) | ❌ Missing | No dedicated message reports |
| XLSX export | ✅ | Export button builds URL with `xlsx=1` parameter, triggers download via `window.location.href` |

---

## 14. Quality Assurance

| V1 Feature | V2 Status | Notes |
|---|---|---|
| QA form (7 tabs with prev/next navigation) | ⚠️ Partial | 6 sections in single drawer (no Feedback tab as 7th) |
| Opening/Greeting scoring (2 pts) | ✅ | 1 criterion |
| Listening scoring (10 pts) | ✅ | 5 criteria |
| Pro-activeness scoring (6 pts) | ✅ | 3 criteria |
| Resolution/Counselling scoring (10 pts) | ✅ | 5 criteria |
| Hold Procedures scoring (4 pts) | ✅ | 2 criteria |
| Closing scoring (2 pts) | ✅ | 1 criterion |
| Feedback tab (standalone comment) | ⚠️ Partial | General feedback textarea exists but not a separate tab |
| No/Partially/Yes (0/1/2) radio scoring | ✅ | Button-style selector |
| Per-section comment | ✅ | Comment field per category |
| Real-time score calculation | ✅ | `useQaForm` computed scores |
| Running total percentage | ✅ | QaScoreSidebar |
| Call recording playback in QA form | ✅ | Audio player in QaFormDrawer header |
| QA list (table with score columns) | ✅ | QasTable with 12 columns |
| QA filters (date, talk time, score ranges, supervisor) | ✅ | QAFilter |
| QA detail view (read-only completed QA) | ✅ | QADetailDrawer slide-out panel showing total score, 7 sections with per-field ratings |
| QA reports | ⚠️ Partial | Only via Custom Explorer, no dedicated QA report tab |

---

## 15. Category Management

| V1 Feature | V2 Status | Notes |
|---|---|---|
| Category tree admin page | ✅ | `/categories` route with Categories.vue page + CategoryTree.vue recursive component |
| Category CRUD (create/edit/activate/deactivate) | ✅ | CategoryForm modal with POST `api/categories/` and `api/categories/{id}` |
| Inline "Add Subcategory" form | ✅ | CategoryTree has inline add button per node, opens CategoryForm with parent pre-set |
| Category tree selector (for case forms) | ✅ | BaseSelect with lazy tree navigation |
| Flat searchable category list (for filters) | ✅ | BaseSelect search mode |
| Checkbox multi-select category list | ✅ | BaseOptions |
| Category breadcrumb trail | ✅ | BaseSelect shows navigation path |

---

## 16. User Management

| V1 Feature | V2 Status | Notes |
|---|---|---|
| User list with pagination | ✅ | UsersTable |
| User list columns (username, name, role, ext, created) | ✅ | |
| User create form | ✅ | UserForm |
| User edit form | ✅ | UserEditForm |
| User form fields (username, fname, lname, phone, email, ext, role, active) | ✅ | All present |
| User detail popup | ✅ | UserDetailsModal |
| User filters (username, fname, role, created) | ✅ | UsersFilter |
| Admin password reset | ✅ | With clipboard copy |
| User search dropdown (for selection) | ❌ Missing | No reusable user search/select widget |
| User assignment to campaigns | ❌ Missing | No member management |

---

## 17. Reports & Dashboard

| V1 Feature | V2 Status | Notes |
|---|---|---|
| Dashboard with live metrics | ✅ | 4 chart widgets |
| Call statistics dashboard | ⚠️ Partial | Basic stats in wallboard tiles; no dedicated call dashboard |
| Case reports by category | ✅ | CHI Reports + Custom Explorer |
| Case reports by demographics (reporter/client/perpetrator) | ✅ | Custom Explorer Y-axis options |
| Case reports by services/referrals | ✅ | Custom Explorer Y-axis |
| Reporter demographic reports | ⚠️ Partial | Via Custom Explorer, not standalone |
| Client demographic reports | ⚠️ Partial | Via Custom Explorer |
| Time-series reporting (hourly/daily/weekly/monthly) | ✅ | Custom Explorer X-axis periods |
| Chart types (bar, stacked bar, pie, line) | ⚠️ Partial | Bar + pie in CHI; SVG bar only in Custom Explorer; no line charts |
| Pivot tables | ✅ | Custom Explorer generates pivot table |
| Report Excel/PDF export | ✅ | PNG chart export (SVG→canvas at 2x) + CSV table export in CHI Reports and Custom Explorer |
| Custom report builder | ✅ | Custom Explorer with configurable axes |
| Website Statistics tab | ✅ | WebsiteStats with KPI cards and stacked bars |

---

## 18. Agent Availability Reports

| V1 Feature | V2 Status | Notes |
|---|---|---|
| Agent availability list (chanss) | ✅ | AgentAvailability.vue page + `useChanssStore` + ChanssTable + ChanssFilter, API: `api/chanss/` |
| Available/Occupied duration | ✅ | Columns in ChanssTable |
| Occupancy Rate % | ✅ | Column in ChanssTable |
| Availability reports | ✅ | Reports tab with pivot table via `api/chanss/rpt` |

---

## 19. Internal Calls (local)

| V1 Feature | V2 Status | Notes |
|---|---|---|
| Internal call history list | ✅ | InternalCalls.vue page + `useLocalsStore` + LocalsTable + LocalsFilter, API: `api/locals/` |
| Internal call filters | ✅ | LocalsFilter with date, direction, phone, extension, duration |
| Internal call reports | ✅ | Reports tab with pivot table via `api/local_rpt/` |
| CSV export | ✅ | Download button via `localsStore.downloadCSV()` |

---

## 20. Extension History (text/exts)

| V1 Feature | V2 Status | Notes |
|---|---|---|
| Extension-level call history | ✅ | ExtensionHistory.vue page + `useExtsStore` + ExtsTable (11 columns) + ExtsFilter, API: `api/exts/` |
| Extension reports | ✅ | Reports tab with pivot table via `api/ext_rpt/` |
| XLSX export | ✅ | Download button via `extsStore.downloadCSV()` |

---

## 21. AI Integration

| V1 Feature | V2 Status | Notes |
|---|---|---|
| Transcription display | ✅ | AiTranscriptCard |
| Translation display | ✅ | AiTranslationCard |
| Named Entity Recognition (persons, orgs, locations, dates, contacts) | ✅ | AiEntitiesCard |
| Classification (category, interventions, priority, confidence) | ✅ | AiClassificationCard |
| Risk Assessment (red flags, barriers, protective factors) | ✅ Enhanced | AiInsightsCard with safeguarding flags |
| Case Summary | ✅ | AiSummaryCard |
| Case Management recommendations (safety, psychosocial, legal, medical) | ✅ Enhanced | AiInsightsCard with decision panel |
| Cultural Considerations | ⚠️ Partial | Not a separate section in V2 |
| Real-time AI sidebar updates during call | ✅ | ATI→DefaultLayout→activeCallStore pipeline |
| AI processing step indicator | ❌ Missing | V1 showed which step AI was on |
| AI feedback widget | ✅ New | AiFeedbackWidget (not in V1) |
| VAC Incident Profile | ✅ New | Violence type, setting, danger flags (not in V1) |
| Service & Referral Plan | ✅ New | Immediate referral, mandatory reporting (not in V1) |

---

## 22. Schedule Management

| V1 Feature | V2 Status | Notes |
|---|---|---|
| Schedule list | ❌ Missing | No page, store, or route |
| Schedule create/edit form | ❌ Missing | |
| Date range + time range + day of week | ❌ Missing | |
| Resource type routing (inbound/outbound/voiceblast/user) | ❌ Missing | |

---

## 23. Campaign / Member Management

| V1 Feature | V2 Status | Notes |
|---|---|---|
| Campaign member list | ❌ Missing | No page, store, or route |
| Add/remove agents from campaign | ❌ Missing | |
| Member role display | ❌ Missing | |

---

## 24. Voice File / Recording Management

| V1 Feature | V2 Status | Notes |
|---|---|---|
| Voice file playback widget | ⚠️ Partial | Inline audio in calls table; no standalone widget |
| Voice file upload (IVR prompts) | ❌ Missing | |
| Voice file reorder (IVR menu sequence) | ❌ Missing | |
| MOH (Music on Hold) management | ❌ Missing | |
| Recording not found fallback | ❌ Missing | |

---

## 25. Disposition Management

| V1 Feature | V2 Status | Notes |
|---|---|---|
| Disposition tracking on calls | ⚠️ Partial | Column shown in calls table |
| Disposition form during call wrapup | ✅ Fixed | DispositionDrawer now POSTs to `api/dispositions/` with callId, selected disposition, and notes |
| Disposition context injection (case + reporter data) | ❌ Missing | V1's `disposition_k` template injected full context |

---

## 26. Miscellaneous

| V1 Feature | V2 Status | Notes |
|---|---|---|
| My Profile popup (availability stats, history chart) | ❌ Missing | |
| Activities page (full activity log) | ✅ | Route exists, store exists |
| FAQs page | ✅ | Route exists |
| Notifications with polling | ✅ | 60-second polling, mark read, pagination |
| Global search | ✅ | Navbar search synced to page filters |

---

## 27. Known Bugs in V2

| Bug | Location | Status |
|---|---|---|
| ~~Perpetrator `location_id` maps sex value~~ | `CaseCreate.vue:729` | ✅ Fixed — now maps `perpetratorForm.location` |
| ~~Referrals missing in legacy case form~~ | `CaseSingleFormView.vue` | ✅ Fixed — referrals payload uncommented + TaxonomyOptions added |
| ~~Edit case: clients/perpetrators/services not pre-populated~~ | `EditCaseForm.vue` | ✅ Fixed — pre-populates from `viewCase()` response |
| ~~"Reporter is Client" not wired to auto-fill~~ | `CaseSingleFormView.vue` | ✅ Fixed — auto-creates client from reporter data |
| ~~MessageInput shows "Service Not Available"~~ | `MessageInput.vue` | ✅ Fixed — removed blocking toast, messages flow to API |
| ~~DispositionDrawer doesn't save to API~~ | `DispositionDrawer.vue` | ✅ Fixed — POSTs to `api/dispositions/` |
| ~~Hardcoded age group IDs (TZ only)~~ | `useAgeCalculator.js` | ✅ Fixed — uses `taxonomyStore.roots.AGE_GROUP` dynamic lookup |
| ~~`BaseSelect` undefined `parentIdx` in search~~ | `BaseSelect.vue` | ✅ Fixed |
| ~~Duplicate `searchSubcategories` in categories store~~ | `stores/categories.js` | ✅ Fixed — removed duplicate definition |
| ~~Sidebar logout doesn't clean up SIP/queue~~ | `Sidebar.vue` | ✅ Fixed — calls `sipStore.stop()` + `activeCallStore.resetQueueState()` |
| ~~Dual WebSocket implementations~~ | `useWebSocketConnection` | ✅ Fixed — dead code removed |
| ~~Dead code: `useWebRtcClient.js`~~ | `composables/useWebRtcClient.js` | ✅ Fixed — file deleted, imports removed |

---

## Summary: Critical Gaps for Production Parity

### Must-Have — ✅ ALL RESOLVED

1. ~~**Hold/Unhold**~~ — ✅ Implemented (sipStore + ActiveCallToolbar button)
2. ~~**Call Transfer**~~ — ✅ Implemented (blind transfer via SIP REFER + TransferDialog)
3. ~~**Supervisor actions**~~ — ✅ Implemented (Spy/Whisper/Barge/Force Logout dropdown on wallboard)
4. ~~**Disposition save**~~ — ✅ Fixed (POSTs to `api/dispositions/`)
5. ~~**Message send**~~ — ✅ Fixed (removed blocking toast)
6. ~~**Category admin page**~~ — ✅ Implemented (tree view + CRUD)
7. ~~**"Reporter is Client" auto-fill**~~ — ✅ Fixed (auto-creates client from reporter)
8. ~~**Case edit pre-population**~~ — ✅ Fixed (loads from `viewCase()`)
9. ~~**Perpetrator location_id bug**~~ — ✅ Fixed (maps correct field)
10. ~~**Referrals in legacy form**~~ — ✅ Fixed (payload uncommented)

### Should-Have — Mostly Resolved

| # | Item | Status |
|---|------|--------|
| 11 | Agent availability reports (chanss) | ✅ Implemented |
| 12 | Internal call history (local) | ✅ Implemented |
| 13 | Extension history (text/exts) | ✅ Implemented |
| 14 | Call detail modal | ❌ Still missing |
| 15 | QA read-only view | ✅ Implemented (QADetailDrawer) |
| 16 | 7-level location hierarchy | ❌ Still missing |
| 17 | Contact standalone page | ❌ Still missing |
| 18 | Case list views (my cases, escalated to/by me, today's) | ✅ Implemented (5 view tabs) |
| 19 | Preset message replies | ✅ Implemented (8 presets in ChatPanel) |
| 20 | Call filter tabs (case + reporter demographics) | ✅ Implemented (collapsible sections) |
| 21 | Message date range filter + XLSX export | ⚠️ XLSX export done; date range filter still missing |
| 22 | OTP authentication | ❌ Still missing |
| 23 | Password change form | ❌ Still missing |
| 24 | Mute/DTMF during call | ✅ Implemented |
| 25 | Audio notification on new message | ❌ Still missing |
| 26 | ATI sidebar with unread counts | ❌ Still missing |
| 27 | Schedule + Campaign management | ❌ Still missing |
| 28 | Report export (Excel/PDF) | ✅ Implemented (PNG chart + CSV table) |
| 29 | Case status: Escalated option | ✅ Implemented |
| 30 | Category-conditional sub-forms | ❌ Still missing |

### Nice-to-Have

31. Wallboard-only mode (TV display) — ❌
32. Conference/add-to-call — ❌
33. Voice file/IVR prompt management — ❌
34. MOH management — ❌
35. Audio device detection — ❌
36. My Profile availability stats — ❌
37. Walk-in quick action button — ❌
38. Follow-up reporter tracking — ❌
39. Client/perpetrator delete with undo — ❌
40. AI processing step indicator — ❌

---

## Sprint Progress (March 2026)

**Resolved:** 12 bugs fixed, 25 features implemented
**Remaining gaps:** 10 should-have items + 10 nice-to-have items
**Build status:** Clean (zero compilation errors)
**Browser validation:** All pages tested, zero console errors on core pages
