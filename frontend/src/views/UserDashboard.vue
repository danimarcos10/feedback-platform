<template>
  <div class="page page-with-bg">
    <div class="container">
      <div class="page-header">
        <h1 class="page-title">My Feedback</h1>
        <p class="page-subtitle">View and manage your submitted feedback</p>
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
        </div>
        <router-link to="/submit" class="btn btn-primary">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="18" height="18">
            <line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/>
          </svg>
          New Feedback
        </router-link>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="loading-container">
        <div class="spinner"></div>
      </div>

      <!-- Feedback List -->
      <FeedbackList
        v-else-if="filteredFeedback.length > 0"
        :feedback="filteredFeedback"
        :show-actions="true"
        @edit="openEditModal"
        @delete="deleteFeedback"
      />

      <!-- No Search Results -->
      <div v-else-if="filteredFeedback.length === 0 && feedback.length > 0" class="empty-state-card card">
        <div class="empty-icon empty-icon-search">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>
          </svg>
        </div>
        <h3 class="empty-title">No results found</h3>
        <p class="empty-description">Try adjusting your search or filters to find what you're looking for.</p>
        <button class="btn btn-outline" @click="searchQuery = ''; statusFilter = ''; loadFeedback()">
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
        <p class="empty-description">Start by sharing your thoughts, ideas, or reporting issues.</p>
        <router-link to="/submit" class="btn btn-primary">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="18" height="18">
            <line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/>
          </svg>
          Submit Your First Feedback
        </router-link>
      </div>

      <!-- Pagination -->
      <div v-if="totalPages > 1" class="pagination mt-6">
        <button
          class="btn btn-outline"
          :disabled="page === 1"
          @click="page--; loadFeedback()"
        >
          Previous
        </button>
        <span class="page-info">Page {{ page }} of {{ totalPages }}</span>
        <button
          class="btn btn-outline"
          :disabled="page >= totalPages"
          @click="page++; loadFeedback()"
        >
          Next
        </button>
      </div>

      <!-- Edit Modal -->
      <div v-if="editingFeedback" class="modal-overlay" @click.self="editingFeedback = null">
        <div class="modal card">
          <h2 class="mb-4">Edit Feedback</h2>
          <form @submit.prevent="saveEdit">
            <div class="form-group">
              <label class="form-label">Title</label>
              <input v-model="editForm.title" class="form-input" required />
            </div>
            <div class="form-group">
              <label class="form-label">Content</label>
              <textarea v-model="editForm.content" class="form-textarea" required></textarea>
            </div>
            <div class="flex gap-2 justify-end">
              <button type="button" class="btn btn-outline" @click="editingFeedback = null">
                Cancel
              </button>
              <button type="submit" class="btn btn-primary">
                Save Changes
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { feedbackApi } from '../api/client'
import FeedbackList from '../components/FeedbackList.vue'
import { useToast } from '../stores/toast'

const toast = useToast()

const feedback = ref([])
const loading = ref(true)
const page = ref(1)
const pageSize = 10
const total = ref(0)
const statusFilter = ref('')
const searchQuery = ref('')
let searchTimeout = null

const editingFeedback = ref(null)
const editForm = ref({ title: '', content: '' })

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
    // Local filtering, no API call needed
  }, 300)
}

async function loadFeedback() {
  loading.value = true
  try {
    const params = {
      page: page.value,
      page_size: pageSize,
    }
    if (statusFilter.value) {
      params.status = statusFilter.value
    }
    const response = await feedbackApi.getMine(params)
    feedback.value = response.data.items
    total.value = response.data.total
  } catch (error) {
    console.error('Failed to load feedback:', error)
    toast.error('Failed to load feedback')
  } finally {
    loading.value = false
  }
}

function openEditModal(item) {
  if (item.status === 'resolved') {
    toast.error('Cannot edit resolved feedback')
    return
  }
  editingFeedback.value = item
  editForm.value = { title: item.title, content: item.content }
}

async function saveEdit() {
  try {
    await feedbackApi.update(editingFeedback.value.id, editForm.value)
    editingFeedback.value = null
    toast.success('Feedback updated successfully')
    loadFeedback()
  } catch (error) {
    toast.error(error.response?.data?.detail || 'Failed to update feedback')
  }
}

async function deleteFeedback(item) {
  if (item.status === 'resolved') {
    toast.error('Cannot delete resolved feedback')
    return
  }
  if (!confirm('Are you sure you want to delete this feedback?')) return
  
  try {
    await feedbackApi.delete(item.id)
    toast.success('Feedback deleted successfully')
    loadFeedback()
  } catch (error) {
    toast.error(error.response?.data?.detail || 'Failed to delete feedback')
  }
}

onMounted(loadFeedback)
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
  max-width: 320px;
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

.search-input::placeholder {
  color: var(--gray-400);
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
}

.empty-icon-search {
  background: linear-gradient(135deg, #fef3c7, #fde68a) !important;
  color: #f59e0b !important;
}

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

/* Empty State */
.empty-state-card {
  padding: 4rem 2rem;
  text-align: center;
  border-radius: 16px;
}

.empty-icon {
  width: 80px;
  height: 80px;
  margin: 0 auto 1.25rem;
  background: linear-gradient(135deg, #eef2ff, #e0e7ff);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #6366f1;
}

.empty-icon svg {
  width: 40px;
  height: 40px;
}

.empty-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--gray-900);
  margin-bottom: 0.5rem;
}

.empty-description {
  color: var(--gray-500);
  margin-bottom: 1.5rem;
  max-width: 300px;
  margin-left: auto;
  margin-right: auto;
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
  max-width: 500px;
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
</style>
