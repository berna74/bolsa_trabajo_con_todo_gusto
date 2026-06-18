<script setup>
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '../services/clienteApi'
import { useTiendaAutenticacion } from '../stores/autenticacion'

const router = useRouter()
const tiendaAutenticacion = useTiendaAutenticacion()
const isLogin = ref(true)
const error = ref('')
const submitting = ref(false)

const submitLabel = computed(() => {
  if (!submitting.value) {
    return isLogin.value ? 'Entrar' : 'Registrarme'
  }

  return isLogin.value ? 'Ingresando...' : 'Creando cuenta...'
})

const helperText = computed(() => {
  if (submitting.value) {
    return isLogin.value
      ? 'Estamos validando tus credenciales y preparando tu sesión.'
      : 'Estamos creando tu cuenta y abriendo tu sesión.'
  }

  return isLogin.value
    ? 'Ingresá con tu usuario y contraseña para administrar tu perfil.'
    : 'Tu cuenta se crea y, si todo sale bien, entrás automáticamente.'
})

function cambiarModo(nextIsLogin) {
  if (submitting.value) {
    return
  }

  isLogin.value = nextIsLogin
  error.value = ''
}

const loginForm = ref({
  username: '',
  password: '',
})

const registerForm = ref({
  username: '',
  email: '',
  password: '',
})

async function iniciarSesion() {
  error.value = ''
  submitting.value = true
  try {
    await tiendaAutenticacion.iniciarSesion(loginForm.value)
    router.push('/tablero')
  } catch {
    error.value = 'No se pudo iniciar sesión. Verificá usuario y contraseña.'
  } finally {
    submitting.value = false
  }
}

async function registrarCuenta() {
  error.value = ''
  submitting.value = true

  try {
    await api.post('/auth/register/', registerForm.value)
    await iniciarSesionConDatosRegistro()
  } catch {
    error.value = 'No se pudo registrar. Revisá los datos e intentá nuevamente.'
  } finally {
    submitting.value = false
  }
}

async function iniciarSesionConDatosRegistro() {
  await tiendaAutenticacion.iniciarSesion({
    username: registerForm.value.username,
    password: registerForm.value.password,
  })
  router.push('/tablero')
}
</script>

<template>
  <section class="tarjeta tarjeta-autenticacion">
    <header class="encabezado-autenticacion">
      <h2>{{ isLogin ? 'Ingresar a mi cuenta' : 'Crear una cuenta' }}</h2>
      <p class="texto-ayuda-autenticacion">{{ helperText }}</p>
    </header>

    <div class="conmutador-autenticacion">
      <button :class="{ active: isLogin }" :disabled="submitting" @click="cambiarModo(true)">Ingresar</button>
      <button :class="{ active: !isLogin }" :disabled="submitting" @click="cambiarModo(false)">Crear cuenta</button>
    </div>

    <p class="estado-autenticacion" :class="{ ocupado: submitting }" aria-live="polite">
      {{ helperText }}
    </p>

    <form v-if="isLogin" class="grilla-formulario" @submit.prevent="iniciarSesion">
      <label>
        Usuario
        <input v-model="loginForm.username" :disabled="submitting" autocomplete="username" required />
      </label>
      <label>
        Contraseña
        <input v-model="loginForm.password" :disabled="submitting" type="password" autocomplete="current-password" required />
      </label>
      <button class="boton-principal" type="submit" :disabled="submitting">{{ submitLabel }}</button>
    </form>

    <form v-else class="grilla-formulario" @submit.prevent="registrarCuenta">
      <label>
        Usuario
        <input v-model="registerForm.username" :disabled="submitting" autocomplete="username" required />
      </label>
      <label>
        Email
        <input v-model="registerForm.email" :disabled="submitting" type="email" autocomplete="email" required />
      </label>
      <label>
        Contraseña
        <input v-model="registerForm.password" :disabled="submitting" type="password" autocomplete="new-password" minlength="8" required />
      </label>
      <button class="boton-principal" type="submit" :disabled="submitting">{{ submitLabel }}</button>
    </form>

    <p v-if="error" class="texto-error caja-error-auth" role="alert">{{ error }}</p>
  </section>
</template>
