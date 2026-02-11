# CHI to VUA Quarterly Report Alignment - Analysis & Mapping

## 1. Existing CHI Reporting Analysis

The existing `CHIReports.vue` implementation focuses on high-level operational metrics compliant with basic CHI standards.

### Current Indicators Reported
| Dimension | Source Field | Granularity | Notes |
|-----------|--------------|-------------|-------|
| **Demographics** | `age`, `sex` | Age Groups (0-5, 6-9, ...), Gender (Male, Female, Other) | 2D Matrix (Age x Sex) available. |
| **Contact Method** | `src` | Phone, SMS, Web, etc. | Top-level methods only. |
| **Main Issues** | `cat_0` | Level 1 Categories (e.g., Abuse, Family, School) | **GAP**: No sub-category breakdown in standard report. |
| **Actions Taken** | `disposition` | Action/Referral lists | Flat list of actions. |
| **Total Contacts** | `case_count` | Raw count of case records | - |

### CHI Definitions (inferred from system)
*   **Counseling Contacts**: Currently not explicitly separated from "Non-counselling" in the UI, but derived from Case Assessment/Disposition.
*   **Violence Contacts**: Cases where `cat_0` falls under "Abuse" or "Violence".
*   **OCSEA**: Currently hidden within `cat_0` (Sexual Abuse) or deeper levels (`cat_1`, `cat_2`). Standard report does **not** break this down.

---

## 2. VUA Quarterly Report Requirements (vs. Existing)

VUA Quarterly Reports typically require specific deep-dives into Violence and OCSEA.

| VUA Requirement | Standard CHI Output | Match Status | Transformation Needed |
|-----------------|---------------------|--------------|-----------------------|
| **Total Contacts** | Total Contacts | ✅ Match | None |
| **Demographics** | Age/Sex Matrix | ✅ Match | None |
| **Violence vs. Non-Violence** | N/A (Mixed in Categories) | ⚠️ Partial | **Aggregation**: Group `cat_0` into 'Violence' (Abuse) vs 'Non-Violence' (Information, School, etc.). |
| **Type of Violence** | Standard Categories | ⚠️ Partial | **Mapping**: Ensure `cat_0` labels align with VUA terms (Physical, Emotional, Sexual, Neglect). |
| **OCSEA Breakdown** | **MISSING** | ❌ Gap | **Drill-down**: Must fetch `cat_1`, `cat_2`, `cat_3` to identify specific OCSEA types (Grooming, Sexting, etc.). |
| **Online vs Offline** | **MISSING** | ❌ Gap | **Classification**: Needs logic to distinguish Online Sexual Abuse (OCSEA) from Contact Sexual Abuse based on sub-categories. |

---

## 3. OCSEA-Specific Compliance Check

**Current State:**
*   `cat_0` likely contains "Sexual Abuse".
*   `cat_1` likely contains "Online" vs "Contact".
*   `taxonomyContract.js` identifies `SEXUAL_ABUSE` trigger ID `362271`.

**Gap:**
*   The raw counts in `CHIReports.vue` (`cat_0`) clump all Sexual Abuse together.
*   VUA requires distinct counts for:
    *   Online Grooming
    *   Sexting / Image-based abuse
    *   CSAM (Production/Distribution)
    *   Cyberbullying (often separate from Sexual Abuse)

**Strategy:**
*   Implement a "Recursive Category Search" in the VUA Report generator.
*   Define a **Taxonomy Map** that explicitly links granular `cat_N` IDs to VUA Output Lines.

---

## 4. Proposed Transformations & Mapping

### Data Source
We will use the generic `getAnalytics` endpoint but request `yaxis=cat_0,cat_1,cat_2,cat_3` to get the full path for every case (or at least aggregates grouped by the full path).
*   *Optimization:* Fetching `yaxis=cat_0,cat_1,cat_2` might be heavy. Alternatively, use specific category filters if the API supports it.
*   *Selected Approach:* Fetch grouped analytics by `cat_0,cat_1,cat_2` and perform client-side mapping for the report table.

### Logic Rule: `isOCSEA(case)`
```javascript
function getOCSEAType(c0, c1, c2, c3) {
    // Example Logic - To be calibrated with actual Taxonomy IDs
    if (c0 === 'Abuse' && c1 === 'Sexual' && c2.includes('Online')) return 'General OCSEA';
    if (c2.includes('Grooming')) return 'Grooming';
    if (c2.includes('Image') || c3.includes('Sexting')) return 'Sexting';
    return null; // Not OCSEA
}
```

---

## 5. VUA Reporting Schema (JSON)

We will define a configuration object that drives the VUA report.

```json
{
  "sections": [
    {
      "id": "violence_summary",
      "title": "Violence vs Non-Violence",
      "indicators": [
        { "label": "Violence Related", "filter": { "cat_0": ["Abuse", "Violence", "Exploitation"] } },
        { "label": "Non-Violence", "filter": { "exclude_cat_0": ["Abuse", "Violence", "Exploitation"] } }
      ]
    },
    {
      "id": "ocsea_detail",
      "title": "Online Child Sexual Exploitation & Abuse (OCSEA)",
      "indicators": [
        { "label": "Online Grooming", "filter": { "cat_matches": ["Grooming", "Solicitation"] } },
        { "label": "Non-Consensual Image Sharing (Sexting)", "filter": { "cat_matches": ["Image", "Sexting"] } },
        { "label": "CSAM Production/Dist.", "filter": { "cat_matches": ["CSAM", "Pornography"] } }
      ]
    }
  ]
}
```

## 6. Implementation Plan

1.  **Create `VUAReports.vue`**: A new component similar to `CHIReports.vue` but with the advanced fetching logic.
2.  **Taxonomy Mapping Config**: A dedicated file `src/config/vua_taxonomy_map.js` to separate logic from UI.
3.  **Update `Reports.vue`**: Add the new tab.

