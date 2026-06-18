<script setup>
import { onMounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import brandLogo from './views/logo3.png'
import RubrosSidebar from './components/RubrosSidebar.vue'
import api from './services/api'
import { canAccessFichas, getAppRole, hasToken, saveAppRole } from './services/auth'

const route = useRoute()
const canSeeFichasLink = ref(false)

async function refreshFichasAccess() {
  if (!hasToken()) {
    canSeeFichasLink.value = false
    saveAppRole('')
    return
  }

  const cachedRole = getAppRole()
  if (cachedRole) {
    canSeeFichasLink.value = canAccessFichas(cachedRole)
    return
  }

  try {
    const { data } = await api.get('/auth/me/')
    const appRole = data?.app_role || ''
    saveAppRole(appRole)
    canSeeFichasLink.value = canAccessFichas(appRole)
  } catch {
    canSeeFichasLink.value = false
  }
}

onMounted(refreshFichasAccess)
watch(() => route.fullPath, refreshFichasAccess)
</script>

<template>
  <div class="app-shell">
    <div class="right-panel">
      <header>
        <div class="top-strip">
          <span class="top-strip-title">
            <span class="top-strip-brand">
              <span class="top-strip-brand-con">Con</span><span class="top-strip-brand-todo">Todo</span><span class="top-strip-brand-gusto">Gusto</span>
            </span>
            | Bolsa de <span class="top-strip-highlight">trabajo</span> gastronómica
          </span>
          <nav class="site-nav" aria-label="Navegación principal">
            <router-link to="/">Inicio</router-link>
            <router-link v-if="canSeeFichasLink" to="/fichas">Fichas</router-link>
            <router-link to="/auth" class="nav-icon-link">
              <svg class="btn-icon" viewBox="0 0 24 24" aria-hidden="true">
                <path
                  d="M12 4a4 4 0 100 8 4 4 0 000-8zm0 10c-3.314 0-6 2.015-6 4.5V20h12v-1.5c0-2.485-2.686-4.5-6-4.5zM16 8h4m-2-2v4"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="1.8"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                />
              </svg>
              Ingresar / Registrarse
            </router-link>
            <router-link to="/dashboard">Mi perfil</router-link>
          </nav>
        </div>
        <div class="brand-bar">
          <router-link to="/" class="brand-bar-logo" aria-label="Ir al inicio">
            <img :src="brandLogo" alt="Logo Con Todo Gusto" class="brand-logo" />
          </router-link>
          <RubrosSidebar />
        </div>
      </header>
      <main class="main-content">
        <router-view />
      </main>
    </div>
  </div>
</template>
