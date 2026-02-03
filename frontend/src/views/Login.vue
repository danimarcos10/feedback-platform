<template>
  <div class="auth-page">
    <!-- Animated background shapes -->
    <div class="bg-shapes">
      <div class="shape shape-1"></div>
      <div class="shape shape-2"></div>
      <div class="shape shape-3"></div>
    </div>

    <div class="auth-container">
      <!-- Glassmorphism card -->
      <div class="auth-card">
        <!-- Logo/Brand -->
        <div class="brand">
          <div class="brand-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
              <path d="M8 10h8M8 14h4"/>
            </svg>
          </div>
          <h1 class="brand-name">Feedback<span>Hub</span></h1>
        </div>
        
        <p class="auth-subtitle">Welcome back! Sign in to continue</p>

        <!-- Role cards -->
        <div class="role-cards">
          <div class="role-card">
            <div class="role-icon-wrapper role-icon-user">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                <circle cx="12" cy="7" r="4"/>
              </svg>
            </div>
            <div class="role-text">
              <span class="role-title">User</span>
              <span class="role-desc">Submit feedback</span>
            </div>
          </div>
          <div class="role-card">
            <div class="role-icon-wrapper role-icon-admin">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="3"/>
                <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/>
              </svg>
            </div>
            <div class="role-text">
              <span class="role-title">Admin</span>
              <span class="role-desc">Manage & Analytics</span>
            </div>
          </div>
        </div>

        <div v-if="error" class="alert alert-error">
          <svg class="alert-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/>
          </svg>
          {{ error }}
        </div>

        <div v-if="success" class="alert alert-success">
          <svg class="alert-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/>
          </svg>
          {{ success }}
        </div>

        <form @submit.prevent="handleLogin" class="auth-form">
          <div class="form-group">
            <label class="form-label">Email</label>
            <div class="input-wrapper">
              <svg class="input-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/>
                <polyline points="22,6 12,13 2,6"/>
              </svg>
              <input
                v-model="email"
                type="email"
                class="form-input"
                placeholder="Enter your email"
                required
              />
            </div>
          </div>

          <div class="form-group">
            <label class="form-label">Password</label>
            <div class="input-wrapper">
              <svg class="input-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
                <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
              </svg>
              <input
                v-model="password"
                type="password"
                class="form-input"
                placeholder="Enter your password"
                required
              />
            </div>
          </div>

          <button type="submit" class="btn btn-primary btn-full" :disabled="loading">
            <span v-if="loading" class="btn-loader"></span>
            {{ loading ? 'Signing in...' : 'Sign In' }}
            <svg v-if="!loading" class="btn-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/>
            </svg>
          </button>
        </form>

        <div class="auth-divider">
          <span>Quick demo access</span>
        </div>

        <div class="demo-buttons">
          <button 
            type="button" 
            class="demo-card demo-admin" 
            @click="fillDemoAdmin"
            :disabled="loading"
          >
            <div class="demo-card-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
              </svg>
            </div>
            <div class="demo-card-content">
              <span class="demo-card-title">Admin Demo</span>
              <span class="demo-card-email">admin@demo.com</span>
            </div>
          </button>
          <button 
            type="button" 
            class="demo-card demo-user" 
            @click="fillDemoUser"
            :disabled="loading"
          >
            <div class="demo-card-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                <circle cx="12" cy="7" r="4"/>
              </svg>
            </div>
            <div class="demo-card-content">
              <span class="demo-card-title">User Demo</span>
              <span class="demo-card-email">user@demo.com</span>
            </div>
          </button>
        </div>

        <p class="auth-footer">
          Don't have an account?
          <router-link to="/register" class="auth-link">Create one now</router-link>
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
  background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
  padding: 1.5rem;
  position: relative;
  overflow: hidden;
}

/* Animated background shapes */
.bg-shapes {
  position: absolute;
  inset: 0;
  overflow: hidden;
  pointer-events: none;
}

.shape {
  position: absolute;
  border-radius: 50%;
  filter: blur(60px);
  opacity: 0.5;
  animation: float 20s infinite ease-in-out;
}

.shape-1 {
  width: 400px;
  height: 400px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  top: -100px;
  left: -100px;
  animation-delay: 0s;
}

