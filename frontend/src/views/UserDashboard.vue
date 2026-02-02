<template>
  <div class="page">
    <div class="container">
      <div class="page-header flex justify-between items-center">
        <div>
          <h1 class="page-title">My Feedback</h1>
          <p class="page-subtitle">View and manage your submitted feedback</p>
        </div>
        <router-link to="/submit" class="btn btn-primary">
          + New Feedback
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
      <div v-else class="card text-center" style="padding: 3rem;">
        <h3>No feedback found</h3>
        <p class="text-secondary mt-2">You haven't submitted any feedback yet.</p>
        <router-link to="/submit" class="btn btn-primary mt-4">
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
.filters {
  padding: 1rem 1.5rem;
}

.pagination {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
}

.page-info {
  font-size: 0.875rem;
  color: var(--text-secondary);
}

.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal {
  width: 100%;
  max-width: 500px;
  max-height: 90vh;
  overflow-y: auto;
}
</style>
