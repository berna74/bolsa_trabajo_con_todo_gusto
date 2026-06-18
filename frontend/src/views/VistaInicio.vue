<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '../services/clienteApi'
import femalePlaceholder from '../assets/female_placeholder_baja.png'
import malePlaceholder from '../assets/male_placeholder_baja.png'

const loading = ref(true)
const error = ref('')
const groups = ref([])
const route = useRoute()
const router = useRouter()
const selectedRubro = ref(null)
const selectedCity = ref('all')

const busquedaTrabajador = computed({
  get() {
    return typeof route.query.q === 'string' ? route.query.q : ''
  },
  set(value) {
    const nextValue = value.trim()
    const nextQuery = { ...route.query }

    if (nextValue) {
      nextQuery.q = nextValue
    } else {
      delete nextQuery.q
    }

    router.replace({ path: route.path, query: nextQuery })
  },
})

const terminoBusqueda = computed(() => {
  return typeof route.query.q === 'string' ? route.query.q.trim().toLowerCase() : ''
})

const gruposOrdenados = computed(() => {
  return [...groups.value].sort((a, b) => {
    const countDiff = (b.workers?.length || 0) - (a.workers?.length || 0)
    if (countDiff !== 0) {
      return countDiff
    }
    return a.rubro.localeCompare(b.rubro)
  })
})

const ciudadesDisponibles = computed(() => {
  const cities = new Set()
  for (const group of groups.value) {
    for (const worker of group.workers || []) {
      const city = (worker.city || '').trim()
      if (city) {
        cities.add(city)
      }
    }
  }
  return [...cities].sort((a, b) => a.localeCompare(b, 'es'))
})

const gruposFiltrados = computed(() => {
  let groups = gruposOrdenados.value
  
  // Filtrar por rubro seleccionado
  if (selectedRubro.value) {
    groups = groups.filter((g) => g.rubro === selectedRubro.value)
  }
  
  if (selectedCity.value !== 'all') {
    groups = groups
      .map((group) => ({
        ...group,
        workers: group.workers.filter((worker) => (worker.city || '').trim() === selectedCity.value),
      }))
      .filter((group) => group.workers.length > 0)
  }

  // Filtrar por búsqueda
  const term = terminoBusqueda.value
  if (!term) {
    return groups.map((group) => ({
      ...group,
      total: group.workers.length,
    }))
  }

  return groups
    .map((group) => {
      const workers = group.workers.filter((worker) => worker.full_name.toLowerCase().includes(term))
      return {
        ...group,
        workers,
        total: group.workers.length,
      }
    })
    .filter((group) => group.workers.length > 0)
})

const HOME_PREVIEW = 5

const gruposVistaPrevia = computed(() =>
  gruposFiltrados.value.map((group) => ({
    ...group,
    workers: group.workers.slice(0, HOME_PREVIEW),
  }))
)

function anclaRubro(rubro) {
  return `rubro-${rubro.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '')}`
}

function aliasRubro(rubro) {
  return rubro
    .normalize('NFD')
    .replace(/\p{Diacritic}/gu, '')
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/(^-|-$)/g, '')
}

function formatearEtiquetaRubro(rubro) {
  const value = (rubro || '').trim()
  if (!value) return ''
  const words = value.split(' ')
  const first = words[0]
  let plural
  if (/s$/i.test(first)) {
    plural = first
  } else if (/o$/i.test(first)) {
    plural = first + 's/as'
  } else if (/a$/i.test(first)) {
    plural = first + 's'
  } else {
    plural = first + 's'
  }
  return words.length > 1 ? `${plural} ${words.slice(1).join(' ')}` : plural
}

function sanearTelefono(phone) {
  return (phone || '').replace(/[^\d+]/g, '')
}

function enlaceWhatsApp(phone, name) {
  const cleanPhone = sanearTelefono(phone)
  if (!cleanPhone) {
    return ''
  }
  const message = encodeURIComponent(`Hola ${name}, vi tu perfil en ConTodoGusto y me gustaría contactarte.`)
  return `https://wa.me/${cleanPhone}?text=${message}`
}

function enlaceCorreo(email, name) {
  if (!email) {
    return ''
  }
  const subject = encodeURIComponent('Contacto laboral desde ConTodoGusto')
  const body = encodeURIComponent(`Hola ${name}, vi tu perfil y me gustaría conversar sobre una oportunidad laboral.`)
  return `mailto:${email}?subject=${subject}&body=${body}`
}

function fotoRespaldoTrabajador(worker) {
  return worker?.gender === 'mujer' ? femalePlaceholder : malePlaceholder
}

async function cargarTrabajadores() {
  loading.value = true
  error.value = ''
  try {
    const { data } = await api.get('/public/workers-by-role/')
    groups.value = data
  } catch {
    error.value = 'No se pudo cargar el listado de trabajadores.'
  } finally {
    loading.value = false
  }
}

onMounted(cargarTrabajadores)
</script>

