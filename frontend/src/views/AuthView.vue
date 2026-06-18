<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '../services/api'
import { saveTokens } from '../services/auth'

const router = useRouter()
const isLogin = ref(true)
const error = ref('')

const loginForm = ref({
  username: '',
  password: '',
})

const registerForm = ref({
  username: '',
  email: '',
  password: '',
})

async function submitLogin() {
  error.value = ''
  try {
    const { data } = await api.post('/auth/login/', loginForm.value)
    saveTokens(data.access, data.refresh)
    router.push('/dashboard')
  } catch {
    error.value = 'No se pudo iniciar sesión. Verificá usuario y contraseña.'
  }
}

async function submitRegister() {
  error.value = ''

  try {
    await api.post('/auth/register/', registerForm.value)
    await submitLoginWithRegisterData()
  } catch {
    error.value = 'No se pudo registrar. Revisá los datos e intentá nuevamente.'
  }
}

async function submitLoginWithRegisterData() {
  const { data } = await api.post('/auth/login/', {
    username: registerForm.value.username,
    password: registerForm.value.password,
  })
  saveTokens(data.access, data.refresh)
  router.push('/dashboard')
}
</script>

<template>
  <section class="panel auth-panel">
    <div class="auth-switch">
      <button :class="{ active: isLogin }" @click="isLogin = true">Ingresar</button>
      <button :class="{ active: !isLogin }" @click="isLogin = false">Crear cuenta</button>
    </div>

    <form v-if="isLogin" class="form-grid" @submit.prevent="submitLogin">
      <label>
        Usuario
        <input v-model="loginForm.username" required />
      </label>
      <label>
        Contraseña
        <input v-model="loginForm.password" type="password" required />
      </label>
      <button class="primary-btn" type="submit">Entrar</button>
    </form>

    <form v-else class="form-grid" @submit.prevent="submitRegister">
      <label>
        Usuario
        <input v-model="registerForm.username" required />
      </label>
      <label>
        Email
        <input v-model="registerForm.email" type="email" required />
      </label>
      <label>
        Contraseña
        <input v-model="registerForm.password" type="password" minlength="8" required />
      </label>
      <button class="primary-btn" type="submit">Registrarme</button>
    </form>

    <p v-if="error" class="error-text">{{ error }}</p>
  </section>
</template>
