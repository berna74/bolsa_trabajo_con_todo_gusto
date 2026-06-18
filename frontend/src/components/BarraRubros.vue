<script setup>
import { onMounted, ref } from 'vue'
import api from '../services/clienteApi'

const groups = ref([])

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

async function fetchGroups() {
  try {
    const { data } = await api.get('/public/workers-by-role/')
    groups.value = data.sort((a, b) => a.rubro.localeCompare(b.rubro, 'es', { sensitivity: 'base' }))
  } catch {
    // silencioso: el sidebar es complementario
  }
}

onMounted(fetchGroups)
</script>

<template>
  <nav class="navegacion-rubros" aria-label="Rubros">
    <router-link
      v-for="group in groups"
      :key="group.rubro"
      :to="`/rubro/${aliasRubro(group.rubro)}`"
      class="enlace-rubro-encabezado"
    >
      <span class="nombre-rubro-encabezado">{{ formatearEtiquetaRubro(group.rubro) }}</span>
      <span class="contador-rubro-encabezado">{{ group.workers.length }}</span>
    </router-link>
    <router-link to="/" class="enlace-rubro-encabezado">
      <span class="nombre-rubro-encabezado">Todos</span>
    </router-link>
  </nav>
</template>
