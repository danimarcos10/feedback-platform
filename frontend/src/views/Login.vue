<template>
  <div class="auth-page">
    <div class="auth-container">
      <div class="auth-card card">
        <h1 class="auth-title">Feedback Platform</h1>
        <p class="auth-subtitle">Sign in to your account</p>

        <!-- Role descriptions -->
        <div class="role-info">
          <div class="role-item">
            <span class="role-icon">👤</span>
            <span><strong>User:</strong> Submit feedback</span>
          </div>
          <div class="role-item">
            <span class="role-icon">⚙️</span>
            <span><strong>Admin:</strong> Manage + Analytics</span>
          </div>
        </div>

        <div v-if="error" class="alert alert-error">
          {{ error }}
        </div>

        <div v-if="success" class="alert alert-success">
          {{ success }}
        </div>

        <form @submit.prevent="handleLogin" class="auth-form">
          <div class="form-group">
            <label class="form-label">Email</label>
            <input
              v-model="email"
              type="email"
              class="form-input"
              placeholder="Enter your email"
              required
            />
          </div>

          <div class="form-group">
            <label class="form-label">Password</label>
            <input
              v-model="password"
              type="password"
              class="form-input"
              placeholder="Enter your password"
              required
            />
          </div>

          <button type="submit" class="btn btn-primary btn-full" :disabled="loading">
            {{ loading ? 'Signing in...' : 'Sign In' }}
          </button>
        </form>

        <div class="auth-divider">
          <span>or try demo accounts</span>
        </div>

        <div class="demo-buttons">
          <button 
            type="button" 
            class="btn btn-demo btn-demo-admin" 
            @click="fillDemoAdmin"
            :disabled="loading"
          >
            Try as Admin
          </button>
          <button 
            type="button" 
            class="btn btn-demo btn-demo-user" 
            @click="fillDemoUser"
            :disabled="loading"
          >
            Try as User
          </button>
        </div>

        <p class="auth-footer">
          Don't have an account?
          <router-link to="/register" class="auth-link">Sign up</router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const email = ref('')
const password = ref('')
const error = ref('')
const success = ref('')
const loading = ref(false)

// Demo account credentials
const DEMO_ADMIN = { email: 'admin@demo.com', password: 'admin1234' }
const DEMO_USER = { email: 'user@demo.com', password: 'user1234' }

async function handleLogin() {
  error.value = ''
  success.value = ''
  loading.value = true

  try {
    const user = await authStore.login(email.value, password.value)
    router.push(user.role === 'admin' ? '/admin' : '/dashboard')
  } catch (err) {
    console.error('Login error:', err)
    error.value = err.userMessage || err.response?.data?.detail || 'Login failed. Please try again.'
  } finally {
    loading.value = false
  }
}

function fillDemoAdmin() {
  email.value = DEMO_ADMIN.email
  password.value = DEMO_ADMIN.password
  success.value = 'Admin credentials filled. Click Sign In to continue.'
  error.value = ''
}

function fillDemoUser() {
  email.value = DEMO_USER.email
  password.value = DEMO_USER.password
  success.value = 'User credentials filled. Click Sign In to continue.'
  error.value = ''
}
</script>

<style scoped>
.auth-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 1rem;
}

.auth-container {
  width: 100%;
  max-width: 420px;
}

.auth-card {
  padding: 2.5rem;
}

.auth-title {
  text-align: center;
  font-size: 1.75rem;
  margin-bottom: 0.5rem;
  color: var(--primary-color);
}

.auth-subtitle {
  text-align: center;
  color: var(--text-secondary);
  margin-bottom: 1rem;
}

.role-info {
  background: var(--background-color);
  border-radius: 0.5rem;
  padding: 0.75rem 1rem;
  margin-bottom: 1.5rem;
}

.role-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  color: var(--text-secondary);
  padding: 0.25rem 0;
}

.role-icon {
  font-size: 1rem;
}

.auth-form {
  margin-top: 1rem;
}

.btn-full {
  width: 100%;
  margin-top: 1rem;
}

.auth-divider {
  display: flex;
  align-items: center;
  margin: 1.5rem 0 1rem;
  color: var(--text-secondary);
  font-size: 0.75rem;
}

.auth-divider::before,
.auth-divider::after {
  content: '';
  flex: 1;
  height: 1px;
  background: var(--border-color);
}

.auth-divider span {
  padding: 0 1rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.demo-buttons {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.75rem;
}

.btn-demo {
  padding: 0.625rem 1rem;
  font-size: 0.8rem;
  font-weight: 500;
  border-radius: 0.5rem;
  border: 1px solid var(--border-color);
  background: white;
  cursor: pointer;
  transition: all 0.15s ease;
}

.btn-demo:hover:not(:disabled) {
  border-color: var(--primary-color);
  background: rgba(59, 130, 246, 0.05);
}

.btn-demo-admin {
  color: #7c3aed;
}

.btn-demo-admin:hover:not(:disabled) {
  border-color: #7c3aed;
  background: rgba(124, 58, 237, 0.05);
}

.btn-demo-user {
  color: #059669;
}

.btn-demo-user:hover:not(:disabled) {
  border-color: #059669;
  background: rgba(5, 150, 105, 0.05);
}

.auth-footer {
  text-align: center;
  margin-top: 1.5rem;
  font-size: 0.875rem;
  color: var(--text-secondary);
}

.auth-link {
  color: var(--primary-color);
  text-decoration: none;
  font-weight: 500;
}

.auth-link:hover {
  text-decoration: underline;
}
</style>
