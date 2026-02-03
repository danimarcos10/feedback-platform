<template>
  <div class="page page-with-bg">
    <div class="container">
      <div class="page-header">
        <h1 class="page-title">Admin Dashboard</h1>
        <p class="page-subtitle">Manage all feedback submissions</p>
      </div>

      <!-- Quick Stats -->
      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-icon stat-icon-primary">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
            </svg>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ stats.total_feedback || 0 }}</div>
            <div class="stat-label">Total Feedback</div>
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-icon stat-icon-warning">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>
            </svg>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ stats.open_feedback || 0 }}</div>
            <div class="stat-label">Open Items</div>
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-icon stat-icon-success">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>
              <polyline points="22 4 12 14.01 9 11.01"/>
            </svg>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ stats.resolved_feedback || 0 }}</div>
            <div class="stat-label">Resolved</div>
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-icon stat-icon-info">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/>
              <polyline points="17 6 23 6 23 12"/>
            </svg>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ formatHours(stats.average_resolution_time_hours) }}</div>
            <div class="stat-label">Avg Resolution</div>
          </div>
        </div>
      </div>

      <!-- Command Bar -->
      <div class="command-bar">
        <div class="command-bar-left">
          <div class="search-input-wrapper">
            <svg class="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>
            </svg>
            <input 
              v-model="searchQuery" 
              type="text" 
              class="search-input" 
              placeholder="Search feedback..."
              @input="debouncedSearch"
            />
          </div>
          <select v-model="statusFilter" class="filter-select" @change="loadFeedback">
            <option value="">All Status</option>
            <option value="new">New</option>
            <option value="triaged">Triaged</option>
            <option value="in_progress">In Progress</option>
            <option value="resolved">Resolved</option>
            <option value="rejected">Rejected</option>
          </select>
          <select v-model="categoryFilter" class="filter-select" @change="loadFeedback">
            <option value="">All Categories</option>
            <option v-for="cat in categories" :key="cat.id" :value="cat.id">
              {{ cat.name }}
            </option>
          </select>
        </div>
        <router-link to="/admin/analytics" class="btn btn-primary">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="18" height="18">
            <line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/>
          </svg>
          View Analytics
        </router-link>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="loading-container">
        <div class="spinner"></div>
      </div>

      <!-- Feedback List (Card-based) -->
      <div v-else-if="filteredFeedback.length > 0" class="feedback-list">
        <div v-for="item in filteredFeedback" :key="item.id" class="feedback-item" @click="openDetailModal(item)">
          <div class="feedback-item-header">
            <div class="feedback-item-title">
              <h3>{{ item.title }}</h3>
              <div class="feedback-item-badges">
                <span :class="['status-chip', `status-${item.status}`]">
                  <span class="status-dot"></span>
                  {{ formatStatus(item.status) }}
                </span>
                <span :class="['sentiment-chip', `sentiment-${getSentimentLabel(item).toLowerCase()}`]">
                  {{ getSentimentIcon(item) }} {{ getSentimentLabel(item) }}
                </span>
              </div>
            </div>
            <button class="btn btn-outline btn-sm view-btn" @click.stop="openDetailModal(item)">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="16" height="16">
                <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
                <circle cx="12" cy="12" r="3"/>
              </svg>
              View Details
            </button>
          </div>
          <p class="feedback-item-preview">{{ item.content.substring(0, 120) }}{{ item.content.length > 120 ? '...' : '' }}</p>
          <div class="feedback-item-meta">
            <span class="meta-tag" v-if="item.category">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="14" height="14">
                <path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/>
              </svg>
              {{ item.category.name }}
            </span>
            <span class="meta-date">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="14" height="14">
                <rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/>
              </svg>
              {{ formatDate(item.created_at) }}
            </span>
          </div>
        </div>
      </div>

      <!-- No Search Results -->
      <div v-else-if="filteredFeedback.length === 0 && feedback.length > 0" class="empty-state-card card">
        <div class="empty-icon empty-icon-search">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>
          </svg>
        </div>
        <h3 class="empty-title">No results found</h3>
        <p class="empty-description">Try adjusting your search or filters.</p>
        <button class="btn btn-outline" @click="searchQuery = ''; statusFilter = ''; categoryFilter = ''; loadFeedback()">
          Clear Filters
        </button>
      </div>

      <!-- Empty State -->
      <div v-else class="empty-state-card card">
        <div class="empty-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
          </svg>
        </div>
        <h3 class="empty-title">No feedback yet</h3>
        <p class="empty-description">Feedback will appear here when users submit it.</p>
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
import { useToast } from '../stores/toast'

