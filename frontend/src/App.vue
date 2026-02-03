<template>
  <div id="app">
    <ToastContainer />
    <nav class="navbar" v-if="authStore.isAuthenticated">
      <div class="container navbar-content">
        <router-link to="/" class="navbar-brand">
          <div class="brand-logo">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
            </svg>
          </div>
          <span class="brand-text">Feedback<span class="brand-accent">Hub</span></span>
        </router-link>
        <div class="navbar-nav">
          <template v-if="authStore.isAdmin">
            <router-link to="/admin" class="nav-link">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="18" height="18">
                <rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/>
                <rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/>
              </svg>
              Dashboard
            </router-link>
            <router-link to="/admin/analytics" class="nav-link">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="18" height="18">
                <line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/>
              </svg>
              Analytics
            </router-link>
          </template>
          <template v-else>
            <router-link to="/dashboard" class="nav-link">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="18" height="18">
                <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
              </svg>
              My Feedback
            </router-link>
            <router-link to="/submit" class="nav-link nav-link-primary">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="18" height="18">
                <line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/>
              </svg>
              Submit
            </router-link>
          </template>
          <div class="nav-divider"></div>
          <button @click="logout" class="btn-logout">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="18" height="18">
              <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/>
              <polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/>
            </svg>
            Logout
          </button>
        </div>
      </div>
    </nav>
    <main>
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { useAuthStore } from './stores/auth'
import { useRouter } from 'vue-router'
import ToastContainer from './components/ToastContainer.vue'

const authStore = useAuthStore()
const router = useRouter()

const logout = () => {
  authStore.logout()
  router.push('/login')
}
</script>

<style scoped>
.navbar {
  background: white;
  border-bottom: 1px solid #e5e7eb;
  padding: 0.75rem 0;
  position: sticky;
  top: 0;
  z-index: 100;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.navbar-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.navbar-brand {
  display: flex;
  align-items: center;
  gap: 0.625rem;
  text-decoration: none;
}

.brand-logo {
  width: 36px;
  height: 36px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
}

.brand-logo svg {
  width: 20px;
  height: 20px;
}

.brand-text {
  font-size: 1.25rem;
  font-weight: 800;
  color: #1f2937;
  letter-spacing: -0.5px;
}

.brand-accent {
  background: linear-gradient(135deg, #667eea, #764ba2);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.navbar-nav {
  display: flex;
  align-items: center;
  gap: 0.375rem;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #6b7280;
  text-decoration: none;
  font-weight: 500;
  font-size: 0.875rem;
  padding: 0.5rem 0.875rem;
  border-radius: 8px;
  transition: all 0.2s;
}

.nav-link:hover {
  color: #4f46e5;
  background: #eef2ff;
}

.nav-link.router-link-active {
  color: #4f46e5;
  background: #eef2ff;
}

.nav-link-primary {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white !important;
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
}

.nav-link-primary:hover {
  background: linear-gradient(135deg, #5a6fd6, #6a4190);
  color: white !important;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.nav-divider {
  width: 1px;
  height: 24px;
  background: #e5e7eb;
  margin: 0 0.5rem;
}

.btn-logout {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #6b7280;
  font-weight: 500;
  font-size: 0.875rem;
  padding: 0.5rem 0.875rem;
  border-radius: 8px;
  border: none;
  background: transparent;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-logout:hover {
  color: #dc2626;
  background: #fef2f2;
}

@media (max-width: 768px) {
  .navbar-nav {
    gap: 0.25rem;
  }
  
  .nav-link span,
  .btn-logout span {
    display: none;
  }
  
  .nav-link,
  .btn-logout {
    padding: 0.5rem;
  }
  
  .nav-divider {
    display: none;
  }
}
</style>
