const TOKEN_KEY = 'ctg_access_token'
const REFRESH_KEY = 'ctg_refresh_token'
const APP_ROLE_KEY = 'ctg_app_role'

export function saveTokens(access, refresh) {
  localStorage.setItem(TOKEN_KEY, access)
  localStorage.setItem(REFRESH_KEY, refresh)
}

export function getToken() {
  return localStorage.getItem(TOKEN_KEY)
}

export function hasToken() {
  return Boolean(getToken())
}

export function saveAppRole(appRole) {
  if (appRole) {
    localStorage.setItem(APP_ROLE_KEY, appRole)
    return
  }
  localStorage.removeItem(APP_ROLE_KEY)
}

export function getAppRole() {
  return localStorage.getItem(APP_ROLE_KEY)
}

export function canAccessFichas(appRole) {
  return appRole === 'superadministrador' || appRole === 'administrador'
}

export function clearAuth() {
  localStorage.removeItem(TOKEN_KEY)
  localStorage.removeItem(REFRESH_KEY)
  localStorage.removeItem(APP_ROLE_KEY)
}
