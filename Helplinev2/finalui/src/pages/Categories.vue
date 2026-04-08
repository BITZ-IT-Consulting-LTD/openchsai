<template>
  <div class="p-6 space-y-6">
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold" :class="isDarkMode ? 'text-white' : 'text-gray-900'">Categories</h1>
        <p class="text-sm mt-1" :class="isDarkMode ? 'text-gray-400' : 'text-gray-600'">Manage category tree structure</p>
      </div>
      <button @click="showCreateForm = true"
        class="px-4 py-2 text-sm font-semibold text-white rounded-xl transition-colors shadow-lg"
        :class="isDarkMode ? 'bg-amber-600 hover:bg-amber-700' : 'bg-amber-700 hover:bg-amber-800'">
        + Add Root Category
      </button>
    </div>

    <!-- Loading -->
    <div v-if="categoryStore.loading" class="flex justify-center py-12">
      <div class="w-8 h-8 border-3 border-amber-500 border-t-transparent rounded-full animate-spin"></div>
    </div>

    <!-- Category Tree -->
    <div v-else class="rounded-xl border overflow-hidden"
      :class="isDarkMode ? 'bg-neutral-900 border-neutral-800' : 'bg-white border-gray-100'">
      <CategoryTree :categories="categoryStore.categories" :keys="categoryStore.categories_k"
        @edit="editCategory" @add-child="addChildCategory" @toggle-active="toggleCategoryActive" />
    </div>

    <!-- Category Form Modal -->
    <CategoryForm v-if="showCreateForm || editingCategory"
      :category="editingCategory"
      :parent-name="parentName"
      :parent-id="parentId"
      @save="handleSave"
      @close="closeForm" />
  </div>
</template>

<script setup>
import { ref, inject, onMounted } from 'vue'
import { toast } from 'vue-sonner'
import { useCategoryStore } from '@/stores/categories'
import CategoryTree from '@/components/categories/CategoryTree.vue'
import CategoryForm from '@/components/categories/CategoryForm.vue'

const isDarkMode = inject('isDarkMode')
const categoryStore = useCategoryStore()

const showCreateForm = ref(false)
const editingCategory = ref(null)
const parentName = ref('')
const parentId = ref('')

onMounted(async () => {
  await categoryStore.listCategories()
})

const editCategory = (cat) => {
  editingCategory.value = cat
}

const addChildCategory = (parent) => {
  parentId.value = parent.id
  parentName.value = parent.name
  showCreateForm.value = true
}

const toggleCategoryActive = async (cat) => {
  try {
    await categoryStore.updateCategory(cat.id, { is_active: cat.is_active === '1' ? '0' : '1' })
    toast.success('Category updated')
    await categoryStore.listCategories()
  } catch (e) {
    toast.error('Failed to update category')
  }
}

const handleSave = async (data) => {
  try {
    if (editingCategory.value) {
      await categoryStore.updateCategory(editingCategory.value.id, data)
      toast.success('Category updated')
    } else {
      await categoryStore.createCategory({ ...data, parent_id: parentId.value || '' })
      toast.success('Category created')
    }
    closeForm()
    await categoryStore.listCategories()
  } catch (e) {
    toast.error('Failed to save category', { description: e.message })
  }
}

const closeForm = () => {
  showCreateForm.value = false
  editingCategory.value = null
  parentId.value = ''
  parentName.value = ''
}
</script>
