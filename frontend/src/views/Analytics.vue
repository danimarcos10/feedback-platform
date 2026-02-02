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
  plugins: {
    legend: { display: false }
  },
  scales: {
    y: { beginAtZero: true }
  }
}

const sentimentChartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { display: false }
  },
  scales: {
    y: { min: -1, max: 1 }
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
}

.chart-container {
  height: 250px;
}

.stats-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.stats-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 0;
  border-bottom: 1px solid var(--border-color);
}

.stats-item:last-child {
  border-bottom: none;
}

.stats-name {
  font-weight: 500;
}

.stats-value {
  background: var(--background-color);
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.875rem;
  font-weight: 600;
}

.topics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1rem;
}

.topic-card {
  background: var(--background-color);
  border-radius: 0.5rem;
  padding: 1rem;
}

.topic-header {
  margin-bottom: 0.75rem;
}

.topic-count {
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--primary-color);
}

.topic-keywords {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 0.75rem;
}

.keyword-badge {
  background: var(--primary-color);
  color: white;
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
  font-size: 0.75rem;
}

.topic-examples {
  font-size: 0.875rem;
}

.topic-examples ul {
  margin-top: 0.25rem;
  padding-left: 1.25rem;
}

.topic-examples li {
  color: var(--text-secondary);
  margin-bottom: 0.25rem;
}
</style>
