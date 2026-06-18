<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import api from '../services/api'
import femalePlaceholder from '../assets/female_placeholder_baja.png'
import malePlaceholder from '../assets/male_placeholder_baja.png'

const route = useRoute()
const loading = ref(true)
const error = ref('')
const groups = ref([])

function sanitizePhone(phone) {
  return (phone || '').replace(/[^\d+]/g, '')
}

function formatDate(value) {
  if (!value) {
    return ''
  }
  const date = new Date(value)
  if (Number.isNaN(date.getTime())) {
    return value
  }
  return date.toLocaleDateString('es-AR')
}

function whatsappLink(phone, name) {
  const cleanPhone = sanitizePhone(phone)
  if (!cleanPhone) {
    return ''
  }
  const message = encodeURIComponent(`Hola ${name}, vi tu perfil en ConTodoGusto y me gustaría contactarte.`)
  return `https://wa.me/${cleanPhone}?text=${message}`
}

function emailLink(email, name) {
  if (!email) {
    return ''
  }
  const subject = encodeURIComponent('Contacto laboral desde ConTodoGusto')
  const body = encodeURIComponent(`Hola ${name}, vi tu perfil y me gustaría conversar sobre una oportunidad laboral.`)
  return `mailto:${email}?subject=${subject}&body=${body}`
}

function workerFallbackPhoto(worker) {
  return worker?.gender === 'mujer' ? femalePlaceholder : malePlaceholder
}

const workerData = computed(() => {
  const workerId = Number(route.params.id)
  for (const group of groups.value) {
    const worker = group.workers.find((item) => item.id === workerId)
    if (worker) {
      return { ...worker, rubro: group.rubro }
    }
  }
  return null
})

async function fetchWorkersByRole() {
  loading.value = true
  error.value = ''
  try {
    const { data } = await api.get('/public/workers-by-role/')
    groups.value = data
  } catch {
    error.value = 'No se pudo cargar el perfil del trabajador.'
  } finally {
    loading.value = false
  }
}

onMounted(fetchWorkersByRole)
</script>

