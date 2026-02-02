import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue'),
    meta: { guest: true }
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('../views/Register.vue'),
    meta: { guest: true }
  },
  {
    path: '/',
    redirect: (to) => {
      const authStore = useAuthStore()
      return authStore.isAdmin ? '/admin' : '/dashboard'
    }
  },
  {
    path: '/dashboard',
    name: 'UserDashboard',
    component: () => import('../views/UserDashboard.vue'),
    meta: { requiresAuth: true, role: 'user' }
  },
  {
    path: '/submit',
    name: 'SubmitFeedback',
    component: () => import('../views/SubmitFeedback.vue'),
    meta: { requiresAuth: true, role: 'user' }
  },
  {
    path: '/admin',
    name: 'AdminDashboard',
    component: () => import('../views/AdminDashboard.vue'),
    meta: { requiresAuth: true, role: 'admin' }
  },
  {
    path: '/admin/analytics',
    name: 'Analytics',
    component: () => import('../views/Analytics.vue'),
    meta: { requiresAuth: true, role: 'admin' }
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next('/login')
  } else if (to.meta.guest && authStore.isAuthenticated) {
    next('/')
  } else if (to.meta.role === 'admin' && !authStore.isAdmin) {
    next('/dashboard')
  } else if (to.meta.role === 'user' && authStore.isAdmin) {
    next('/admin')
  } else {
    next()
  }
})

export default router
