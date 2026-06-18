import { createRouter, createWebHistory } from 'vue-router'
import VistaIngreso from './views/VistaIngreso.vue'
import VistaTablero from './views/VistaTablero.vue'
import VistaFichas from './views/VistaFichas.vue'
import VistaInicio from './views/VistaInicio.vue'
import VistaRubro from './views/VistaRubro.vue'
import VistaPerfilTrabajador from './views/VistaPerfilTrabajador.vue'
import api from './services/clienteApi'
import { puedeVerFichas, useTiendaAutenticacion } from './stores/autenticacion'
import { pinia } from './stores/instanciaPinia'

async function resolverRolAplicacionActual() {
  const tiendaAutenticacion = useTiendaAutenticacion(pinia)
  const cachedRole = tiendaAutenticacion.rolAplicacion
  if (cachedRole) {
    return cachedRole
  }

  try {
    const { data } = await api.get('/auth/me/')
    tiendaAutenticacion.guardarRolAplicacion(data?.app_role || '')
    return data?.app_role || ''
  } catch {
    tiendaAutenticacion.guardarRolAplicacion('')
    return ''
  }
}

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: VistaInicio },
    { path: '/rubro/:slug', component: VistaRubro },
    { path: '/trabajador/:id', component: VistaPerfilTrabajador },
    { path: '/auth', component: VistaIngreso },
    { path: '/tablero', component: VistaTablero, meta: { requiresAuth: true } },
    { path: '/fichas', component: VistaFichas, meta: { requiresAuth: true } },
  ],
})

router.beforeEach(async (to) => {
  const tiendaAutenticacion = useTiendaAutenticacion(pinia)

  if (to.meta.requiresAuth && !(await tiendaAutenticacion.asegurarSesion())) {
    return '/auth'
  }

  if (to.path === '/fichas') {
    return resolverRolAplicacionActual().then((appRole) => {
      if (!puedeVerFichas(appRole)) {
        return '/tablero'
      }
      return true
    })
  }

  if (to.path === '/auth' && (await tiendaAutenticacion.asegurarSesion())) {
    return '/tablero'
  }

  return true
})

export default router