.shape-2 {
  width: 300px;
  height: 300px;
  background: linear-gradient(135deg, #f093fb, #f5576c);
  bottom: -50px;
  right: -50px;
  animation-delay: -5s;
}

.shape-3 {
  width: 250px;
  height: 250px;
  background: linear-gradient(135deg, #4facfe, #00f2fe);
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  animation-delay: -10s;
}

@keyframes float {
  0%, 100% { transform: translate(0, 0) scale(1); }
  25% { transform: translate(30px, -30px) scale(1.1); }
  50% { transform: translate(-20px, 20px) scale(0.95); }
  75% { transform: translate(20px, 30px) scale(1.05); }
}

.auth-container {
  width: 100%;
  max-width: 440px;
  position: relative;
  z-index: 1;
}

/* Glassmorphism card */
.auth-card {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-radius: 24px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  padding: 2.5rem;
  box-shadow: 
    0 8px 32px rgba(0, 0, 0, 0.3),
    inset 0 0 0 1px rgba(255, 255, 255, 0.1);
}

/* Brand */
.brand {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  margin-bottom: 0.5rem;
}

.brand-icon {
  width: 48px;
  height: 48px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
}

.brand-icon svg {
  width: 28px;
  height: 28px;
  color: white;
}

.brand-name {
  font-size: 1.75rem;
  font-weight: 700;
  color: white;
  letter-spacing: -0.5px;
}

.brand-name span {
  background: linear-gradient(135deg, #667eea, #764ba2);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.auth-subtitle {
  text-align: center;
  color: rgba(255, 255, 255, 0.7);
  margin-bottom: 1.5rem;
  font-size: 0.95rem;
}

/* Role cards */
.role-cards {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.75rem;
  margin-bottom: 1.5rem;
}

.role-card {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.875rem;
  background: rgba(255, 255, 255, 0.08);
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.role-icon-wrapper {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.role-icon-wrapper svg {
  width: 18px;
  height: 18px;
}

.role-icon-user {
  background: linear-gradient(135deg, #10b981, #059669);
  color: white;
}

.role-icon-admin {
  background: linear-gradient(135deg, #8b5cf6, #7c3aed);
  color: white;
}

.role-text {
  display: flex;
  flex-direction: column;
}

.role-title {
  font-weight: 600;
  color: white;
  font-size: 0.875rem;
}

.role-desc {
  color: rgba(255, 255, 255, 0.6);
  font-size: 0.75rem;
}

/* Alerts */
.alert {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.875rem 1rem;
  border-radius: 12px;
  margin-bottom: 1rem;
  font-size: 0.875rem;
}

.alert-icon {
  width: 20px;
  height: 20px;
  flex-shrink: 0;
}

.alert-error {
  background: rgba(239, 68, 68, 0.2);
  border: 1px solid rgba(239, 68, 68, 0.3);
  color: #fca5a5;
}

.alert-success {
  background: rgba(34, 197, 94, 0.2);
  border: 1px solid rgba(34, 197, 94, 0.3);
  color: #86efac;
}

/* Form */
.auth-form {
  margin-top: 0;
}

.form-group {
  margin-bottom: 1.25rem;
}

.form-label {
  display: block;
  color: rgba(255, 255, 255, 0.9);
  font-size: 0.875rem;
  font-weight: 500;
  margin-bottom: 0.5rem;
}

.input-wrapper {
  position: relative;
}

.input-icon {
  position: absolute;
  left: 1rem;
  top: 50%;
  transform: translateY(-50%);
  width: 20px;
  height: 20px;
  color: rgba(255, 255, 255, 0.4);
  pointer-events: none;
  transition: color 0.2s;
}

.input-wrapper:focus-within .input-icon {
  color: #667eea;
}

.form-input {
  width: 100%;
  padding: 0.875rem 1rem 0.875rem 3rem;
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 12px;
  color: white;
  font-size: 0.95rem;
  transition: all 0.2s;
}

.form-input::placeholder {
  color: rgba(255, 255, 255, 0.4);
}

.form-input:focus {
  outline: none;
  border-color: #667eea;
  background: rgba(255, 255, 255, 0.12);
  box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.2);
}

/* Primary button */
.btn-primary {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  width: 100%;
  padding: 1rem 1.5rem;
  background: linear-gradient(135deg, #667eea, #764ba2);
  border: none;
  border-radius: 12px;
  color: white;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
  margin-top: 0.5rem;
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.5);
}

.btn-primary:active:not(:disabled) {
  transform: translateY(0);
}

.btn-primary:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.btn-arrow {
  width: 20px;
  height: 20px;
  transition: transform 0.2s;
}

.btn-primary:hover .btn-arrow {
  transform: translateX(4px);
}

.btn-loader {
  width: 20px;
  height: 20px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Divider */
.auth-divider {
  display: flex;
  align-items: center;
  margin: 1.75rem 0 1.25rem;
  color: rgba(255, 255, 255, 0.5);
  font-size: 0.75rem;
}

.auth-divider::before,
.auth-divider::after {
  content: '';
  flex: 1;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
}

.auth-divider span {
  padding: 0 1rem;
  text-transform: uppercase;
  letter-spacing: 0.1em;
}

/* Demo cards */
.demo-buttons {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.75rem;
}

.demo-card {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s;
  text-align: left;
}

.demo-card:hover:not(:disabled) {
  background: rgba(255, 255, 255, 0.1);
  transform: translateY(-2px);
}

.demo-card:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.demo-card-icon {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.demo-card-icon svg {
  width: 20px;
  height: 20px;
  color: white;
}

.demo-admin .demo-card-icon {
  background: linear-gradient(135deg, #8b5cf6, #7c3aed);
  box-shadow: 0 4px 12px rgba(139, 92, 246, 0.3);
}

.demo-user .demo-card-icon {
  background: linear-gradient(135deg, #10b981, #059669);
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
}

.demo-card-content {
  display: flex;
  flex-direction: column;
}

.demo-card-title {
  font-weight: 600;
  color: white;
  font-size: 0.875rem;
}

.demo-card-email {
  color: rgba(255, 255, 255, 0.5);
  font-size: 0.75rem;
}

/* Footer */
.auth-footer {
  text-align: center;
  margin-top: 1.75rem;
  font-size: 0.875rem;
  color: rgba(255, 255, 255, 0.6);
}

.auth-link {
  color: #667eea;
  text-decoration: none;
  font-weight: 600;
  transition: color 0.2s;
}

.auth-link:hover {
  color: #818cf8;
  text-decoration: underline;
}

/* Responsive */
@media (max-width: 480px) {
  .auth-card {
    padding: 1.75rem;
    border-radius: 20px;
  }
  
  .role-cards {
    grid-template-columns: 1fr;
  }
  
  .demo-buttons {
    grid-template-columns: 1fr;
  }
  
  .brand-name {
    font-size: 1.5rem;
  }
}
</style>
