<template>
  <div class="feedback-list">
    <div v-for="item in feedback" :key="item.id" class="feedback-card card">
      <div class="feedback-header">
        <h3 class="feedback-title">{{ item.title }}</h3>
        <span :class="['badge', `badge-${item.status}`]">
          {{ formatStatus(item.status) }}
        </span>
      </div>
      
      <p class="feedback-content">{{ item.content }}</p>
      
      <div class="feedback-meta">
        <div class="meta-item" v-if="item.category">
          <span class="meta-label">Category:</span>
          <span>{{ item.category.name }}</span>
        </div>
        <div class="meta-item" v-if="item.tags?.length">
          <span class="meta-label">Tags:</span>
          <span class="tags">
            <span v-for="tag in item.tags" :key="tag.id" class="tag">
              {{ tag.name }}
            </span>
          </span>
        </div>
        <div class="meta-item">
          <span class="meta-label">Created:</span>
          <span>{{ formatDate(item.created_at) }}</span>
        </div>
        <div class="meta-item" v-if="item.sentiment_score !== null">
          <span class="meta-label">Sentiment:</span>
          <span :class="getSentimentClass(item.sentiment_score)">
            {{ formatSentiment(item.sentiment_score) }}
          </span>
        </div>
      </div>

      <div v-if="showActions && canEdit(item)" class="feedback-actions">
        <button class="btn btn-outline btn-sm" @click="$emit('edit', item)">
          Edit
        </button>
        <button class="btn btn-danger btn-sm" @click="$emit('delete', item)">
          Delete
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  feedback: {
    type: Array,
    required: true
  },
  showActions: {
    type: Boolean,
    default: false
  }
})

defineEmits(['edit', 'delete'])

function formatStatus(status) {
  return status.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())
}

function formatDate(date) {
  return new Date(date).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

function formatSentiment(score) {
  if (score >= 0.3) return 'Positive'
  if (score <= -0.3) return 'Negative'
  return 'Neutral'
}

function getSentimentClass(score) {
  if (score >= 0.3) return 'text-success'
  if (score <= -0.3) return 'text-danger'
  return 'text-secondary'
}

function canEdit(item) {
  return item.status !== 'resolved'
}
</script>

<style scoped>
.feedback-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.feedback-card {
  transition: box-shadow 0.15s ease;
}

.feedback-card:hover {
  box-shadow: var(--shadow-md);
}

.feedback-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 1rem;
  margin-bottom: 0.75rem;
}

.feedback-title {
  font-size: 1.125rem;
  font-weight: 600;
  margin: 0;
}

.feedback-content {
  color: var(--text-secondary);
  margin-bottom: 1rem;
  line-height: 1.6;
}

.feedback-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  font-size: 0.875rem;
  padding-top: 1rem;
  border-top: 1px solid var(--border-color);
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.meta-label {
  color: var(--text-secondary);
}

.tags {
  display: flex;
  gap: 0.5rem;
}

.tag {
  background: var(--background-color);
  padding: 0.125rem 0.5rem;
  border-radius: 0.25rem;
  font-size: 0.75rem;
}

.feedback-actions {
  display: flex;
  gap: 0.5rem;
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid var(--border-color);
}

.btn-sm {
  padding: 0.375rem 0.75rem;
  font-size: 0.75rem;
}
</style>
