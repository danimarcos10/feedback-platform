<template>
  <div class="analytics-cards grid grid-4">
    <div class="stat-card card">
      <div class="stat-icon stat-icon-blue">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
        </svg>
      </div>
      <div class="stat-content">
        <div class="stat-value">{{ stats.total_feedback || 0 }}</div>
        <div class="stat-label">Total Feedback</div>
      </div>
    </div>

    <div class="stat-card card">
      <div class="stat-icon stat-icon-yellow">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="12" cy="12" r="10"></circle>
          <polyline points="12 6 12 12 16 14"></polyline>
        </svg>
      </div>
      <div class="stat-content">
        <div class="stat-value">{{ stats.open_feedback || 0 }}</div>
        <div class="stat-label">Open Feedback</div>
      </div>
    </div>

    <div class="stat-card card">
      <div class="stat-icon stat-icon-green">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <polyline points="20 6 9 17 4 12"></polyline>
        </svg>
      </div>
      <div class="stat-content">
        <div class="stat-value">{{ stats.resolved_feedback || 0 }}</div>
        <div class="stat-label">Resolved</div>
      </div>
    </div>

    <div class="stat-card card">
      <div class="stat-icon stat-icon-purple">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <line x1="12" y1="20" x2="12" y2="10"></line>
          <line x1="18" y1="20" x2="18" y2="4"></line>
          <line x1="6" y1="20" x2="6" y2="16"></line>
        </svg>
      </div>
      <div class="stat-content">
        <div class="stat-value">{{ formatResolutionTime(stats.average_resolution_time_hours) }}</div>
        <div class="stat-label">Avg Resolution Time</div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  stats: {
    type: Object,
    default: () => ({})
  }
})

function formatResolutionTime(hours) {
  if (!hours) return '-'
  if (hours < 24) return `${hours.toFixed(1)}h`
  return `${(hours / 24).toFixed(1)}d`
}
</script>

<style scoped>
.stat-card {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1.25rem;
  cursor: default;
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
  opacity: 0;
  transition: opacity 0.2s ease;
}

.stat-card:nth-child(1)::before { background: linear-gradient(90deg, #3b82f6, #60a5fa); }
.stat-card:nth-child(2)::before { background: linear-gradient(90deg, #f59e0b, #fbbf24); }
.stat-card:nth-child(3)::before { background: linear-gradient(90deg, #22c55e, #4ade80); }
.stat-card:nth-child(4)::before { background: linear-gradient(90deg, #8b5cf6, #a78bfa); }

.stat-card:hover::before {
  opacity: 1;
}

.stat-card:hover {
  transform: translateY(-3px);
  box-shadow: var(--shadow-md);
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 0.75rem;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  transition: all 0.2s ease;
}

.stat-card:hover .stat-icon {
  transform: scale(1.1) rotate(-5deg);
}

.stat-icon-blue {
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.15), rgba(59, 130, 246, 0.05));
  color: #3b82f6;
}

.stat-icon-yellow {
  background: linear-gradient(135deg, rgba(245, 158, 11, 0.15), rgba(245, 158, 11, 0.05));
  color: #f59e0b;
}

.stat-icon-green {
  background: linear-gradient(135deg, rgba(34, 197, 94, 0.15), rgba(34, 197, 94, 0.05));
  color: #22c55e;
}

.stat-icon-purple {
  background: linear-gradient(135deg, rgba(139, 92, 246, 0.15), rgba(139, 92, 246, 0.05));
  color: #8b5cf6;
}

.stat-content {
  flex: 1;
}

.stat-value {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--text-primary);
  line-height: 1.2;
  transition: all 0.2s ease;
}

.stat-card:hover .stat-value {
  transform: scale(1.02);
}

.stat-card:nth-child(1):hover .stat-value { color: #3b82f6; }
.stat-card:nth-child(2):hover .stat-value { color: #f59e0b; }
.stat-card:nth-child(3):hover .stat-value { color: #22c55e; }
.stat-card:nth-child(4):hover .stat-value { color: #8b5cf6; }

.stat-label {
  font-size: 0.875rem;
  color: var(--text-secondary);
  margin-top: 0.25rem;
  transition: color 0.2s ease;
}

.stat-card:hover .stat-label {
  color: var(--gray-600);
}
</style>
