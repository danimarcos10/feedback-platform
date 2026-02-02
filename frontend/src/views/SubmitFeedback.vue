<template>
  <div class="page">
    <div class="container">
      <div class="page-header">
        <h1 class="page-title">Submit Feedback</h1>
        <p class="page-subtitle">Share your thoughts, ideas, or report issues</p>
      </div>

      <div class="submit-card card">
        <div v-if="success" class="alert alert-success">
          Feedback submitted successfully! 
          <router-link to="/dashboard">View your feedback</router-link>
        </div>

        <div v-if="error" class="alert alert-error">
          {{ error }}
        </div>

        <form @submit.prevent="submitFeedback">
          <div class="form-group">
            <label class="form-label">Title *</label>
            <input
              v-model="form.title"
              type="text"
              class="form-input"
              placeholder="Brief summary of your feedback"
              required
              maxlength="255"
            />
          </div>

          <div class="form-group">
            <label class="form-label">Description *</label>
            <textarea
              v-model="form.content"
              class="form-textarea"
              placeholder="Provide detailed information about your feedback..."
              required
              rows="6"
            ></textarea>
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
          </div>

          <div class="form-actions">
            <router-link to="/dashboard" class="btn btn-outline">
              Cancel
            </router-link>
            <button type="submit" class="btn btn-primary" :disabled="loading">
              {{ loading ? 'Submitting...' : 'Submit Feedback' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { feedbackApi, categoriesApi, tagsApi } from '../api/client'

const form = ref({
  title: '',
  content: '',
  category_id: null,
  tag_ids: []
})

const categories = ref([])
const tags = ref([])
const loading = ref(false)
const error = ref('')
const success = ref(false)

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
  error.value = ''
  success.value = false
  loading.value = true

  try {
    await feedbackApi.create(form.value)
    success.value = true
    form.value = { title: '', content: '', category_id: null, tag_ids: [] }
  } catch (err) {
    error.value = err.response?.data?.detail || 'Failed to submit feedback. Please try again.'
  } finally {
    loading.value = false
  }
}

onMounted(loadOptions)
</script>

<style scoped>
.submit-card {
  max-width: 700px;
}

.tags-select {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
}

.tag-checkbox {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
}

.tag-checkbox input {
  width: 1rem;
  height: 1rem;
}

.tag-label {
  font-size: 0.875rem;
}

.form-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  margin-top: 1.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid var(--border-color);
}
</style>
