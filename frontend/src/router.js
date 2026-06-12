import { createRouter, createWebHistory } from 'vue-router'
import AuthView from './views/AuthView.vue'
import DashboardView from './views/DashboardView.vue'
import HomeView from './views/HomeView.vue'
import RoleView from './views/RoleView.vue'
import WorkerProfileView from './views/WorkerProfileView.vue'
import { hasToken } from './services/auth'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: HomeView },
    { path: '/rubro/:slug', component: RoleView },
    { path: '/trabajador/:id', component: WorkerProfileView },
    { path: '/auth', component: AuthView },
    { path: '/dashboard', component: DashboardView, meta: { requiresAuth: true } },
  ],
})

router.beforeEach((to) => {
  if (to.meta.requiresAuth && !hasToken()) {
    return '/auth'
  }
  if (to.path === '/auth' && hasToken()) {
    return '/dashboard'
  }
})

export default router
