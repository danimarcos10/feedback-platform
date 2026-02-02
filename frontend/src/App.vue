<template>
  <div id="app">
    <ToastContainer />
    <nav class="navbar" v-if="authStore.isAuthenticated">
      <div class="container navbar-content">
        <router-link to="/" class="navbar-brand">Feedback Platform</router-link>
        <div class="navbar-nav">
          <template v-if="authStore.isAdmin">
            <router-link to="/admin" class="nav-link">Dashboard</router-link>
            <router-link to="/admin/analytics" class="nav-link">Analytics</router-link>
          </template>
          <template v-else>
            <router-link to="/dashboard" class="nav-link">My Feedback</router-link>
            <router-link to="/submit" class="nav-link">Submit Feedback</router-link>
          </template>
          <button @click="logout" class="btn btn-outline">Logout</button>
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
