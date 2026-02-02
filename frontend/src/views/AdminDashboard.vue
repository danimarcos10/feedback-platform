<template>
  <div class="page">
    <div class="container">
      <div class="page-header">
        <h1 class="page-title">Admin Dashboard</h1>
        <p class="page-subtitle">Manage all feedback submissions</p>
      </div>

      <!-- Quick Stats -->
      <div class="grid grid-4 mb-6">
        <div class="stat-card card">
          <div class="stat-value">{{ stats.total_feedback || 0 }}</div>
          <div class="stat-label">Total Feedback</div>
        </div>
        <div class="stat-card card">
          <div class="stat-value">{{ stats.open_feedback || 0 }}</div>
          <div class="stat-label">Open</div>
        </div>
        <div class="stat-card card">
          <div class="stat-value">{{ stats.resolved_feedback || 0 }}</div>
          <div class="stat-label">Resolved</div>
        </div>
        <div class="stat-card card">
          <div class="stat-value">{{ formatHours(stats.average_resolution_time_hours) }}</div>
          <div class="stat-label">Avg Resolution Time</div>
        </div>
      </div>

      <!-- Filters -->
      <div class="filters card mb-6">
        <div class="flex gap-4 items-center">
          <div class="form-group" style="margin-bottom: 0; flex: 1;">
            <label class="form-label">Status</label>
            <select v-model="statusFilter" class="form-select" @change="loadFeedback">
              <option value="">All Status</option>
              <option value="new">New</option>
              <option value="triaged">Triaged</option>
              <option value="in_progress">In Progress</option>
              <option value="resolved">Resolved</option>
              <option value="rejected">Rejected</option>
            </select>
          </div>
          <div class="form-group" style="margin-bottom: 0; flex: 1;">
            <label class="form-label">Category</label>
            <select v-model="categoryFilter" class="form-select" @change="loadFeedback">
              <option value="">All Categories</option>
              <option v-for="cat in categories" :key="cat.id" :value="cat.id">
                {{ cat.name }}
              </option>
            </select>
          </div>
        </div>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="loading-container">
        <div class="spinner"></div>
      </div>

      <!-- Feedback Table -->
      <div v-else-if="feedback.length > 0" class="card">
        <table class="table">
          <thead>
            <tr>
              <th>Title</th>
              <th>Status</th>
              <th>Category</th>
              <th>Sentiment</th>
              <th>Created</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in feedback" :key="item.id">
              <td>
                <strong>{{ item.title }}</strong>
                <div class="text-secondary" style="font-size: 0.75rem;">
                  {{ item.content.substring(0, 80) }}{{ item.content.length > 80 ? '...' : '' }}
                </div>
              </td>
              <td>
                <span :class="['badge', `badge-${item.status}`]">
                  {{ formatStatus(item.status) }}
                </span>
              </td>
              <td>{{ item.category?.name || '-' }}</td>
              <td>
                <span :class="getSentimentClass(item.sentiment_score)">
                  {{ formatSentiment(item.sentiment_score) }}
                </span>
              </td>
              <td>{{ formatDate(item.created_at) }}</td>
              <td>
                <button class="btn btn-outline btn-sm" @click="openDetailModal(item)">
                  Manage
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Empty State -->
      <div v-else class="card text-center" style="padding: 3rem;">
        <h3>No feedback found</h3>
        <p class="text-secondary mt-2">No feedback matches your filters.</p>
      </div>

      <!-- Pagination -->
      <div v-if="totalPages > 1" class="pagination mt-6">
        <button class="btn btn-outline" :disabled="page === 1" @click="page--; loadFeedback()">
          Previous
        </button>
        <span class="page-info">Page {{ page }} of {{ totalPages }}</span>
        <button class="btn btn-outline" :disabled="page >= totalPages" @click="page++; loadFeedback()">
          Next
        </button>
      </div>

      <!-- Detail Modal -->
      <div v-if="selectedFeedback" class="modal-overlay" @click.self="selectedFeedback = null">
        <div class="modal card modal-lg">
          <div class="modal-header">
            <h2>{{ selectedFeedback.title }}</h2>
            <button class="btn-close" @click="selectedFeedback = null">&times;</button>
          </div>
          
          <div class="modal-body">
            <div class="detail-section">
              <h4>Content</h4>
              <p>{{ selectedFeedback.content }}</p>
            </div>

            <div class="detail-section">
              <h4>Update Status</h4>
              <select v-model="updateForm.status" class="form-select" @change="updateStatus">
                <option value="new">New</option>
                <option value="triaged">Triaged</option>
                <option value="in_progress">In Progress</option>
                <option value="resolved">Resolved</option>
                <option value="rejected">Rejected</option>
              </select>
            </div>

            <div class="detail-section">
              <h4>Assign Category</h4>
              <select v-model="updateForm.category_id" class="form-select" @change="updateCategory">
                <option :value="null">No Category</option>
                <option v-for="cat in categories" :key="cat.id" :value="cat.id">
                  {{ cat.name }}
                </option>
              </select>
            </div>

            <div class="detail-section">
              <h4>Tags</h4>
              <div class="tags-select">
                <label v-for="tag in tags" :key="tag.id" class="tag-checkbox">
                  <input
                    type="checkbox"
                    :value="tag.id"
                    v-model="updateForm.tag_ids"
                    @change="updateTags"
                  />
                  <span class="tag-label">{{ tag.name }}</span>
                </label>
              </div>
            </div>

            <div class="detail-section">
              <h4>Add Response</h4>
              <textarea
                v-model="responseMessage"
                class="form-textarea"
                placeholder="Write a response to this feedback..."
              ></textarea>
              <button class="btn btn-primary mt-2" @click="sendResponse" :disabled="!responseMessage.trim()">
                Send Response
              </button>
            </div>

            <div v-if="selectedFeedback.admin_responses?.length" class="detail-section">
              <h4>Previous Responses</h4>
              <div v-for="resp in selectedFeedback.admin_responses" :key="resp.id" class="response-item">
                <p>{{ resp.message }}</p>
                <small class="text-secondary">{{ formatDate(resp.created_at) }}</small>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { adminApi, analyticsApi, categoriesApi, tagsApi, feedbackApi } from '../api/client'