<template>
  <section class="panel detail-panel">
    <p v-if="loading">Cargando perfil...</p>
    <p v-else-if="error" class="error-text">{{ error }}</p>

    <template v-else-if="workerData">
      <div class="worker-profile-header">
        <img
          v-if="workerData.personal_photo_url"
          :src="workerData.personal_photo_url"
          :alt="`Foto de ${workerData.full_name}`"
          class="worker-photo worker-photo-lg"
        />
        <img
          v-else
          :src="workerFallbackPhoto(workerData)"
          :alt="`Placeholder de chef para ${workerData.full_name}`"
          class="worker-photo worker-photo-lg worker-photo-placeholder"
        />

        <div class="worker-profile-meta">
          <h2>{{ workerData.full_name }}</h2>
          <p v-if="workerData.city"><strong>Ciudad:</strong> {{ workerData.city }}</p>
          <p v-if="workerData.years_experience"><strong>Experiencia:</strong> {{ workerData.years_experience }} años</p>
          <p v-if="workerData.availability"><strong>Disponibilidad:</strong> {{ workerData.availability }}</p>
          <div class="worker-actions worker-actions-detail">
            <a
              v-if="whatsappLink(workerData.phone, workerData.full_name)"
              :href="whatsappLink(workerData.phone, workerData.full_name)"
              target="_blank"
              rel="noopener noreferrer"
              class="contact-btn"
              aria-label="Contactar por WhatsApp"
              title="WhatsApp"
            >
              <svg class="btn-icon" viewBox="0 0 24 24" aria-hidden="true">
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
              v-if="emailLink(workerData.email, workerData.full_name)"
              :href="emailLink(workerData.email, workerData.full_name)"
              class="contact-btn"
              aria-label="Contactar por Email"
              title="Email"
            >
              <svg class="btn-icon" viewBox="0 0 24 24" aria-hidden="true">
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

      <section v-if="workerData.bio" class="worker-bio-block">
        <h3>Presentación profesional</h3>
        <p>{{ workerData.bio }}</p>
      </section>

      <section
        v-if="workerData.birth_date || workerData.address || workerData.social_networks"
        class="worker-bio-block"
      >
        <h3>Datos personales</h3>
        <p v-if="workerData.birth_date"><strong>Fecha de nacimiento:</strong> {{ formatDate(workerData.birth_date) }}</p>
        <p v-if="workerData.address"><strong>Domicilio:</strong> {{ workerData.address }}</p>
        <p v-if="workerData.social_networks"><strong>Redes sociales:</strong> {{ workerData.social_networks }}</p>
      </section>

      <section
        v-if="workerData.years_experience || workerData.availability || workerData.schedule || workerData.can_work_weekends_holidays || workerData.expected_salary"
        class="worker-bio-block"
      >
        <h3>Experiencia y disponibilidad</h3>
        <p v-if="workerData.years_experience"><strong>Años de experiencia:</strong> {{ workerData.years_experience }}</p>
        <p v-if="workerData.availability"><strong>Disponibilidad:</strong> {{ workerData.availability }}</p>
        <p v-if="workerData.schedule"><strong>Horario preferido:</strong> {{ workerData.schedule }}</p>
        <p v-if="workerData.can_work_weekends_holidays"><strong>Trabaja fines de semana/feriados:</strong> Sí</p>
        <p v-if="workerData.expected_salary"><strong>Remuneración pretendida:</strong> {{ workerData.expected_salary }}</p>
      </section>

      <section
        v-if="workerData.primary_education || workerData.secondary_education || workerData.tertiary_education || workerData.tertiary_details || workerData.gastro_courses"
        class="worker-bio-block"
      >
        <h3>Formación</h3>
        <p v-if="workerData.primary_education"><strong>Primaria:</strong> {{ workerData.primary_education }}</p>
        <p v-if="workerData.secondary_education"><strong>Secundaria:</strong> {{ workerData.secondary_education }}</p>
        <p v-if="workerData.tertiary_education"><strong>Terciaria/Universitaria:</strong> Sí</p>
        <p v-if="workerData.tertiary_details"><strong>Detalle terciario:</strong> {{ workerData.tertiary_details }}</p>
        <p v-if="workerData.gastro_courses"><strong>Cursos gastronómicos:</strong> {{ workerData.gastro_courses }}</p>
      </section>

      <section
        v-if="workerData.skills || workerData.has_sanitary_license || workerData.has_food_handling_cert || workerData.has_own_transport"
        class="worker-bio-block"
      >
        <h3>Habilidades y certificaciones</h3>
        <p v-if="workerData.skills"><strong>Habilidades:</strong> {{ workerData.skills }}</p>
        <p v-if="workerData.has_sanitary_license"><strong>Libreta sanitaria:</strong> Sí</p>
        <p v-if="workerData.has_food_handling_cert"><strong>Carnet manipulación:</strong> Sí</p>
        <p v-if="workerData.has_own_transport"><strong>Movilidad propia:</strong> Sí</p>
      </section>

      <section v-if="workerData.experiences?.length" class="worker-bio-block">
        <h3>Experiencia laboral registrada</h3>
        <article v-for="(exp, idx) in workerData.experiences" :key="`${exp.company_name}-${idx}`" class="list-card">
          <p v-if="exp.company_name"><strong>Empresa:</strong> {{ exp.company_name }}</p>
          <p v-if="exp.role"><strong>Puesto:</strong> {{ exp.role }}</p>
          <p v-if="exp.start_date"><strong>Desde:</strong> {{ formatDate(exp.start_date) }}</p>
          <p v-if="exp.is_current || exp.end_date"><strong>Hasta:</strong> {{ exp.is_current ? 'Actualidad' : formatDate(exp.end_date) }}</p>
          <p v-if="exp.description"><strong>Tareas:</strong> {{ exp.description }}</p>
        </article>
      </section>

      <section v-if="workerData.references?.length" class="worker-bio-block">
        <h3>Referencias profesionales</h3>
        <article v-for="(ref, idx) in workerData.references" :key="`${ref.full_name}-${idx}`" class="list-card">
          <p v-if="ref.full_name"><strong>Nombre:</strong> {{ ref.full_name }}</p>
          <p v-if="ref.company"><strong>Empresa:</strong> {{ ref.company }}</p>
          <p v-if="ref.relation"><strong>Relación:</strong> {{ ref.relation }}</p>
          <p v-if="ref.phone"><strong>Teléfono:</strong> {{ ref.phone }}</p>
          <p v-if="ref.email"><strong>Email:</strong> {{ ref.email }}</p>
          <p v-if="ref.note"><strong>Nota:</strong> {{ ref.note }}</p>
        </article>
      </section>

      <section v-if="workerData.observations" class="worker-bio-block">
        <h3>Observaciones</h3>
        <p>{{ workerData.observations }}</p>
      </section>

      <div class="detail-actions">
        <router-link class="secondary-btn" to="/">Volver al inicio</router-link>
      </div>
    </template>

    <template v-else>
      <h2>Perfil no encontrado</h2>
      <p>El trabajador no existe o ya no está publicado.</p>
      <router-link class="secondary-btn" to="/">Volver al inicio</router-link>
    </template>
  </section>
</template>
