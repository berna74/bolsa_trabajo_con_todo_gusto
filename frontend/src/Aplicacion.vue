<script setup>
import { computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import brandLogo from './views/logo3.png'
import BarraRubros from './components/BarraRubros.vue'
import api from './services/clienteApi'
import { useTiendaAutenticacion, puedeVerFichas } from './stores/autenticacion'

const route = useRoute()
const tiendaAutenticacion = useTiendaAutenticacion()
const puedeVerFichasEnNavegacion = computed(() => puedeVerFichas(tiendaAutenticacion.rolAplicacion))

async function actualizarAccesoFichas() {
  if (!(await tiendaAutenticacion.asegurarSesion())) {
    tiendaAutenticacion.guardarRolAplicacion('')
    return
  }

  const cachedRole = tiendaAutenticacion.rolAplicacion
  if (cachedRole) {
    return
  }

  try {
    const { data } = await api.get('/auth/me/')
    tiendaAutenticacion.guardarRolAplicacion(data?.app_role || '')
  } catch {
    tiendaAutenticacion.guardarRolAplicacion('')
  }
}

onMounted(actualizarAccesoFichas)
watch(() => route.fullPath, actualizarAccesoFichas)
</script>

<template>
  <div class="envoltorio-app">
    <div class="panel-derecho">
      <header>
        <div class="franja-superior">
          <span class="titulo-franja-superior">
            <span class="marca-franja-superior">
              <span class="marca-con">Con</span><span class="marca-todo">Todo</span><span class="marca-gusto">Gusto</span>
            </span>
            | Bolsa de <span class="resalte-franja">trabajo</span> gastronómica
          </span>
          <nav class="navegacion-principal" aria-label="Navegación principal">
            <router-link to="/">Inicio</router-link>
            <router-link v-if="puedeVerFichasEnNavegacion" to="/fichas">Fichas</router-link>
            <router-link to="/auth" class="enlace-icono-nav">
              <svg class="icono-boton" viewBox="0 0 24 24" aria-hidden="true">
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
            <router-link to="/tablero">Mi perfil</router-link>
          </nav>
        </div>
        <div class="barra-marca">
          <router-link to="/" class="enlace-logo" aria-label="Ir al inicio">
            <img :src="brandLogo" alt="Logo Con Todo Gusto" class="brand-logo" />
          </router-link>
          <BarraRubros />
        </div>
      </header>
      <main class="contenido-principal">
        <router-view />
      </main>
    </div>
  </div>
</template>
