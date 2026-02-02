import { ref } from 'vue'

const toasts = ref([])
let toastId = 0

export function useToast() {
  function addToast(message, type = 'info', duration = 4000) {
    const id = ++toastId
    toasts.value.push({ id, message, type })
    
    if (duration > 0) {
      setTimeout(() => {
        removeToast(id)
      }, duration)
    }
    
    return id
  }

  function removeToast(id) {
    const index = toasts.value.findIndex(t => t.id === id)
    if (index > -1) {
      toasts.value.splice(index, 1)
    }
  }

  function success(message, duration = 4000) {
    return addToast(message, 'success', duration)
  }

  function error(message, duration = 5000) {
    return addToast(message, 'error', duration)
  }

  function info(message, duration = 4000) {
    return addToast(message, 'info', duration)
  }

  return {
    toasts,
    addToast,
    removeToast,
    success,
    error,
    info
  }
}
