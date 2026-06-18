import axios from 'axios'
import { defineStore } from 'pinia'
import { API_BASE_URL } from '../services/configuracion'

const TOKEN_KEY = 'ctg_access_token'
const REFRESH_KEY = 'ctg_refresh_token'
const APP_ROLE_KEY = 'ctg_app_role'

let refreshRequest = null

function leerCargaToken(token) {
  if (!token) {
    return null
  }

  const [, payload] = token.split('.')
  if (!payload) {
    return null
  }

  try {
    return JSON.parse(atob(payload.replace(/-/g, '+').replace(/_/g, '/')))
  } catch {
    return null
  }
}

function estaTokenVencido(token) {
  const payload = leerCargaToken(token)
  if (!payload?.exp) {
    return true
  }

  return payload.exp * 1000 <= Date.now()
}

export function puedeVerFichas(rolAplicacion) {
  return rolAplicacion === 'superadministrador' || rolAplicacion === 'administrador'
}

export const useTiendaAutenticacion = defineStore('autenticacion', {
  state: () => ({
    tokenAcceso: localStorage.getItem(TOKEN_KEY) || '',
    tokenActualizacion: localStorage.getItem(REFRESH_KEY) || '',
    rolAplicacion: localStorage.getItem(APP_ROLE_KEY) || '',
  }),

  getters: {
    sesionActiva: (state) => Boolean(state.tokenAcceso),
    tieneTokenActualizacion: (state) => Boolean(state.tokenActualizacion),
    puedeVerFichas: (state) => puedeVerFichas(state.rolAplicacion),
    tieneTokenAccesoVigente: (state) => Boolean(state.tokenAcceso) && !estaTokenVencido(state.tokenAcceso),
  },

  actions: {
    guardarTokens(tokenAcceso, tokenActualizacion = this.tokenActualizacion) {
      this.tokenAcceso = tokenAcceso || ''
      this.tokenActualizacion = tokenActualizacion || ''

      if (this.tokenAcceso) {
        localStorage.setItem(TOKEN_KEY, this.tokenAcceso)
      } else {
        localStorage.removeItem(TOKEN_KEY)
      }

      if (this.tokenActualizacion) {
        localStorage.setItem(REFRESH_KEY, this.tokenActualizacion)
      } else {
        localStorage.removeItem(REFRESH_KEY)
      }
    },

    guardarRolAplicacion(rolAplicacion) {
      this.rolAplicacion = rolAplicacion || ''

      if (this.rolAplicacion) {
        localStorage.setItem(APP_ROLE_KEY, this.rolAplicacion)
      } else {
        localStorage.removeItem(APP_ROLE_KEY)
      }
    },

    limpiarAutenticacion() {
      this.tokenAcceso = ''
      this.tokenActualizacion = ''
      this.rolAplicacion = ''
      localStorage.removeItem(TOKEN_KEY)
      localStorage.removeItem(REFRESH_KEY)
      localStorage.removeItem(APP_ROLE_KEY)
    },

    async iniciarSesion(credentials) {
      const { data } = await axios.post(`${API_BASE_URL}/auth/login/`, credentials)
      this.guardarTokens(data.access, data.refresh)
      return data
    },

    async refrescarTokenAcceso() {
      if (!this.tokenActualizacion) {
        throw new Error('No refresh token available')
      }

      if (!refreshRequest) {
        refreshRequest = axios
          .post(`${API_BASE_URL}/auth/refresh/`, { refresh: this.tokenActualizacion })
          .then(({ data }) => {
            this.guardarTokens(data.access, data.refresh || this.tokenActualizacion)
            return this.tokenAcceso
          })
          .catch((error) => {
            this.limpiarAutenticacion()
            throw error
          })
          .finally(() => {
            refreshRequest = null
          })
      }

      return refreshRequest
    },

    async revocarTokenActualizacion() {
      if (!this.tokenActualizacion) {
        return
      }

      await axios.post(`${API_BASE_URL}/auth/logout/`, { refresh: this.tokenActualizacion }, {
        headers: this.tokenAcceso
          ? { Authorization: `Bearer ${this.tokenAcceso}` }
          : undefined,
      })
    },

    async asegurarSesion() {
      if (this.tieneTokenAccesoVigente) {
        return true
      }

      if (!this.tokenActualizacion) {
        this.limpiarAutenticacion()
        return false
      }

      try {
        await this.refrescarTokenAcceso()
        return true
      } catch {
        return false
      }
    },

    cerrarSesion() {
      this.limpiarAutenticacion()
    },
  },
})
