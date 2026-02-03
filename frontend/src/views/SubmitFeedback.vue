<template>
  <div class="page">
    <div class="container">
      <div class="page-header">
        <router-link to="/dashboard" class="back-link">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="20" height="20">
            <line x1="19" y1="12" x2="5" y2="12"/><polyline points="12 19 5 12 12 5"/>
          </svg>
          Back to Dashboard
        </router-link>
        <h1 class="page-title">Submit Feedback</h1>
        <p class="page-subtitle">Share your thoughts, ideas, or report issues with our team</p>
      </div>

      <div class="submit-card card">
        <div class="form-header">
          <div class="form-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
              <line x1="9" y1="10" x2="15" y2="10"/>
              <line x1="9" y1="14" x2="12" y2="14"/>
            </svg>
          </div>
          <h2 class="form-title">New Feedback</h2>
        </div>
        <form @submit.prevent="submitFeedback">
          <div class="form-group">
            <label class="form-label">Title *</label>
            <input
              v-model="form.title"
              type="text"
              :class="['form-input', { 'is-invalid': errors.title }]"
              placeholder="Brief summary of your feedback"
              maxlength="255"
              @blur="validateTitle"
            />
            <span v-if="errors.title" class="form-error">{{ errors.title }}</span>
          </div>

          <div class="form-group">
            <label class="form-label">Description *</label>
            <textarea
              v-model="form.content"
              :class="['form-textarea', { 'is-invalid': errors.content }]"
              placeholder="Provide detailed information about your feedback..."
              rows="6"
              @blur="validateContent"
            ></textarea>
            <span v-if="errors.content" class="form-error">{{ errors.content }}</span>
            <span v-else class="form-hint">{{ form.content.length }}/10 minimum characters</span>
          </div>

          <div class="form-group">
            <label class="form-label">Category (Optional)</label>
            <select v-model="form.category_id" class="form-select">
              <option :value="null">Select a category</option>
              <option v-for="cat in categories" :key="cat.id" :value="cat.id">
                {{ cat.name }}
              </option>
            </select>
          </div>

          <div class="form-group">
            <label class="form-label">Tags (Optional)</label>
            <div class="tags-select">
              <label v-for="tag in tags" :key="tag.id" class="tag-checkbox">
                <input
                  type="checkbox"
                  :value="tag.id"
                  v-model="form.tag_ids"
                />
                <span class="tag-label">{{ tag.name }}</span>
              </label>
            </div>
            <p v-if="tags.length === 0" class="form-hint">No tags available yet.</p>
          </div>

          <div class="form-actions">
            <router-link to="/dashboard" class="btn btn-outline">
              Cancel
            </router-link>
            <button type="submit" class="btn btn-primary" :disabled="loading || !isValid">
              {{ loading ? 'Submitting...' : 'Submit Feedback' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { feedbackApi, categoriesApi, tagsApi } from '../api/client'
import { useToast } from '../stores/toast'

const router = useRouter()
const toast = useToast()

const form = ref({
  title: '',
  content: '',
  category_id: null,
  tag_ids: []
})

const errors = ref({
  title: '',
  content: ''
})

const categories = ref([])
const tags = ref([])
const loading = ref(false)

const isValid = computed(() => {
  return form.value.title.trim().length >= 3 && 
         form.value.content.trim().length >= 10 &&
         !errors.value.title &&
         !errors.value.content
})

function validateTitle() {
  if (!form.value.title.trim()) {
    errors.value.title = 'Title is required'
  } else if (form.value.title.trim().length < 3) {
    errors.value.title = 'Title must be at least 3 characters'
  } else {
    errors.value.title = ''
  }
}

function validateContent() {
  if (!form.value.content.trim()) {
    errors.value.content = 'Description is required'
  } else if (form.value.content.trim().length < 10) {
    errors.value.content = 'Description must be at least 10 characters'
  } else {
    errors.value.content = ''
  }
}

async function loadOptions() {
  try {
    const [catResponse, tagResponse] = await Promise.all([
      categoriesApi.list(),
      tagsApi.list()
    ])
    categories.value = catResponse.data
    tags.value = tagResponse.data
  } catch (err) {
    console.error('Failed to load options:', err)
  }
}

async function submitFeedback() {
  // Validate all fields
  validateTitle()
  validateContent()
  
  if (!isValid.value) {
    toast.error('Please fix the validation errors')
    return
  }
  
  loading.value = true

  try {
    await feedbackApi.create(form.value)
    toast.success('Feedback submitted successfully!')
    form.value = { title: '', content: '', category_id: null, tag_ids: [] }
    errors.value = { title: '', content: '' }
    // Navigate to dashboard after short delay
    setTimeout(() => {
      router.push('/dashboard')
    }, 1500)
  } catch (err) {
    toast.error(err.response?.data?.detail || 'Failed to submit feedback. Please try again.')
  } finally {
    loading.value = false
  }
}

onMounted(loadOptions)
</script>

<style scoped>
.back-link {
  display: inline-flex;
  align-items: center;
  gap: 0.375rem;
  color: var(--gray-500);
  text-decoration: none;
  font-size: 0.875rem;
  font-weight: 500;
  margin-bottom: 0.75rem;
  transition: color 0.2s;
}

.back-link:hover {
  color: var(--primary-500);
}

.submit-card {
  max-width: 700px;
  border-radius: 20px;
  padding: 2rem;
}

.form-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 2rem;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid var(--gray-100);
}

.form-icon {
  width: 56px;
  height: 56px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  box-shadow: 0 4px 14px rgba(102, 126, 234, 0.3);
}

.form-icon svg {
  width: 28px;
  height: 28px;
}

.form-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--gray-900);
}

.tags-select {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.tag-checkbox {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 0.875rem;
  background: var(--gray-50);
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
  border: 2px solid transparent;
}

.tag-checkbox:hover {
  background: var(--gray-100);
}

.tag-checkbox:has(input:checked) {
  background: var(--primary-50);
  border-color: var(--primary-200);
}

.tag-checkbox input {
  accent-color: var(--primary-500);
}

.tag-label {
  font-size: 0.8125rem;
  font-weight: 500;
  color: var(--gray-700);
}

.form-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  margin-top: 2rem;
  padding-top: 1.5rem;
  border-top: 1px solid var(--gray-100);
}

.form-hint {
  color: var(--gray-500);
  font-size: 0.8125rem;
  margin-top: 0.375rem;
}
</style>