const toast = useToast()

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
const searchQuery = ref('')
let searchTimeout = null

const selectedFeedback = ref(null)
const updateForm = ref({ status: '', category_id: null, tag_ids: [] })
const responseMessage = ref('')

const totalPages = computed(() => Math.ceil(total.value / pageSize))

// Filter feedback locally based on search query
const filteredFeedback = computed(() => {
  if (!searchQuery.value.trim()) return feedback.value
  const query = searchQuery.value.toLowerCase()
  return feedback.value.filter(item => 
    item.title.toLowerCase().includes(query) ||
    item.content.toLowerCase().includes(query)
  )
})

function debouncedSearch() {
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    // Local filtering via computed property
  }, 300)
}

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
    toast.error('Failed to load feedback')
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
    toast.error('Failed to load feedback details')
  }
}

async function updateStatus() {
  try {
    await adminApi.updateStatus(selectedFeedback.value.id, updateForm.value.status)
    toast.success('Status updated successfully')
    loadFeedback()
    loadStats()
  } catch (error) {
    toast.error('Failed to update status')
  }
}

async function updateCategory() {
  if (!updateForm.value.category_id) return
  try {
    await adminApi.updateCategory(selectedFeedback.value.id, updateForm.value.category_id)
    toast.success('Category updated')
    loadFeedback()
  } catch (error) {
    toast.error('Failed to update category')
  }
}

async function updateTags() {
  try {
    await adminApi.updateTags(selectedFeedback.value.id, updateForm.value.tag_ids)
    toast.success('Tags updated')
    loadFeedback()
  } catch (error) {
    toast.error('Failed to update tags')
  }
}

async function sendResponse() {
  if (!responseMessage.value.trim()) return
  try {
    await adminApi.respond(selectedFeedback.value.id, responseMessage.value)
    toast.success('Response sent')
    responseMessage.value = ''
    openDetailModal(selectedFeedback.value)
  } catch (error) {
    toast.error('Failed to send response')
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

function getSentimentLabel(item) {
  if (item.sentiment_label) {
    return item.sentiment_label.charAt(0).toUpperCase() + item.sentiment_label.slice(1)
  }
  const score = item.sentiment_score
  if (score === null || score === undefined) return '-'
  if (score >= 0.2) return 'Positive'
  if (score <= -0.2) return 'Negative'
  return 'Neutral'
}

function getSentimentClass(item) {
  const label = getSentimentLabel(item).toLowerCase()
  if (label === 'positive') return 'badge-sentiment badge-sentiment-positive'
  if (label === 'negative') return 'badge-sentiment badge-sentiment-negative'
  if (label === 'neutral') return 'badge-sentiment badge-sentiment-neutral'
  return ''
}

function getSentimentIcon(item) {
  const label = getSentimentLabel(item).toLowerCase()
  if (label === 'positive') return '😊'
  if (label === 'negative') return '😟'
  return '😐'
}

onMounted(() => {
  loadFeedback()
  loadStats()
  loadOptions()
})
</script>

<style scoped>
/* Command Bar */
.command-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  background: white;
  padding: 1rem 1.25rem;
  border-radius: 16px;
  margin-bottom: 1.5rem;
  border: 1px solid var(--gray-100);
  box-shadow: var(--shadow-sm);
}

.command-bar-left {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex: 1;
}

.search-input-wrapper {
  position: relative;
  flex: 1;
  max-width: 280px;
}

.search-icon {
  position: absolute;
  left: 0.875rem;
  top: 50%;
  transform: translateY(-50%);
  width: 18px;
  height: 18px;
  color: var(--gray-400);
  pointer-events: none;
}

.search-input {
  width: 100%;
  padding: 0.625rem 1rem 0.625rem 2.5rem;
  font-size: 0.875rem;
  border: 2px solid var(--gray-200);
  border-radius: 10px;
  background: var(--gray-50);
  transition: all 0.2s;
}

.search-input:focus {
  outline: none;
  border-color: var(--primary-500);
  background: white;
  box-shadow: 0 0 0 4px var(--primary-50);
}

.filter-select {
  padding: 0.625rem 2rem 0.625rem 0.875rem;
  font-size: 0.875rem;
  border: 2px solid var(--gray-200);
  border-radius: 10px;
  background: var(--gray-50);
  cursor: pointer;
  transition: all 0.2s;
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24' fill='none' stroke='%239ca3af' stroke-width='2'%3E%3Cpolyline points='6 9 12 15 18 9'%3E%3C/polyline%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 0.75rem center;
}

.filter-select:focus {
  outline: none;
  border-color: var(--primary-500);
  background-color: white;
}

/* Feedback List */
.feedback-list {
  display: flex;
  flex-direction: column;
  gap: 0.875rem;
}

.feedback-item {
  background: white;
  border-radius: 14px;
  padding: 1.25rem 1.5rem;
  border: 1px solid var(--gray-100);
  cursor: pointer;
  transition: all 0.2s ease;
  position: relative;
}

.feedback-item::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 4px;
  background: var(--accent-gradient);
  border-radius: 14px 0 0 14px;
  opacity: 0;
  transition: opacity 0.2s;
}

