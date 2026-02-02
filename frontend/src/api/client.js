import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

console.log('[API Client] Connecting to backend at:', API_URL)

const client = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000, // 10 second timeout
})

// Request interceptor to add auth token and log requests
client.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    console.log(`[API] ${config.method?.toUpperCase()} ${config.url}`, config.data || '')
    return config
  },
  (error) => {
    console.error('[API] Request error:', error)
    return Promise.reject(error)
  }
)

// Response interceptor to handle errors with detailed logging
client.interceptors.response.use(
  (response) => {
    console.log(`[API] Response ${response.status}:`, response.data)
    return response
  },
  (error) => {
    // Log detailed error information
    console.error('[API] Error details:', {
      message: error.message,
      status: error.response?.status,
      statusText: error.response?.statusText,
      data: error.response?.data,
      url: error.config?.url,
      method: error.config?.method,
    })

    // Handle specific error types
    if (error.code === 'ECONNABORTED') {
      error.userMessage = 'Request timed out. Please check if the server is running.'
    } else if (error.code === 'ERR_NETWORK' || !error.response) {
      error.userMessage = 'Cannot connect to server. Please ensure the backend is running at ' + API_URL
    } else if (error.response?.status === 401) {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      window.location.href = '/login'
      error.userMessage = 'Session expired. Please login again.'
    } else if (error.response?.status === 422) {
      // Validation error - extract details
      const detail = error.response.data?.detail
      if (Array.isArray(detail)) {
        error.userMessage = detail.map(d => `${d.loc?.join('.')}: ${d.msg}`).join(', ')
      } else {
        error.userMessage = detail || 'Validation error'
      }
    } else if (error.response?.status === 500) {
      error.userMessage = 'Server error. Please check the backend logs.'
    } else {
      error.userMessage = error.response?.data?.detail || error.message
    }

    return Promise.reject(error)
  }
)

// Auth API
export const authApi = {
  register: (email, password) => 
    client.post('/auth/register', { email, password }),
  
  login: (email, password) => {
    const formData = new URLSearchParams()
    formData.append('username', email)
    formData.append('password', password)
    return client.post('/auth/login', formData, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    })
  },
  
  getMe: () => client.get('/auth/me'),
}

// Feedback API
export const feedbackApi = {
  create: (data) => client.post('/feedback/', data),
  getMine: (params) => client.get('/feedback/mine', { params }),
  getById: (id) => client.get(`/feedback/${id}`),
  update: (id, data) => client.put(`/feedback/${id}`, data),
  delete: (id) => client.delete(`/feedback/${id}`),
}

// Admin API
export const adminApi = {
  getAllFeedback: (params) => client.get('/admin/feedback', { params }),
  updateStatus: (id, status) => client.put(`/admin/feedback/${id}/status`, { status }),
  updateCategory: (id, categoryId) => client.put(`/admin/feedback/${id}/category`, { category_id: categoryId }),
  updateTags: (id, tagIds) => client.put(`/admin/feedback/${id}/tags`, { tag_ids: tagIds }),
  respond: (id, message) => client.post(`/admin/feedback/${id}/respond`, { message }),
}

// Analytics API
export const analyticsApi = {
  getOverview: () => client.get('/analytics/overview'),
  getTimeseries: (days = 30) => client.get('/analytics/timeseries', { params: { days } }),
  getTopTags: (limit = 10) => client.get('/analytics/top-tags', { params: { limit } }),
  getTopCategories: (limit = 10) => client.get('/analytics/top-categories', { params: { limit } }),
  getSentimentTrends: (days = 30) => client.get('/analytics/sentiment-trends', { params: { days } }),
  getTopics: (k = 5) => client.get('/analytics/topics', { params: { k } }),
}

// Categories API
export const categoriesApi = {
  list: () => client.get('/categories/'),
  create: (name) => client.post('/categories/', { name }),
  update: (id, name) => client.put(`/categories/${id}`, { name }),
  delete: (id) => client.delete(`/categories/${id}`),
}

// Tags API
export const tagsApi = {
  list: () => client.get('/tags/'),
  create: (name) => client.post('/tags/', { name }),
  update: (id, name) => client.put(`/tags/${id}`, { name }),
  delete: (id) => client.delete(`/tags/${id}`),
}

export default client
