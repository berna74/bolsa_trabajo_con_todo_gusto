<script setup>
import { onMounted, ref } from 'vue'
import api from '../services/api'

const groups = ref([])

function rubroSlug(rubro) {
  return rubro
    .normalize('NFD')
    .replace(/\p{Diacritic}/gu, '')
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/(^-|-$)/g, '')
}

function formatRubroLabel(rubro) {
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
  <nav class="rubros-header-nav" aria-label="Rubros">
    <router-link
      v-for="group in groups"
      :key="group.rubro"
      :to="`/rubro/${rubroSlug(group.rubro)}`"
      class="rubros-header-link"
    >
      <span class="rubros-header-link-name">{{ formatRubroLabel(group.rubro) }}</span>
      <span class="rubros-header-link-count">{{ group.workers.length }}</span>
    </router-link>
    <router-link to="/" class="rubros-header-link">
      <span class="rubros-header-link-name">Todos</span>
    </router-link>
  </nav>
</template>