.feedback-item:hover {
  box-shadow: 0 8px 24px -4px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
  border-color: var(--gray-200);
}

.feedback-item:hover::before {
  opacity: 1;
}

.feedback-item-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 1rem;
  margin-bottom: 0.75rem;
}

.feedback-item-title h3 {
  font-size: 1rem;
  font-weight: 600;
  color: var(--gray-900);
  margin: 0 0 0.5rem 0;
  line-height: 1.4;
}

.feedback-item-badges {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.status-chip, .sentiment-chip {
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  padding: 0.25rem 0.625rem;
  font-size: 0.6875rem;
  font-weight: 600;
  border-radius: 20px;
}

.status-dot {
  width: 5px;
  height: 5px;
  border-radius: 50%;
}

.status-new { background: #dbeafe; color: #1e40af; }
.status-new .status-dot { background: #3b82f6; }
.status-triaged { background: #fef3c7; color: #92400e; }
.status-triaged .status-dot { background: #f59e0b; }
.status-in_progress { background: #e0e7ff; color: #3730a3; }
.status-in_progress .status-dot { background: #6366f1; }
.status-resolved { background: #d1fae5; color: #065f46; }
.status-resolved .status-dot { background: #10b981; }
.status-rejected { background: #fee2e2; color: #991b1b; }
.status-rejected .status-dot { background: #ef4444; }

.sentiment-positive { background: #d1fae5; color: #065f46; }
.sentiment-neutral { background: #f3f4f6; color: #374151; }
.sentiment-negative { background: #fee2e2; color: #991b1b; }

.view-btn {
  flex-shrink: 0;
  opacity: 0;
  transform: translateX(8px);
  transition: all 0.2s;
}

.feedback-item:hover .view-btn {
  opacity: 1;
  transform: translateX(0);
}

.feedback-item-preview {
  font-size: 0.875rem;
  color: var(--gray-500);
  line-height: 1.6;
  margin: 0 0 0.875rem 0;
}

.feedback-item-meta {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.meta-tag, .meta-date {
  display: inline-flex;
  align-items: center;
  gap: 0.375rem;
  font-size: 0.75rem;
  color: var(--gray-400);
}

.meta-tag {
  background: var(--gray-50);
  padding: 0.25rem 0.5rem;
  border-radius: 6px;
}

/* Empty states */
.empty-state-card {
  padding: 4rem 2rem;
  text-align: center;
}

.empty-icon {
  width: 64px;
  height: 64px;
  margin: 0 auto 1rem;
  background: linear-gradient(135deg, #eef2ff, #e0e7ff);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #6366f1;
}

.empty-icon svg {
  width: 28px;
  height: 28px;
}

.empty-icon-search {
  background: linear-gradient(135deg, #fef3c7, #fde68a) !important;
  color: #f59e0b !important;
}

.empty-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--gray-900);
  margin-bottom: 0.375rem;
}

.empty-description {
  color: var(--gray-500);
  font-size: 0.875rem;
  margin-bottom: 1.25rem;
}

@media (max-width: 768px) {
  .command-bar {
    flex-direction: column;
    align-items: stretch;
  }
  .command-bar-left {
    flex-direction: column;
  }
  .search-input-wrapper {
    max-width: 100%;
  }
  .feedback-item-header {
    flex-direction: column;
  }
  .view-btn {
    opacity: 1;
    transform: none;
  }
}

/* Stats Grid */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1.25rem;
  margin-bottom: 2rem;
}

@media (max-width: 1024px) {
  .stats-grid { grid-template-columns: repeat(2, 1fr); }
}

@media (max-width: 640px) {
  .stats-grid { grid-template-columns: 1fr; }
  .page-header-row { flex-direction: column; }
}

.stat-card {
  background: white;
  border-radius: 16px;
  padding: 1.5rem;
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  border: 1px solid var(--gray-100);
  transition: all 0.2s ease;
  position: relative;
  overflow: hidden;
}

.stat-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: var(--accent-gradient);
  opacity: 0;
  transition: opacity 0.2s;
}

.stat-card:hover {
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

.stat-card:hover::before {
  opacity: 1;
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.stat-icon svg {
  width: 24px;
  height: 24px;
}

.stat-icon-primary {
  background: linear-gradient(135deg, #eef2ff, #e0e7ff);
  color: #6366f1;
}

.stat-icon-success {
  background: linear-gradient(135deg, #ecfdf5, #d1fae5);
  color: #10b981;
}

.stat-icon-warning {
  background: linear-gradient(135deg, #fffbeb, #fef3c7);
  color: #f59e0b;
}

.stat-icon-info {
  background: linear-gradient(135deg, #eff6ff, #dbeafe);
  color: #3b82f6;
}

.stat-content {
  flex: 1;
}

.stat-value {
  font-size: 1.75rem;
  font-weight: 800;
  color: var(--gray-900);
  line-height: 1;
  letter-spacing: -0.025em;
}

.stat-label {
  font-size: 0.8125rem;
  color: var(--gray-500);
  margin-top: 0.375rem;
  font-weight: 500;
}

/* Filters */
.filters {
  padding: 1.25rem 1.5rem;
  border-radius: 16px;
}

/* Table improvements */
.table-card {
  border-radius: 16px;
  overflow: hidden;
}

.feedback-title-cell strong {
  color: var(--gray-900);
  font-weight: 600;
}

.feedback-excerpt {
  color: var(--gray-500);
  font-size: 0.8125rem;
  margin-top: 0.25rem;
  line-height: 1.4;
}

.btn-sm {
  padding: 0.5rem 1rem;
  font-size: 0.8125rem;
}

/* Pagination */
.pagination {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  margin-top: 2rem;
}

.page-info {
  font-size: 0.875rem;
  color: var(--gray-500);
  font-weight: 500;
}

/* Modal */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(4px);
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
  border-radius: 20px;
  animation: modalSlide 0.2s ease;
}

@keyframes modalSlide {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
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
  border-bottom: 1px solid var(--gray-100);
}

.modal-header h2 {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--gray-900);
}

.btn-close {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--gray-100);
  border: none;
  border-radius: 10px;
  font-size: 1.25rem;
  cursor: pointer;
  color: var(--gray-500);
  transition: all 0.2s;
}

.btn-close:hover {
  background: var(--gray-200);
  color: var(--gray-700);
}

.detail-section {
  margin-bottom: 1.5rem;
}

.detail-section h4 {
  font-size: 0.8125rem;
  font-weight: 600;
  margin-bottom: 0.625rem;
  color: var(--gray-500);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.detail-section p {
  color: var(--gray-700);
  line-height: 1.7;
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
  padding: 0.5rem 0.75rem;
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

.response-item {
  background: var(--gray-50);
  padding: 1rem 1.25rem;
  border-radius: 12px;
  margin-bottom: 0.75rem;
  border-left: 3px solid var(--primary-400);
}

.response-item p {
  color: var(--gray-700);
  margin-bottom: 0.5rem;
}

.response-item small {
  color: var(--gray-500);
  font-size: 0.75rem;
}

/* Empty state */
.empty-state-card {
  padding: 4rem 2rem;
  text-align: center;
  border-radius: 16px;
}

.empty-icon {
  width: 64px;
  height: 64px;
  margin: 0 auto 1rem;
  background: var(--gray-100);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--gray-400);
}

.empty-icon svg {
  width: 32px;
  height: 32px;
}
</style>
