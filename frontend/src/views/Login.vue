<template>
  <div class="auth-page">
    <div class="auth-container">
      <div class="auth-card card">
        <h1 class="auth-title">Welcome Back</h1>
        <p class="auth-subtitle">Sign in to your account</p>

        <div v-if="error" class="alert alert-error">
          {{ error }}
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
const loading = ref(false)

async function handleLogin() {
  error.value = ''
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
  max-width: 400px;
}

.auth-card {
  padding: 2.5rem;
}

.auth-title {
  text-align: center;
  font-size: 1.75rem;
  margin-bottom: 0.5rem;
}

.auth-subtitle {
  text-align: center;
  color: var(--text-secondary);
  margin-bottom: 1.5rem;
}

.auth-form {
  margin-top: 1.5rem;
}

.btn-full {
  width: 100%;
  margin-top: 1rem;
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
