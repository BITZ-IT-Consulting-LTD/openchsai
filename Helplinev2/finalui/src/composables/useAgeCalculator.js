
import { useTaxonomyStore } from '@/stores/taxonomy'

export function useAgeCalculator() {
    // Resolve age group IDs dynamically from taxonomy store
    function getAgeGroupOptions() {
        const taxonomyStore = useTaxonomyStore()
        const rootId = taxonomyStore.roots?.AGE_GROUP
        if (!rootId) {
            // Fallback to hardcoded DEMO IDs if taxonomy not loaded
            return {
                '0-5': '361950',
                '6-12': '361951',
                '13-17': '361952',
                '18-24': '361953',
                '25-35': '361954',
                '36-50': '361955',
                '51+': '361956'
            }
        }

        const cached = taxonomyStore.categoriesCache[rootId]
        if (cached && cached.items && cached.keys) {
            const k = cached.keys
            const idIdx = Number(k.id?.[0] ?? 0)
            const nameIdx = Number(k.name?.[0] ?? 5)
            const map = {}
            cached.items.forEach(item => {
                const name = item[nameIdx]
                const id = String(item[idIdx])
                if (name && id) map[name] = id
            })
            if (Object.keys(map).length > 0) return map
        }

        // Fallback
        return {
            '0-5': '361950',
            '6-12': '361951',
            '13-17': '361952',
            '18-24': '361953',
            '25-35': '361954',
            '36-50': '361955',
            '51+': '361956'
        }
    }

    const AGE_BRACKETS = [
        { min: 0, max: 5, label: '0-5' },
        { min: 6, max: 12, label: '6-12' },
        { min: 13, max: 17, label: '13-17' },
        { min: 18, max: 24, label: '18-24' },
        { min: 25, max: 35, label: '25-35' },
        { min: 36, max: 50, label: '36-50' },
        { min: 51, max: Infinity, label: '51+' }
    ]

    const getAgeGroupFromAge = (age) => {
        if (!age && age !== 0) return '';
        const a = parseInt(age);
        if (isNaN(a) || a < 0) return '';

        const bracket = AGE_BRACKETS.find(b => a >= b.min && a <= b.max)
        return bracket ? bracket.label : ''
    };

    const getAgeGroupId = (age) => {
        const text = getAgeGroupFromAge(age);
        if (!text) return ''
        const map = getAgeGroupOptions()
        return map[text] || '';
    };

    const calculateAgeFromDob = (dob) => {
        if (!dob) return '';
        const birthDate = new Date(dob);
        const today = new Date();
        let age = today.getFullYear() - birthDate.getFullYear();
        const monthDiff = today.getMonth() - birthDate.getMonth();
        if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birthDate.getDate())) {
            age--;
        }
        return age >= 0 ? age.toString() : '';
    };

    const calculateDobFromAge = (age) => {
        if (!age && age !== 0) return '';
        const a = parseInt(age);
        if (isNaN(a) || a < 0) return '';

        const today = new Date();
        const birthYear = today.getFullYear() - a;
        return `${birthYear}-01-01`;
    };

    return {
        getAgeGroupId,
        getAgeGroupFromAge,
        calculateAgeFromDob,
        calculateDobFromAge
    };
}
