<template>
  <div class="feedback-list">
    <div v-for="item in feedback" :key="item.id" class="feedback-card">
      <div class="feedback-header">
        <div class="feedback-title-section">
          <h3 class="feedback-title">{{ item.title }}</h3>
          <div class="feedback-badges">
            <span :class="['status-badge', `status-${item.status}`]">
              <span class="status-dot"></span>
              {{ formatStatus(item.status) }}
            </span>
            <span 
              v-if="item.sentiment_label || item.sentiment_score !== null" 
              :class="['sentiment-badge', `sentiment-${getSentimentKey(item)}`]"
            >
              {{ getSentimentIcon(item) }} {{ getSentimentLabel(item) }}
            </span>
          </div>
        </div>
      </div>
      
      <p class="feedback-content">{{ item.content }}</p>
      
      <div class="feedback-meta">
        <div class="meta-row">
          <div class="meta-item" v-if="item.category">
            <svg class="meta-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/>
            </svg>
            <span>{{ item.category.name }}</span>
          </div>
          <div class="meta-item" v-if="item.tags?.length">
            <svg class="meta-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M20.59 13.41l-7.17 7.17a2 2 0 0 1-2.83 0L2 12V2h10l8.59 8.59a2 2 0 0 1 0 2.82z"/>
              <line x1="7" y1="7" x2="7.01" y2="7"/>
            </svg>
            <div class="tags-list">
              <span v-for="tag in item.tags" :key="tag.id" class="tag-chip">
                {{ tag.name }}
              </span>
            </div>
          </div>
        </div>
        <div class="meta-date">
          <svg class="meta-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"/>
            <polyline points="12 6 12 12 16 14"/>
          </svg>
          <span>{{ formatDate(item.created_at) }}</span>
        </div>
      </div>

      <div v-if="showActions && canEdit(item)" class="feedback-actions">
        <button class="action-btn action-edit" @click="$emit('edit', item)">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
            <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
          </svg>
          Edit
        </button>
        <button class="action-btn action-delete" @click="$emit('delete', item)">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="3 6 5 6 21 6"/>
            <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>
          </svg>
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

function getSentimentLabel(item) {
  if (item.sentiment_label) {
    return item.sentiment_label.charAt(0).toUpperCase() + item.sentiment_label.slice(1)
  }
  const score = item.sentiment_score
  if (score === null || score === undefined) return 'Unknown'
  if (score >= 0.2) return 'Positive'
  if (score <= -0.2) return 'Negative'
  return 'Neutral'
}

function getSentimentKey(item) {
  return getSentimentLabel(item).toLowerCase()
}

function getSentimentIcon(item) {
  const label = getSentimentLabel(item).toLowerCase()
  if (label === 'positive') return '😊'
  if (label === 'negative') return '😟'
  return '😐'
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
  background: white;
  border-radius: 16px;
  padding: 1.5rem;
  border: 1px solid var(--gray-100);
  transition: all 0.2s ease;
  position: relative;
}

.feedback-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: var(--accent-gradient);
  border-radius: 16px 16px 0 0;
  opacity: 0;
  transition: opacity 0.2s;
}

.feedback-card:hover {
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

.feedback-card:hover::before {
  opacity: 1;
}

.feedback-header {
  margin-bottom: 1rem;
}

.feedback-title-section {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 1rem;
  flex-wrap: wrap;
}

.feedback-title {
  font-size: 1.125rem;
  font-weight: 700;
  color: var(--gray-900);
  margin: 0;
  line-height: 1.4;
}

.feedback-badges {
  display: flex;
  gap: 0.5rem;
  flex-shrink: 0;
  flex-wrap: wrap;
}

/* Status badges */
.status-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.375rem;
  padding: 0.375rem 0.75rem;
  font-size: 0.75rem;
  font-weight: 600;
  border-radius: 20px;
  text-transform: capitalize;
}

.status-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.status-new {
  background: linear-gradient(135deg, #dbeafe, #bfdbfe);
  color: #1e40af;
}
.status-new .status-dot { background: #3b82f6; }

.status-triaged {
  background: linear-gradient(135deg, #fef3c7, #fde68a);
  color: #92400e;
}
.status-triaged .status-dot { background: #f59e0b; }

.status-in_progress {
  background: linear-gradient(135deg, #e0e7ff, #c7d2fe);
  color: #3730a3;
}
.status-in_progress .status-dot { background: #6366f1; }

.status-resolved {
  background: linear-gradient(135deg, #d1fae5, #a7f3d0);
  color: #065f46;
}
.status-resolved .status-dot { background: #10b981; animation: none; }

.status-rejected {
  background: linear-gradient(135deg, #fee2e2, #fecaca);
  color: #991b1b;
}
.status-rejected .status-dot { background: #ef4444; animation: none; }

/* Sentiment badges */
.sentiment-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  padding: 0.375rem 0.75rem;
  font-size: 0.75rem;
  font-weight: 600;
  border-radius: 20px;
}

.sentiment-positive {
  background: linear-gradient(135deg, #d1fae5, #a7f3d0);
  color: #065f46;
}

.sentiment-neutral {
  background: linear-gradient(135deg, #f3f4f6, #e5e7eb);
  color: #374151;
}

.sentiment-negative {
  background: linear-gradient(135deg, #fee2e2, #fecaca);
  color: #991b1b;
}

.feedback-content {
  color: var(--gray-600);
  line-height: 1.7;
  margin-bottom: 1.25rem;
  font-size: 0.9375rem;
}

.feedback-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;
  padding-top: 1rem;
  border-top: 1px solid var(--gray-100);
}

.meta-row {
  display: flex;
  flex-wrap: wrap;
  gap: 1.25rem;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.8125rem;
  color: var(--gray-500);
}

.meta-icon {
  width: 16px;
  height: 16px;
  color: var(--gray-400);
}

.meta-date {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.8125rem;
  color: var(--gray-400);
}

.tags-list {
  display: flex;
  gap: 0.375rem;
  flex-wrap: wrap;
}

.tag-chip {
  background: var(--gray-100);
  color: var(--gray-600);
  padding: 0.125rem 0.5rem;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 500;
}

.feedback-actions {
  display: flex;
  gap: 0.75rem;
  margin-top: 1.25rem;
  padding-top: 1rem;
  border-top: 1px solid var(--gray-100);
}

.action-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.375rem;
  padding: 0.5rem 1rem;
  font-size: 0.8125rem;
  font-weight: 600;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  transition: all 0.2s;
}

.action-btn svg {
  width: 16px;
  height: 16px;
}

.action-edit {
  background: var(--gray-100);
  color: var(--gray-700);
}

.action-edit:hover {
  background: var(--primary-50);
  color: var(--primary-600);
}

.action-delete {
  background: var(--danger-50);
  color: var(--danger-600);
}

.action-delete:hover {
  background: #fee2e2;
  color: #dc2626;
}
</style>