<template>
  <section class="tarjeta panel-inicio">
    <div class="encabezado-inicio">
      <h2>Trabajadores registrados por rubro</h2>
      <label class="contenedor-busqueda-inicio" for="buscador-trabajador">
        <span class="prefijo-busqueda-inicio">Buscar trabajador/a...</span>
        <input
          id="buscador-trabajador"
          v-model="busquedaTrabajador"
          type="search"
          placeholder="Ej: Juan Perez"
          class="entrada-busqueda-inicio entrada-busqueda-interna"
        />
      </label>
      <select v-model="selectedRubro" class="selector-rubros" aria-label="Filtrar por rubro">
        <option :value="null">Todos los rubros</option>
        <option v-for="group in gruposOrdenados" :key="group.rubro" :value="group.rubro">
          {{ formatearEtiquetaRubro(group.rubro) }} ({{ group.workers.length }})
        </option>
      </select>
      <select v-model="selectedCity" class="selector-rubros" aria-label="Filtrar por ciudad">
        <option value="all">Todas las ciudades</option>
          <option v-for="city in ciudadesDisponibles" :key="city" :value="city">
          {{ city }}
        </option>
      </select>
    </div>

    <p v-if="loading">Cargando trabajadores...</p>
    <p v-else-if="error" class="texto-error">{{ error }}</p>

    <template v-else>
      <p v-if="!gruposFiltrados.length" class="estado-vacio">No hay trabajadores que coincidan con la búsqueda.</p>

      <div class="grilla-rubros">
        <article v-for="group in gruposVistaPrevia" :id="anclaRubro(group.rubro)" :key="group.rubro" class="tarjeta-rubro">
          <h3>
            <router-link class="enlace-rubro" :to="`/rubro/${aliasRubro(group.rubro)}`">
              {{ formatearEtiquetaRubro(group.rubro) }} ({{ group.total }})
            </router-link>
          </h3>
          <ul class="lista-trabajadores">
            <li v-for="worker in group.workers" :key="worker.id">
              <div class="fila-trabajador">
                <img
                  v-if="worker.personal_photo_url"
                  :src="worker.personal_photo_url"
                  :alt="`Foto de ${worker.full_name}`"
                  class="foto-trabajador"
                />
                <img
                  v-else
                  :src="fotoRespaldoTrabajador(worker)"
                  :alt="`Placeholder de chef para ${worker.full_name}`"
                  class="foto-trabajador foto-reemplazo"
                />
                <div class="metadatos-trabajador">
                  <router-link class="enlace-trabajador" :to="`/trabajador/${worker.id}`">
                    <strong>{{ worker.full_name }}</strong>
                  </router-link>
                  <span>{{ worker.city || 'Ciudad no indicada' }}</span>
                  <span>{{ worker.years_experience }} años de experiencia</span>
                  <span v-if="worker.availability">Disponibilidad: {{ worker.availability }}</span>
                  <div class="acciones-trabajador">
                    <a
                      v-if="enlaceWhatsApp(worker.phone, worker.full_name)"
                      :href="enlaceWhatsApp(worker.phone, worker.full_name)"
                      target="_blank"
                      rel="noopener noreferrer"
                      class="boton-contacto"
                      aria-label="Contactar por WhatsApp"
                      title="WhatsApp"
                    >
                      <svg class="icono-boton" viewBox="0 0 24 24" aria-hidden="true">
                        <path
                          d="M12 3a8.5 8.5 0 00-7.302 12.87L4 21l5.305-1.659A8.5 8.5 0 1012 3z"
                          fill="none"
                          stroke="currentColor"
                          stroke-width="1.8"
                          stroke-linecap="round"
                          stroke-linejoin="round"
                        />
                        <path
                          d="M9.2 9.8c.2-.4.5-.4.7-.4h.6c.2 0 .4.1.5.3l.5 1.1c.1.2 0 .4-.1.5l-.4.6c.5.9 1.2 1.5 2 2l.6-.4c.2-.1.4-.2.6-.1l1.1.5c.2.1.3.3.3.5v.6c0 .2 0 .5-.4.7-.7.3-1.5.3-2.2 0-2-.8-3.6-2.4-4.4-4.4-.3-.7-.3-1.5 0-2.2z"
                          fill="currentColor"
                        />
                      </svg>
                    </a>
                    <a
                      v-if="enlaceCorreo(worker.email, worker.full_name)"
                      :href="enlaceCorreo(worker.email, worker.full_name)"
                      class="boton-contacto"
                      aria-label="Contactar por Email"
                      title="Email"
                    >
                      <svg class="icono-boton" viewBox="0 0 24 24" aria-hidden="true">
                        <path
                          d="M4 6h16v12H4z"
                          fill="none"
                          stroke="currentColor"
                          stroke-width="1.8"
                          stroke-linejoin="round"
                        />
                        <path
                          d="M4 7l8 6 8-6"
                          fill="none"
                          stroke="currentColor"
                          stroke-width="1.8"
                          stroke-linecap="round"
                          stroke-linejoin="round"
                        />
                      </svg>
                    </a>
                  </div>
                </div>
              </div>
            </li>
          </ul>
          <router-link
            v-if="group.total > 5"
            class="ver-mas-rubro"
            :to="`/rubro/${aliasRubro(group.rubro)}`"
          >
            Ver los {{ group.total - 5 }} restantes &rarr;
          </router-link>
        </article>
      </div>
    </template>
  </section>
</template>
