import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authApi } from '../api/client'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('token'))
  const user = ref(JSON.parse(localStorage.getItem('user') || 'null'))

  const isAuthenticated = computed(() => !!token.value)
  const isAdmin = computed(() => user.value?.role === 'admin')

  async function login(email, password) {
    const response = await authApi.login(email, password)
    token.value = response.data.access_token
    localStorage.setItem('token', token.value)
    
    // Fetch user info
    const userResponse = await authApi.getMe()
    user.value = userResponse.data
    localStorage.setItem('user', JSON.stringify(user.value))
    
    return user.value
  }

  async function register(email, password) {
    await authApi.register(email, password)
    return login(email, password)
  }

  function logout() {
    token.value = null
    user.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('user')
  }

  async function fetchUser() {
    if (!token.value) return null
    try {
      const response = await authApi.getMe()
      user.value = response.data
      localStorage.setItem('user', JSON.stringify(user.value))
      return user.value
    } catch (error) {
      logout()
      return null
    }
  }

  return {
    token,
    user,
    isAuthenticated,
    isAdmin,
    login,
    register,
    logout,
    fetchUser,
  }
})
