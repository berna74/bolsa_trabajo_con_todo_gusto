import { createRouter, createWebHistory } from 'vue-router'
import AuthView from './views/AuthView.vue'
import DashboardView from './views/DashboardView.vue'
import FichasAdminView from './views/FichasAdminView.vue'
import HomeView from './views/HomeView.vue'
import RoleView from './views/RoleView.vue'
import WorkerProfileView from './views/WorkerProfileView.vue'
import api from './services/api'
import { canAccessFichas, getAppRole, hasToken, saveAppRole } from './services/auth'

async function resolveCurrentAppRole() {
  const cachedRole = getAppRole()
  if (cachedRole) {
    return cachedRole
  }

  try {
    const { data } = await api.get('/auth/me/')
    saveAppRole(data?.app_role || '')
    return data?.app_role || ''
  } catch {
    return ''
  }
}

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: HomeView },
    { path: '/rubro/:slug', component: RoleView },
    { path: '/trabajador/:id', component: WorkerProfileView },
    { path: '/auth', component: AuthView },
    { path: '/dashboard', component: DashboardView, meta: { requiresAuth: true } },
    { path: '/fichas', component: FichasAdminView, meta: { requiresAuth: true } },
  ],
})

router.beforeEach((to) => {
  if (to.meta.requiresAuth && !hasToken()) {
    return '/auth'
  }

  if (to.path === '/fichas') {
    return resolveCurrentAppRole().then((appRole) => {
      if (!canAccessFichas(appRole)) {
        return '/dashboard'
      }
      return true
    })
  }

  if (to.path === '/auth' && hasToken()) {
    return '/dashboard'
  }
})

export default router
