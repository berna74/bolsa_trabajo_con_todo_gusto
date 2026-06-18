<script setup>
import { computed, onMounted, ref } from 'vue'
import api from '../services/clienteApi'

const loading = ref(true)
const saving = ref(false)
const deletingId = ref(null)
const error = ref('')
const success = ref('')
const me = ref(null)

const rubros = ref([])
const fichas = ref([])

const rubroForm = ref({ name: '' })
const fichaForm = ref({ type: 'requisito', name: '', description: '', is_active: true })

const typeOptions = [
  { value: 'requisito', label: 'Requisito' },
  { value: 'habilidad', label: 'Habilidad' },
  { value: 'otro', label: 'Otro' },
]

const groupedFichas = computed(() => {
  const groups = {
    requisito: [],
    habilidad: [],
    otro: [],
  }

  for (const item of fichas.value) {
    if (groups[item.type]) {
      groups[item.type].push(item)
    }
  }

  return groups
})

const hasFichasAccess = computed(() => {
  const appRole = me.value?.app_role
  return appRole === 'superadministrador' || appRole === 'administrador'
})

function resetMessages() {
  error.value = ''
  success.value = ''
}

async function fetchInitialData() {
  loading.value = true
  resetMessages()

  try {
    const [meRes, rolesRes, fichasRes] = await Promise.all([
      api.get('/auth/me/'),
      api.get('/roles/'),
      api.get('/fichas/'),
    ])

    me.value = meRes.data
    rubros.value = rolesRes.data
    fichas.value = fichasRes.data
  } catch {
    error.value = 'No se pudo cargar la gestión de fichas.'
  } finally {
    loading.value = false
  }
}

async function createRubro() {
  if (!rubroForm.value.name.trim()) {
    return
  }

  saving.value = true
  resetMessages()

  try {
    const { data } = await api.post('/roles/', { name: rubroForm.value.name.trim() })
    rubros.value.push(data)
    rubros.value.sort((a, b) => a.name.localeCompare(b.name))
    rubroForm.value.name = ''
    success.value = 'Rubro creado correctamente.'
  } catch {
    error.value = 'No se pudo crear el rubro. Recordá que esta acción requiere administrador o superadministrador.'
  } finally {
    saving.value = false
  }
}

async function updateRubro(item) {
  saving.value = true
  resetMessages()

  try {
    const payload = { name: (item.edit_name || item.name).trim() }
    const { data } = await api.patch(`/roles/${item.id}/`, payload)
    item.name = data.name
    item.editing = false
    success.value = 'Rubro actualizado.'
  } catch {
    error.value = 'No se pudo actualizar el rubro.'
  } finally {
    saving.value = false
  }
}

async function deleteRubro(item) {
  deletingId.value = `rubro-${item.id}`
  resetMessages()

  try {
    await api.delete(`/roles/${item.id}/`)
    rubros.value = rubros.value.filter((r) => r.id !== item.id)
    success.value = 'Rubro eliminado.'
  } catch {
    error.value = 'No se pudo eliminar el rubro.'
  } finally {
    deletingId.value = null
  }
}

async function createFicha() {
  if (!fichaForm.value.name.trim()) {
    return
  }

  saving.value = true
  resetMessages()

  try {
    const payload = {
      type: fichaForm.value.type,
      name: fichaForm.value.name.trim(),
      description: fichaForm.value.description.trim(),
      is_active: fichaForm.value.is_active,
    }

    const { data } = await api.post('/fichas/', payload)
    fichas.value.push(data)
    fichas.value.sort((a, b) => `${a.type}-${a.name}`.localeCompare(`${b.type}-${b.name}`))
    fichaForm.value = { type: 'requisito', name: '', description: '', is_active: true }
    success.value = 'Ficha creada correctamente.'
  } catch {
    error.value = 'No se pudo crear la ficha. Recordá que esta acción requiere administrador o superadministrador.'
  } finally {
    saving.value = false
  }
}

