/**
 * VUA Monthly/Quarterly Reporting Taxonomy Map
 * 
 * This file maps the internal CHI categories (Level 0, 1, 2) to the
 * standard Voice Up Africa (VUA) reporting indicators.
 * 
 * Rules:
 * - Arrays are treated as OR conditions.
 * - String matching is case-insensitive.
 * - 'match' can be 'exact' or 'contains'.
 */

export const VUA_MAPPING = {
    // 1. Broad Classification (Violence vs Non-Violence)
    // Matches against `cat_0` (Main Category)
    VIOLENCE_CATEGORIES: [
        'Abuse',
        'Violence',
        'Exploitation',
        'Neglect',
        'Harmful Practices',
        'Trafficking'
    ],

    // 2. Violence Types (Sub-classification of Violence)
    // Matches against `cat_1` or `cat_2`
    VIOLENCE_TYPES: {
        'Physical Violence': ['Physical', 'Beating', 'Corporal Punishment'],
        'Emotional Violence': ['Emotional', 'Psychological', 'Verbal Abuse'],
        'Sexual Violence': ['Sexual', 'Rape', 'Defilement', 'Sodomy'], // General SV
        'Neglect': ['Neglect', 'Abandonment', 'Denial of Resources'],
        'Exploitation': ['Exploitation', 'Child Labor', 'Trafficking'],
        'Harmful/Cultural': ['FGM', 'Child Marriage', 'Initiation']
    },

    // 3. OCSEA (Online Child Sexual Exploitation & Abuse)
    // These are specific indicators that might appear in `cat_1` or `cat_2`
    // Priority: If a case matches OCSEA, it falls here regardless of other types.
    OCSEA_INDICATORS: {
        'Online Grooming': ['Grooming', 'Solicitation', 'Luring'],
        'Sexting / Non-Consensual Images': ['Sexting', 'Image-based', 'Nudes', 'Self-generated'],
        'Cyberbullying': ['Cyberbullying', 'Online Harassment', 'Trolling'],
        'CSAM (Production/Distribution)': ['CSAM', 'Pornography', 'Material'],
        'Extortion / Blackmail': ['Extortion', 'Blackmail', 'Sextortion'],
        'Online Privacy Violation': ['Privacy', 'Doxing', 'Hacking']
    }
};

/**
 * Helper to determine if a case is OCSEA based on its category path.
 * @param {string} c0 - Main Category
 * @param {string} c1 - Sub Category 1
 * @param {string} c2 - Sub Category 2
 * @returns {string|null} - The OCSEA type label or null
 */
export const getOCSEAType = (c0, c1, c2) => {
    const fullPath = `${c0} ${c1} ${c2}`.toLowerCase();

    // Check OCSEA indicators first (most specific)
    for (const [label, keywords] of Object.entries(VUA_MAPPING.OCSEA_INDICATORS)) {
        if (keywords.some(k => fullPath.includes(k.toLowerCase()))) {
            return label;
        }
    }

    // General check for "Online" in Sexual Violence context
    if (fullPath.includes('sexual') && fullPath.includes('online')) {
        return 'General OCSEA';
    }

    return null;
};

/**
 * Helper to determine general Violence Type
 */
export const getViolenceType = (c0, c1, c2) => {
    const fullPath = `${c0} ${c1} ${c2}`.toLowerCase();

    for (const [label, keywords] of Object.entries(VUA_MAPPING.VIOLENCE_TYPES)) {
        if (keywords.some(k => fullPath.includes(k.toLowerCase()))) {
            return label;
        }
    }
    return 'Other/Unspecified Violence';
};
