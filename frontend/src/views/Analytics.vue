<template>
  <div class="page">
    <div class="container">
      <div class="page-header">
        <h1 class="page-title">Analytics Dashboard</h1>
        <p class="page-subtitle">Insights and trends from your feedback data</p>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="loading-container">
        <div class="spinner"></div>
      </div>

      <template v-else>
        <!-- Overview Cards -->
        <AnalyticsCards :stats="overview" />

        <!-- Charts Row -->
        <div class="grid grid-2 mt-6">
          <!-- Timeseries Chart -->
          <div class="card">
            <h3 class="card-title">Feedback Volume (Last 30 Days)</h3>
            <div class="chart-container">
              <Line :data="timeseriesChartData" :options="chartOptions" />
            </div>
          </div>

          <!-- Sentiment Trends -->
          <div class="card">
            <h3 class="card-title">Sentiment Trends</h3>
            <div class="chart-container">
              <Line :data="sentimentChartData" :options="sentimentChartOptions" />
            </div>
          </div>
        </div>

        <!-- Categories and Tags -->
        <div class="grid grid-2 mt-6">
          <!-- Top Categories -->
          <div class="card">
            <h3 class="card-title">Top Categories</h3>
            <div v-if="topCategories.length" class="stats-list">
              <div v-for="cat in topCategories" :key="cat.category_id" class="stats-item">
                <span class="stats-name">{{ cat.category_name }}</span>
                <span class="stats-value">{{ cat.count }}</span>
              </div>
            </div>
            <p v-else class="text-secondary">No categories yet</p>
          </div>

          <!-- Top Tags -->
          <div class="card">
            <h3 class="card-title">Top Tags</h3>
            <div v-if="topTags.length" class="stats-list">
              <div v-for="tag in topTags" :key="tag.tag_id" class="stats-item">
                <span class="stats-name">{{ tag.tag_name }}</span>
                <span class="stats-value">{{ tag.count }}</span>
              </div>
            </div>
            <p v-else class="text-secondary">No tags yet</p>
          </div>
        </div>

        <!-- Topic Clusters -->
        <div class="card mt-6">
          <h3 class="card-title">Topic Clusters</h3>
          <p class="text-secondary mb-4">AI-generated groupings of similar feedback</p>
          
          <div v-if="topics.length" class="topics-grid">
            <div v-for="topic in topics" :key="topic.cluster_id" class="topic-card">
              <div class="topic-header">
                <span class="topic-count">{{ topic.count }} items</span>
              </div>
              <div class="topic-keywords">
                <span v-for="kw in topic.keywords.slice(0, 3)" :key="kw" class="keyword-badge">
                  {{ kw }}
                </span>
              </div>
              <div class="topic-examples">
                <strong>Examples:</strong>
                <ul>
                  <li v-for="title in topic.example_titles.slice(0, 2)" :key="title">
                    {{ title }}
                  </li>
                </ul>
              </div>
            </div>
          </div>
          <p v-else class="text-secondary">Not enough feedback for topic analysis</p>
        </div>
      </template>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { Line } from 'vue-chartjs'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
} from 'chart.js'
import { analyticsApi } from '../api/client'
import AnalyticsCards from '../components/AnalyticsCards.vue'

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
)

const loading = ref(true)
const overview = ref({})
const timeseries = ref([])
const sentimentTrends = ref([])
const topCategories = ref([])
const topTags = ref([])
const topics = ref([])

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  interaction: {
    mode: 'index',
    intersect: false,
  },
  plugins: {
    legend: { display: false },
    tooltip: {
      enabled: true,
      backgroundColor: 'rgba(17, 24, 39, 0.95)',
      titleColor: '#fff',
      bodyColor: '#e5e7eb',
      titleFont: { size: 13, weight: '600' },
      bodyFont: { size: 12 },
      padding: 12,
      cornerRadius: 8,
      displayColors: false,
      callbacks: {
        title: (items) => items[0]?.label || '',
        label: (item) => `${item.parsed.y} feedback items`
      }
    }
  },
  scales: {
    y: { 
      beginAtZero: true,
      grid: { color: 'rgba(0,0,0,0.05)' },
      ticks: { color: '#6b7280', font: { size: 11 } }
    },
    x: {
      grid: { display: false },
      ticks: { color: '#6b7280', font: { size: 11 } }
    }
  },
  elements: {
    point: {
      radius: 0,
      hoverRadius: 6,
      hoverBackgroundColor: '#3b82f6',
      hoverBorderColor: '#fff',
      hoverBorderWidth: 2
    },
    line: {
      borderWidth: 2.5
    }
  }
}

const sentimentChartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  interaction: {
    mode: 'index',
    intersect: false,
  },
  plugins: {
    legend: { display: false },
    tooltip: {
      enabled: true,
      backgroundColor: 'rgba(17, 24, 39, 0.95)',
      titleColor: '#fff',
      bodyColor: '#e5e7eb',
      titleFont: { size: 13, weight: '600' },
      bodyFont: { size: 12 },
      padding: 12,
      cornerRadius: 8,
      displayColors: false,
      callbacks: {
        title: (items) => items[0]?.label || '',
        label: (item) => {
          const val = item.parsed.y.toFixed(2)
          const sentiment = val >= 0.2 ? '😊 Positive' : val <= -0.2 ? '😞 Negative' : '😐 Neutral'
          return `Score: ${val} (${sentiment})`
        }
      }
    }
  },
  scales: {
    y: { 
      min: -1, 
      max: 1,
      grid: { color: 'rgba(0,0,0,0.05)' },
      ticks: { 
        color: '#6b7280', 
        font: { size: 11 },
        callback: (val) => val === 0 ? '0' : val > 0 ? `+${val}` : val
      }
    },
    x: {
      grid: { display: false },
      ticks: { color: '#6b7280', font: { size: 11 } }
    }
  },
  elements: {
    point: {
      radius: 0,
      hoverRadius: 6,
      hoverBackgroundColor: '#22c55e',
      hoverBorderColor: '#fff',
      hoverBorderWidth: 2
    },
    line: {
      borderWidth: 2.5
    }
  }
}

