import axios from 'axios'
import { API_BASE_URL } from './configuracion'
import { useTiendaAutenticacion } from '../stores/autenticacion'
import { pinia } from '../stores/instanciaPinia'

const api = axios.create({
  baseURL: API_BASE_URL,
})

api.interceptors.request.use((config) => {
  const tiendaAutenticacion = useTiendaAutenticacion(pinia)
  const token = tiendaAutenticacion.tokenAcceso
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const tiendaAutenticacion = useTiendaAutenticacion(pinia)
    const originalRequest = error.config
    const requestUrl = originalRequest?.url || ''
    const isAuthEndpoint = requestUrl.includes('/auth/login/') || requestUrl.includes('/auth/register/')
    const isRefreshRequest = requestUrl.includes('/auth/refresh/')

    if (error.response?.status === 401 && !originalRequest?._retry && !isAuthEndpoint && !isRefreshRequest) {
      originalRequest._retry = true

      try {
        const accessToken = await tiendaAutenticacion.refrescarTokenAcceso()
        originalRequest.headers = originalRequest.headers || {}
        originalRequest.headers.Authorization = `Bearer ${accessToken}`
        return api(originalRequest)
      } catch {
        tiendaAutenticacion.cerrarSesion()
        if (window.location.pathname !== '/auth') {
          window.location.href = '/auth'
        }
      }
    }

    if (error.response?.status === 401 && isRefreshRequest) {
      tiendaAutenticacion.cerrarSesion()
      if (window.location.pathname !== '/auth') {
        window.location.href = '/auth'
      }
    }

    return Promise.reject(error)
  },
)

export default api
