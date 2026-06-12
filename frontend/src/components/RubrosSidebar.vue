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
  if (/os$/i.test(value)) return `${value}/as`
  if (/as$/i.test(value)) return `${value}/os`
  if (/o$/i.test(value)) return `${value.slice(0, -1)}os/as`
  if (/a$/i.test(value)) return `${value.slice(0, -1)}as/os`
  if (/s$/i.test(value)) return value
  if (/[aeiou]$/i.test(value)) return `${value}s`
  return `${value}es`
}

async function fetchGroups() {
  try {
    const { data } = await api.get('/public/workers-by-role/')
    groups.value = data.sort((a, b) => {
      const diff = (b.workers?.length || 0) - (a.workers?.length || 0)
      return diff !== 0 ? diff : a.rubro.localeCompare(b.rubro)
    })
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
  </nav>
</template>