async function updateFicha(item) {
  saving.value = true
  resetMessages()

  try {
    const payload = {
      type: item.edit_type ?? item.type,
      name: (item.edit_name ?? item.name).trim(),
      description: (item.edit_description ?? item.description ?? '').trim(),
      is_active: item.edit_is_active ?? item.is_active,
    }

    const { data } = await api.patch(`/fichas/${item.id}/`, payload)
    Object.assign(item, data, {
      editing: false,
      edit_type: undefined,
      edit_name: undefined,
      edit_description: undefined,
      edit_is_active: undefined,
    })
    success.value = 'Ficha actualizada.'
  } catch {
    error.value = 'No se pudo actualizar la ficha.'
  } finally {
    saving.value = false
  }
}

async function deleteFicha(item) {
  deletingId.value = `ficha-${item.id}`
  resetMessages()

  try {
    await api.delete(`/fichas/${item.id}/`)
    fichas.value = fichas.value.filter((f) => f.id !== item.id)
    success.value = 'Ficha eliminada.'
  } catch {
    error.value = 'No se pudo eliminar la ficha.'
  } finally {
    deletingId.value = null
  }
}

function beginEditRubro(item) {
  item.editing = true
  item.edit_name = item.name
}

function beginEditFicha(item) {
  item.editing = true
  item.edit_type = item.type
  item.edit_name = item.name
  item.edit_description = item.description || ''
  item.edit_is_active = item.is_active
}

onMounted(fetchInitialData)
</script>