const timeseriesChartData = computed(() => ({
  labels: timeseries.value.map(d => formatDate(d.date)),
  datasets: [{
    data: timeseries.value.map(d => d.count),
    borderColor: '#3b82f6',
    backgroundColor: 'rgba(59, 130, 246, 0.1)',
    fill: true,
    tension: 0.4
  }]
}))

const sentimentChartData = computed(() => ({
  labels: sentimentTrends.value.map(d => formatDate(d.date)),
  datasets: [{
    data: sentimentTrends.value.map(d => d.average_sentiment),
    borderColor: '#22c55e',
    backgroundColor: 'rgba(34, 197, 94, 0.1)',
    fill: true,
    tension: 0.4
  }]
}))

function formatDate(dateStr) {
  const date = new Date(dateStr)
  return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
}

async function loadAnalytics() {
  loading.value = true
  try {
    const [
      overviewRes,
      timeseriesRes,
      sentimentRes,
      categoriesRes,
      tagsRes,
      topicsRes
    ] = await Promise.all([
      analyticsApi.getOverview(),
      analyticsApi.getTimeseries(30),
      analyticsApi.getSentimentTrends(30),
      analyticsApi.getTopCategories(10),
      analyticsApi.getTopTags(10),
      analyticsApi.getTopics(5)
    ])

    overview.value = overviewRes.data
    timeseries.value = timeseriesRes.data.data
    sentimentTrends.value = sentimentRes.data.data
    topCategories.value = categoriesRes.data.data
    topTags.value = tagsRes.data.data
    topics.value = topicsRes.data.clusters
  } catch (error) {
    console.error('Failed to load analytics:', error)
  } finally {
    loading.value = false
  }
}

onMounted(loadAnalytics)
</script>

<style scoped>
.card-title {
  font-size: 1rem;
  font-weight: 600;
  margin-bottom: 1rem;
  color: var(--gray-800);
}

.chart-container {
  height: 250px;
  position: relative;
}

/* Stats List with hover effects */
.stats-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.stats-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 1rem;
  border-radius: var(--radius-md);
  background: transparent;
  transition: all var(--transition);
  cursor: default;
}

.stats-item:hover {
  background: var(--gray-50);
  transform: translateX(4px);
}

.stats-name {
  font-weight: 500;
  color: var(--gray-700);
  transition: color var(--transition);
}

.stats-item:hover .stats-name {
  color: var(--primary-600);
}

.stats-value {
  background: var(--gray-100);
  padding: 0.375rem 0.875rem;
  border-radius: 9999px;
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--gray-700);
  transition: all var(--transition);
}

.stats-item:hover .stats-value {
  background: var(--primary-100);
  color: var(--primary-700);
  transform: scale(1.05);
}

/* Topics Grid with enhanced cards */
.topics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1rem;
}

.topic-card {
  background: var(--gray-50);
  border-radius: var(--radius-md);
  padding: 1.25rem;
  border: 1px solid transparent;
  transition: all var(--transition);
  cursor: default;
}

.topic-card:hover {
  background: white;
  border-color: var(--primary-200);
  box-shadow: var(--shadow-sm);
  transform: translateY(-2px);
}

.topic-header {
  margin-bottom: 0.75rem;
}

.topic-count {
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--primary-600);
  display: inline-flex;
  align-items: center;
  gap: 0.375rem;
}

.topic-count::before {
  content: '';
  width: 8px;
  height: 8px;
  background: var(--primary-500);
  border-radius: 50%;
  opacity: 0.7;
}

.topic-keywords {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.keyword-badge {
  background: linear-gradient(135deg, var(--primary-500), var(--primary-600));
  color: white;
  padding: 0.375rem 0.625rem;
  border-radius: var(--radius);
  font-size: 0.75rem;
  font-weight: 500;
  transition: all var(--transition);
}

.keyword-badge:hover {
  transform: translateY(-2px) scale(1.02);
  box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
}

.topic-examples {
  font-size: 0.8125rem;
}

.topic-examples strong {
  color: var(--gray-600);
  font-weight: 600;
}

.topic-examples ul {
  margin-top: 0.5rem;
  padding-left: 1.25rem;
  list-style: none;
}

.topic-examples li {
  color: var(--gray-500);
  margin-bottom: 0.375rem;
  position: relative;
  padding-left: 0.75rem;
  transition: all var(--transition);
}

.topic-examples li::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0.5em;
  width: 4px;
  height: 4px;
  background: var(--gray-400);
  border-radius: 50%;
  transition: all var(--transition);
}

.topic-card:hover .topic-examples li {
  color: var(--gray-700);
  transform: translateX(2px);
}

.topic-card:hover .topic-examples li::before {
  background: var(--primary-500);
}
</style>
