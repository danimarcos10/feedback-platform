<template>
  <div class="page">
    <div class="container">
      <div class="page-header-row">
        <div class="page-header">
          <h1 class="page-title">My Feedback</h1>
          <p class="page-subtitle">View and manage your submitted feedback</p>
        </div>
        <router-link to="/submit" class="btn btn-primary">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="18" height="18">
            <line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/>
          </svg>
          New Feedback
        </router-link>
      </div>

      <!-- Filters -->
      <div class="filters card mb-6">
        <div class="flex gap-4 items-center">
          <div class="form-group" style="margin-bottom: 0; flex: 1;">
            <label class="form-label">Filter by Status</label>
            <select v-model="statusFilter" class="form-select" @change="loadFeedback">
              <option value="">All Status</option>
              <option value="new">New</option>
              <option value="triaged">Triaged</option>
              <option value="in_progress">In Progress</option>
              <option value="resolved">Resolved</option>
              <option value="rejected">Rejected</option>
            </select>
          </div>
        </div>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="loading-container">
        <div class="spinner"></div>
      </div>

      <!-- Feedback List -->
      <FeedbackList
        v-else-if="feedback.length > 0"
        :feedback="feedback"
        :show-actions="true"
        @edit="openEditModal"
        @delete="deleteFeedback"
      />

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

const editingFeedback = ref(null)
const editForm = ref({ title: '', content: '' })

const totalPages = computed(() => Math.ceil(total.value / pageSize))

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
.page-header-row {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 1rem;
  margin-bottom: 2rem;
}

@media (max-width: 640px) {
  .page-header-row {
    flex-direction: column;
  }
}

.filters {
  padding: 1.25rem 1.5rem;
  border-radius: 16px;
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
