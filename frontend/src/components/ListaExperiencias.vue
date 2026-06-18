<script setup>
defineProps({
  experiences: {
    type: Array,
    required: true,
  },
})

const emit = defineEmits(['delete'])
</script>

<template>
  <div class="seccion-lista">
    <h3>Experiencia laboral</h3>
    <article v-for="item in experiences" :key="item.id" class="tarjeta-lista">
      <div class="cabecera-lista">
        <strong>{{ item.role }}</strong>
        <button class="danger-btn" @click="emit('delete', item.id)">Eliminar</button>
      </div>
      <p>{{ item.company_name }}</p>
      <p>{{ item.start_date }} - {{ item.is_current ? 'Actual' : item.end_date || 'Sin fecha fin' }}</p>
      <p>{{ item.description }}</p>
    </article>
  </div>
</template>