const feedback = ref([])
const stats = ref({})
const categories = ref([])
const tags = ref([])
const loading = ref(true)
const page = ref(1)
const pageSize = 20
const total = ref(0)
const statusFilter = ref('')
const categoryFilter = ref('')

const selectedFeedback = ref(null)
const updateForm = ref({ status: '', category_id: null, tag_ids: [] })
const responseMessage = ref('')

const totalPages = computed(() => Math.ceil(total.value / pageSize))

async function loadFeedback() {
  loading.value = true
  try {
    const params = { page: page.value, page_size: pageSize }
    if (statusFilter.value) params.status = statusFilter.value
    if (categoryFilter.value) params.category_id = categoryFilter.value
    
    const response = await adminApi.getAllFeedback(params)
    feedback.value = response.data.items
    total.value = response.data.total
  } catch (error) {
    console.error('Failed to load feedback:', error)
  } finally {
    loading.value = false
  }
}

async function loadStats() {
  try {
    const response = await analyticsApi.getOverview()
    stats.value = response.data
  } catch (error) {
    console.error('Failed to load stats:', error)
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

async function openDetailModal(item) {
  try {
    const response = await feedbackApi.getById(item.id)
    selectedFeedback.value = response.data
    updateForm.value = {
      status: item.status,
      category_id: item.category_id,
      tag_ids: item.tags?.map(t => t.id) || []
    }
    responseMessage.value = ''
  } catch (error) {
    alert('Failed to load feedback details')
  }
}

async function updateStatus() {
  try {
    await adminApi.updateStatus(selectedFeedback.value.id, updateForm.value.status)
    loadFeedback()
    loadStats()
  } catch (error) {
    alert('Failed to update status')
  }
}

async function updateCategory() {
  if (!updateForm.value.category_id) return
  try {
    await adminApi.updateCategory(selectedFeedback.value.id, updateForm.value.category_id)
    loadFeedback()
  } catch (error) {
    alert('Failed to update category')
  }
}

async function updateTags() {
  try {
    await adminApi.updateTags(selectedFeedback.value.id, updateForm.value.tag_ids)
    loadFeedback()
  } catch (error) {
    alert('Failed to update tags')
  }
}

async function sendResponse() {
  if (!responseMessage.value.trim()) return
  try {
    await adminApi.respond(selectedFeedback.value.id, responseMessage.value)
    responseMessage.value = ''
    openDetailModal(selectedFeedback.value)
  } catch (error) {
    alert('Failed to send response')
  }
}

function formatStatus(status) {
  return status.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())
}

function formatDate(date) {
  return new Date(date).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

function formatHours(hours) {
  if (!hours) return '-'
  if (hours < 24) return `${hours.toFixed(1)}h`
  return `${(hours / 24).toFixed(1)}d`
}

function formatSentiment(score) {
  if (score === null || score === undefined) return '-'
  if (score >= 0.3) return 'Positive'
  if (score <= -0.3) return 'Negative'
  return 'Neutral'
}

function getSentimentClass(score) {
  if (score === null || score === undefined) return ''
  if (score >= 0.3) return 'text-success'
  if (score <= -0.3) return 'text-danger'
  return 'text-secondary'
}

onMounted(() => {
  loadFeedback()
  loadStats()
  loadOptions()
})
</script>

<style scoped>
.stat-card {
  text-align: center;
  padding: 1.5rem;
}

.stat-value {
  font-size: 2rem;
  font-weight: 700;
  color: var(--primary-color);
}

.stat-label {
  font-size: 0.875rem;
  color: var(--text-secondary);
  margin-top: 0.25rem;
}

.filters {
  padding: 1rem 1.5rem;
}

.btn-sm {
  padding: 0.375rem 0.75rem;
  font-size: 0.75rem;
}

.pagination {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
}

.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 1rem;
}

.modal {
  width: 100%;
  max-width: 600px;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-lg {
  max-width: 700px;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid var(--border-color);
}

.btn-close {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: var(--text-secondary);
}

.detail-section {
  margin-bottom: 1.5rem;
}

.detail-section h4 {
  font-size: 0.875rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: var(--text-secondary);
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

.tag-label {
  font-size: 0.875rem;
}

.response-item {
  background: var(--background-color);
  padding: 1rem;
  border-radius: 0.5rem;
  margin-bottom: 0.5rem;
}
</style>
