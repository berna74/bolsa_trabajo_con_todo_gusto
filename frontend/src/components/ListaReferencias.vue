<script setup>
defineProps({
  references: {
    type: Array,
    required: true,
  },
})

const emit = defineEmits(['delete'])
</script>

<template>
  <div class="seccion-lista">
    <h3>Referencias</h3>
    <article v-for="item in references" :key="item.id" class="tarjeta-lista">
      <div class="cabecera-lista">
        <strong>{{ item.full_name }}</strong>
        <button class="danger-btn" @click="emit('delete', item.id)">Eliminar</button>
      </div>
      <p>{{ item.relation }} <span v-if="item.company">- {{ item.company }}</span></p>
      <p>{{ item.phone }} <span v-if="item.email">| {{ item.email }}</span></p>
      <p>{{ item.note }}</p>
    </article>
  </div>
</template>
