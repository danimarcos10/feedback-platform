<template>
  <div class="auth-page">
    <div class="auth-container">
      <div class="auth-card card">
        <h1 class="auth-title">Create Account</h1>
        <p class="auth-subtitle">Sign up to get started</p>

        <div v-if="error" class="alert alert-error">
          {{ error }}
        </div>

        <form @submit.prevent="handleRegister" class="auth-form">
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
              placeholder="Create a password"
              required
              minlength="6"
            />
          </div>

          <div class="form-group">
            <label class="form-label">Confirm Password</label>
            <input
              v-model="confirmPassword"
              type="password"
              class="form-input"
              placeholder="Confirm your password"
              required
            />
          </div>

          <button type="submit" class="btn btn-primary btn-full" :disabled="loading">
            {{ loading ? 'Creating account...' : 'Sign Up' }}
          </button>
        </form>

        <p class="auth-footer">
          Already have an account?
          <router-link to="/login" class="auth-link">Sign in</router-link>
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
const confirmPassword = ref('')
const error = ref('')
const loading = ref(false)

async function handleRegister() {
  error.value = ''

  if (password.value !== confirmPassword.value) {
    error.value = 'Passwords do not match'
    return
  }

  if (password.value.length < 6) {
    error.value = 'Password must be at least 6 characters'
    return
  }

  loading.value = true

  try {
    await authStore.register(email.value, password.value)
    router.push('/dashboard')
  } catch (err) {
    console.error('Registration error:', err)
    // Use the detailed error message from our interceptor
    error.value = err.userMessage || err.response?.data?.detail || 'Registration failed. Please try again.'
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