<template>
  <section class="tarjeta">
    <h2>Fichas</h2>
    <p class="muted-text">Gestión de rubros, requisitos, habilidades y demás categorías.</p>

    <p v-if="loading">Cargando gestión de fichas...</p>

    <template v-else>
      <p v-if="!hasFichasAccess" class="texto-error">
        Esta pantalla es solo para superadministradores y administradores.
      </p>

      <template v-else>
        <p v-if="error" class="texto-error">{{ error }}</p>
        <p v-if="success" class="ok-text">{{ success }}</p>

        <article class="inline-card">
          <h3>Nuevo Rubro</h3>
          <form class="grilla-formulario" @submit.prevent="createRubro">
            <label>
              Nombre del rubro
              <input v-model="rubroForm.name" required placeholder="Ej: Ayudantes de cocina" />
            </label>
            <button class="boton-principal" type="submit" :disabled="saving">Crear rubro</button>
          </form>

          <ul class="inline-list">
            <li v-for="item in rubros" :key="item.id" class="inline-item">
              <template v-if="item.editing">
                <input v-model="item.edit_name" />
                <button class="boton-secundario" @click="updateRubro(item)" :disabled="saving">Guardar</button>
                <button class="ghost-btn" @click="item.editing = false">Cancelar</button>
              </template>
              <template v-else>
                <span>{{ item.name }}</span>
                <button class="boton-secundario" @click="beginEditRubro(item)">Editar</button>
                <button class="ghost-btn" @click="deleteRubro(item)" :disabled="deletingId === `rubro-${item.id}`">Eliminar</button>
              </template>
            </li>
          </ul>
        </article>

        <article class="inline-card">
          <h3>Nueva Ficha</h3>
          <form class="grilla-formulario" @submit.prevent="createFicha">
            <label>
              Tipo
              <select v-model="fichaForm.type">
                <option v-for="opt in typeOptions" :key="opt.value" :value="opt.value">{{ opt.label }}</option>
              </select>
            </label>
            <label>
              Nombre
              <input v-model="fichaForm.name" required placeholder="Ej: Libreta sanitaria vigente" />
            </label>
            <label class="ancho-completo">
              Descripción
              <textarea v-model="fichaForm.description" rows="2"></textarea>
            </label>
            <label class="etiqueta-checkbox">
              <input v-model="fichaForm.is_active" type="checkbox" />
              Activa
            </label>
            <button class="boton-principal" type="submit" :disabled="saving">Crear ficha</button>
          </form>

          <div class="fichas-grid">
            <section class="fichas-col">
              <h4>Requisitos</h4>
              <ul class="inline-list">
                <li v-for="item in groupedFichas.requisito" :key="item.id" class="inline-item ficha-item">
                  <template v-if="item.editing">
                    <input v-model="item.edit_name" />
                    <textarea v-model="item.edit_description" rows="2"></textarea>
                    <label class="etiqueta-checkbox"><input v-model="item.edit_is_active" type="checkbox" /> Activa</label>
                    <div class="item-actions">
                      <button class="boton-secundario" @click="updateFicha(item)" :disabled="saving">Guardar</button>
                      <button class="ghost-btn" @click="item.editing = false">Cancelar</button>
                    </div>
                  </template>
                  <template v-else>
                    <strong>{{ item.name }}</strong>
                    <p>{{ item.description || 'Sin descripción' }}</p>
                    <small>{{ item.is_active ? 'Activa' : 'Inactiva' }}</small>
                    <div class="item-actions">
                      <button class="boton-secundario" @click="beginEditFicha(item)">Editar</button>
                      <button class="ghost-btn" @click="deleteFicha(item)" :disabled="deletingId === `ficha-${item.id}`">Eliminar</button>
                    </div>
                  </template>
                </li>
              </ul>
            </section>

            <section class="fichas-col">
              <h4>Habilidades</h4>
              <ul class="inline-list">
                <li v-for="item in groupedFichas.habilidad" :key="item.id" class="inline-item ficha-item">
                  <template v-if="item.editing">
                    <input v-model="item.edit_name" />
                    <textarea v-model="item.edit_description" rows="2"></textarea>
                    <label class="etiqueta-checkbox"><input v-model="item.edit_is_active" type="checkbox" /> Activa</label>
                    <div class="item-actions">
                      <button class="boton-secundario" @click="updateFicha(item)" :disabled="saving">Guardar</button>
                      <button class="ghost-btn" @click="item.editing = false">Cancelar</button>
                    </div>
                  </template>
                  <template v-else>
                    <strong>{{ item.name }}</strong>
                    <p>{{ item.description || 'Sin descripción' }}</p>
                    <small>{{ item.is_active ? 'Activa' : 'Inactiva' }}</small>
                    <div class="item-actions">
                      <button class="boton-secundario" @click="beginEditFicha(item)">Editar</button>
                      <button class="ghost-btn" @click="deleteFicha(item)" :disabled="deletingId === `ficha-${item.id}`">Eliminar</button>
                    </div>
                  </template>
                </li>
              </ul>
            </section>

            <section class="fichas-col">
              <h4>Otras</h4>
              <ul class="inline-list">
                <li v-for="item in groupedFichas.otro" :key="item.id" class="inline-item ficha-item">
                  <template v-if="item.editing">
                    <input v-model="item.edit_name" />
                    <textarea v-model="item.edit_description" rows="2"></textarea>
                    <label class="etiqueta-checkbox"><input v-model="item.edit_is_active" type="checkbox" /> Activa</label>
                    <div class="item-actions">
                      <button class="boton-secundario" @click="updateFicha(item)" :disabled="saving">Guardar</button>
                      <button class="ghost-btn" @click="item.editing = false">Cancelar</button>
                    </div>
                  </template>
                  <template v-else>
                    <strong>{{ item.name }}</strong>
                    <p>{{ item.description || 'Sin descripción' }}</p>
                    <small>{{ item.is_active ? 'Activa' : 'Inactiva' }}</small>
                    <div class="item-actions">
                      <button class="boton-secundario" @click="beginEditFicha(item)">Editar</button>
                      <button class="ghost-btn" @click="deleteFicha(item)" :disabled="deletingId === `ficha-${item.id}`">Eliminar</button>
                    </div>
                  </template>
                </li>
              </ul>
            </section>
          </div>
        </article>
      </template>
    </template>
  </section>
</template>

<style scoped>
.muted-text {
  margin-top: 0;
  color: #6f6a63;
}

.ok-text {
  color: #205f39;
  font-weight: 600;
}

.inline-card {
  margin-top: 1.25rem;
  padding: 1rem;
  border: 1px solid #e1d7c9;
  border-radius: 12px;
  background: #fff9f2;
}

.inline-list {
  list-style: none;
  margin: 1rem 0 0;
  padding: 0;
  display: grid;
  gap: 0.75rem;
}

.inline-item {
  display: grid;
  gap: 0.5rem;
  padding: 0.75rem;
  border: 1px solid #eadfce;
  border-radius: 10px;
  background: #fff;
}

.item-actions {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.fichas-grid {
  margin-top: 1rem;
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 1rem;
}

.fichas-col h4 {
  margin: 0;
}

.ficha-item p {
  margin: 0;
  color: #625648;
}

@media (max-width: 980px) {
  .fichas-grid {
    grid-template-columns: 1fr;
  }
}
</style>
