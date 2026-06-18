<script setup>
import { onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import api from '../services/clienteApi'
import { limpiarAutenticacion } from '../services/autenticacion'
import ListaExperiencias from '../components/ListaExperiencias.vue'
import ListaReferencias from '../components/ListaReferencias.vue'

const router = useRouter()
const loading = ref(true)
const saving = ref(false)
const error = ref('')
const roles = ref([])
const selectedPhoto = ref(null)
const photoInputKey = ref(0)
const selectedPhotoPreview = ref('')

const profile = ref({
  first_name: '',
  last_name: '',
  gender: '',
  personal_photo_url: '',
  dni: '',
  birth_date: '',
  address: '',
  phone: '',
  city: '',
  social_networks: '',
  role: null,
  roles: [],
  role_name: '',
  role_names: [],
  years_experience: 0,
  availability: '',
  schedule: '',
  can_work_weekends_holidays: false,
  expected_salary: '',
  primary_education: '',
  secondary_education: '',
  tertiary_education: false,
  tertiary_details: '',
  gastro_courses: '',
  skills: '',
  has_sanitary_license: false,
  has_food_handling_cert: false,
  has_own_transport: false,
  bio: '',
  observations: '',
  experiences: [],
  references: [],
})

const experienceForm = ref({
  company_name: '',
  role: '',
  start_date: '',
  end_date: '',
  is_current: false,
  description: '',
})

const referenceForm = ref({
  full_name: '',
  company: '',
  relation: '',
  phone: '',
  email: '',
  note: '',
})

function alternarGeneroPerfil(gender, checked) {
  profile.value.gender = checked ? gender : ''
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

async function cargarPerfil() {
  loading.value = true
  try {
    const { data } = await api.get('/profile/')
    data.roles = Array.isArray(data.roles) && data.roles.length ? data.roles : (data.role ? [data.role] : [])
    // Merge con valores por defecto para asegurar todos los campos
    profile.value = {
      ...profile.value,
      ...data,
      roles: data.roles,
    }
  } catch {
    error.value = 'No se pudo cargar tu perfil.'
  } finally {
    loading.value = false
  }
}

async function cargarRubros() {
  try {
    const { data } = await api.get('/roles/')
    roles.value = data
  } catch {
    error.value = 'No se pudo cargar la lista de rubros.'
  }
}

async function guardarPerfil() {
  saving.value = true
  error.value = ''
  try {
    const payload = new FormData()
    payload.append('first_name', profile.value.first_name || '')
    payload.append('last_name', profile.value.last_name || '')
    payload.append('gender', profile.value.gender || '')
    payload.append('dni', profile.value.dni || '')
    payload.append('birth_date', profile.value.birth_date || '')
    payload.append('address', profile.value.address || '')
    payload.append('phone', profile.value.phone || '')
    payload.append('city', profile.value.city || '')
    payload.append('social_networks', profile.value.social_networks || '')
    payload.append('schedule', profile.value.schedule || '')
    payload.append('can_work_weekends_holidays', profile.value.can_work_weekends_holidays ? 'true' : 'false')
    payload.append('expected_salary', profile.value.expected_salary || '')
    payload.append('primary_education', profile.value.primary_education || '')
    payload.append('secondary_education', profile.value.secondary_education || '')
    payload.append('tertiary_education', profile.value.tertiary_education ? 'true' : 'false')
    payload.append('tertiary_details', profile.value.tertiary_details || '')
    payload.append('gastro_courses', profile.value.gastro_courses || '')
    payload.append('skills', profile.value.skills || '')
    payload.append('has_sanitary_license', profile.value.has_sanitary_license ? 'true' : 'false')
    payload.append('has_food_handling_cert', profile.value.has_food_handling_cert ? 'true' : 'false')
    payload.append('has_own_transport', profile.value.has_own_transport ? 'true' : 'false')
    
    const selectedRoles = Array.isArray(profile.value.roles) && profile.value.roles.length
      ? profile.value.roles
      : (profile.value.role ? [profile.value.role] : [])

    selectedRoles.forEach((roleId) => {
      payload.append('roles', String(roleId))
    })

    if (selectedRoles.length) {
      payload.append('role', String(selectedRoles[0]))
    }
    payload.append('years_experience', String(profile.value.years_experience ?? 0))
    payload.append('availability', profile.value.availability || '')
    payload.append('bio', profile.value.bio || '')
    payload.append('observations', profile.value.observations || '')
    if (selectedPhoto.value) {
      payload.append('personal_photo', selectedPhoto.value)
    }

    const { data } = await api.put('/profile/', payload)
    data.roles = Array.isArray(data.roles) && data.roles.length ? data.roles : (data.role ? [data.role] : [])
    profile.value = { ...profile.value, ...data, roles: data.roles }
    selectedPhoto.value = null
    photoInputKey.value += 1
  } catch {
    error.value = 'No se pudo guardar tu perfil.'
  } finally {
    saving.value = false
  }
}

function cambiarFoto(event) {
  const [file] = event.target.files || []
  selectedPhoto.value = file || null
}

function obtenerUrlVistaPreviaFoto() {
  if (selectedPhotoPreview.value) {
    return selectedPhotoPreview.value
  }
  return profile.value.personal_photo_url
}

watch(selectedPhoto, (file) => {
  if (selectedPhotoPreview.value) {
    URL.revokeObjectURL(selectedPhotoPreview.value)
    selectedPhotoPreview.value = ''
  }

  if (file) {
    selectedPhotoPreview.value = URL.createObjectURL(file)
  }
})

onBeforeUnmount(() => {
  if (selectedPhotoPreview.value) {
    URL.revokeObjectURL(selectedPhotoPreview.value)
  }
})

async function agregarExperiencia() {
  error.value = ''
  try {
    await api.post('/experiences/', experienceForm.value)
    experienceForm.value = {
      company_name: '',
      role: '',
      start_date: '',
      end_date: '',
      is_current: false,
      description: '',
    }
    await cargarPerfil()
  } catch {
    error.value = 'No se pudo agregar la experiencia.'
  }
}

async function eliminarExperiencia(id) {
  try {
    await api.delete(`/experiences/${id}/`)
    await cargarPerfil()
  } catch {
    error.value = 'No se pudo eliminar la experiencia.'
  }
}

async function agregarReferencia() {
  error.value = ''
  try {
    await api.post('/references/', referenceForm.value)
    referenceForm.value = {
      full_name: '',
      company: '',
      relation: '',
      phone: '',
      email: '',
      note: '',
    }
    await cargarPerfil()
  } catch {
    error.value = 'No se pudo agregar la referencia.'
  }
}

async function eliminarReferencia(id) {
  try {
    await api.delete(`/references/${id}/`)
    await cargarPerfil()
  } catch {
    error.value = 'No se pudo eliminar la referencia.'
  }
}

function cerrarSesion() {
  limpiarAutenticacion()
  router.push('/auth')
}

onMounted(cargarPerfil)
onMounted(cargarRubros)
</script>

<template>
  <section v-if="loading" class="tarjeta">Cargando perfil...</section>

  <section v-else class="grilla-tablero">
    <article class="tarjeta">
      <div class="cabecera-en-linea">
        <h2>Mi perfil profesional</h2>
        <button class="boton-secundario" @click="cerrarSesion">Cerrar sesión</button>
      </div>
      <form class="grilla-formulario" @submit.prevent="guardarPerfil">
        <div class="bloque-foto-perfil ancho-completo">
          <img
            v-if="selectedPhoto || profile.personal_photo_url"
            :src="obtenerUrlVistaPreviaFoto()"
            alt="Foto personal del trabajador"
            class="vista-previa-foto-perfil"
          />
          <label class="ancho-completo">
            Fotografía personal
            <input
              :key="photoInputKey"
              type="file"
              accept="image/*"
              @change="cambiarFoto"
            />
          </label>
          <small class="ayuda-campo">Formato recomendado: JPG o PNG, imagen vertical, hasta 5 MB.</small>
        </div>

        <h3 class="titulo-seccion ancho-completo">Datos Personales</h3>
        <label>
          Nombre
          <input v-model="profile.first_name" required />
        </label>
        <label>
          Apellido
          <input v-model="profile.last_name" required />
        </label>
        <div class="campo-genero">
          <span>Perfil del trabajador</span>
          <div class="opciones-genero" role="group" aria-label="Seleccionar género del trabajador">
            <label class="etiqueta-checkbox opcion-genero">
              <input
                type="checkbox"
                :checked="profile.gender === 'hombre'"
                @change="alternarGeneroPerfil('hombre', $event.target.checked)"
              />
              Hombre
            </label>
            <label class="etiqueta-checkbox opcion-genero">
              <input
                type="checkbox"
                :checked="profile.gender === 'mujer'"
                @change="alternarGeneroPerfil('mujer', $event.target.checked)"
              />
              Mujer
            </label>
          </div>
          <small class="ayuda-campo">Esto define el avatar automático si no cargás foto.</small>
        </div>
        <label>
          DNI
          <input v-model="profile.dni" placeholder="Ej: 12345678" />
        </label>
        <label>
          Fecha de nacimiento
          <input v-model="profile.birth_date" type="date" />
        </label>
        <label class="ancho-completo">
          Domicilio
          <input v-model="profile.address" placeholder="Calle, número, piso" />
        </label>
        <label>
          Localidad/Ciudad
          <input v-model="profile.city" required />
        </label>
        <label>
          Teléfono
          <input v-model="profile.phone" required />
        </label>
        <label class="ancho-completo">
          Redes sociales (opcional)
          <input v-model="profile.social_networks" placeholder="LinkedIn, Instagram, Facebook..." />
        </label>

        <h3 class="titulo-seccion ancho-completo">Puesto al que se postula</h3>
        <div class="ancho-completo campo-rubros">
          <span>Rubros</span>
          <div class="casillas-rubros" role="group" aria-label="Rubros disponibles">
            <label v-for="roleItem in roles" :key="roleItem.id" class="etiqueta-checkbox casilla-rubro">
              <input v-model="profile.roles" type="checkbox" :value="roleItem.id" />
              {{ formatearEtiquetaRubro(roleItem.name) }}
            </label>
          </div>
          <small class="ayuda-campo">Podés seleccionar uno o varios rubros.</small>
        </div>

        <h3 class="titulo-seccion ancho-completo">Experiencia y Disponibilidad</h3>
        <label>
          Años de experiencia
          <input v-model.number="profile.years_experience" type="number" min="0" required />
        </label>
        <label>
          Disponibilidad
          <input v-model="profile.availability" placeholder="Full time, turno noche, fines de semana..." />
        </label>
        <label>
          Horario preferido
          <select v-model="profile.schedule">
            <option value="">Seleccionar...</option>
            <option value="manana">Mañana</option>
            <option value="tarde">Tarde</option>
            <option value="noche">Noche</option>
            <option value="full_time">Full Time</option>
          </select>
        </label>
        <label class="etiqueta-checkbox">
          <input v-model="profile.can_work_weekends_holidays" type="checkbox" />
          Puede trabajar fines de semana y feriados
        </label>
        <label>
          Remuneración pretendida
          <input v-model="profile.expected_salary" placeholder="Rango salarial" />
        </label>

        <h3 class="titulo-seccion ancho-completo">Formación</h3>
        <label>
          Estudios primarios
          <select v-model="profile.primary_education">
            <option value="">Seleccionar...</option>
            <option value="completo">Completo</option>
            <option value="incompleto">Incompleto</option>
          </select>
        </label>
        <label>
          Estudios secundarios
          <select v-model="profile.secondary_education">
            <option value="">Seleccionar...</option>
            <option value="completo">Completo</option>
            <option value="incompleto">Incompleto</option>
          </select>
        </label>
        <label class="etiqueta-checkbox">
          <input v-model="profile.tertiary_education" type="checkbox" />
          Tiene estudios terciarios/universitarios
        </label>
        <label class="ancho-completo">
          Detalles de estudios terciarios/universitarios
          <textarea v-model="profile.tertiary_details" rows="2"></textarea>
        </label>
        <label class="ancho-completo">
          Cursos gastronómicos realizados
          <textarea v-model="profile.gastro_courses" rows="2" placeholder="Detalla los cursos que has realizado"></textarea>
        </label>

        <h3 class="titulo-seccion ancho-completo">Conocimientos y Habilidades</h3>
        <label class="ancho-completo">
          Habilidades (separadas por comas)
          <input v-model="profile.skills" placeholder="Ej: Atención al cliente, Cocina caliente, Pastelería..." />
        </label>

        <h3 class="titulo-seccion ancho-completo">Documentos y Certificaciones</h3>
        <label class="etiqueta-checkbox">
          <input v-model="profile.has_sanitary_license" type="checkbox" />
          Cuenta con Libreta Sanitaria vigente
        </label>
        <label class="etiqueta-checkbox">
          <input v-model="profile.has_food_handling_cert" type="checkbox" />
          Posee carnet de manipulación de alimentos
        </label>
        <label class="etiqueta-checkbox">
          <input v-model="profile.has_own_transport" type="checkbox" />
          Tiene movilidad propia
        </label>

        <h3 class="titulo-seccion ancho-completo">Información General</h3>
        <label class="ancho-completo">
          Presentación profesional
          <textarea v-model="profile.bio" rows="4" placeholder="Contá tu recorrido y fortalezas en gastronomía"></textarea>
        </label>
        <label class="ancho-completo">
          Observaciones adicionales
          <textarea v-model="profile.observations" rows="3"></textarea>
        </label>

        <button class="boton-principal ancho-completo" type="submit" :disabled="saving">{{ saving ? 'Guardando...' : 'Guardar perfil' }}</button>
      </form>
    </article>

    <article class="tarjeta">
      <h2>Nueva experiencia</h2>
      <form class="grilla-formulario" @submit.prevent="agregarExperiencia">
        <label>
          Empresa
          <input v-model="experienceForm.company_name" required />
        </label>
        <label>
          Rol
          <input v-model="experienceForm.role" required />
        </label>
        <label>
          Fecha inicio
          <input v-model="experienceForm.start_date" type="date" required />
        </label>
        <label>
          Fecha fin
          <input v-model="experienceForm.end_date" type="date" :disabled="experienceForm.is_current" />
        </label>
        <label class="etiqueta-checkbox">
          <input v-model="experienceForm.is_current" type="checkbox" />
          Trabajo actual
        </label>
        <label class="ancho-completo">
          Descripción
          <textarea v-model="experienceForm.description" rows="3"></textarea>
        </label>
        <button class="boton-principal" type="submit">Agregar experiencia</button>
      </form>
      <ListaExperiencias :experiences="profile.experiences" @delete="eliminarExperiencia" />
    </article>

    <article class="tarjeta">
      <h2>Nueva referencia</h2>
      <form class="grilla-formulario" @submit.prevent="agregarReferencia">
        <label>
          Nombre
          <input v-model="referenceForm.full_name" required />
        </label>
        <label>
          Empresa
          <input v-model="referenceForm.company" />
        </label>
        <label>
          Relación
          <input v-model="referenceForm.relation" placeholder="Ex jefe, supervisor, compañero" required />
        </label>
        <label>
          Teléfono
          <input v-model="referenceForm.phone" />
        </label>
        <label>
          Email
          <input v-model="referenceForm.email" type="email" />
        </label>
        <label class="ancho-completo">
          Nota
          <textarea v-model="referenceForm.note" rows="3"></textarea>
        </label>
        <button class="boton-principal" type="submit">Agregar referencia</button>
      </form>
      <ListaReferencias :references="profile.references" @delete="eliminarReferencia" />
    </article>

    <p v-if="error" class="texto-error">{{ error }}</p>
  </section>
</template>

<style scoped>
.titulo-seccion {
  margin-top: 2rem;
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid #d4a574;
  font-size: 1.1rem;
  font-weight: 600;
  color: #8b6f47;
}

.titulo-seccion:first-of-type {
  margin-top: 1rem;
}
</style>
