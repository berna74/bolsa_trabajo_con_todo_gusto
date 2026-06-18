import { useTiendaAutenticacion } from '../stores/autenticacion'
import { pinia } from '../stores/instanciaPinia'

function authStore() {
  return useTiendaAutenticacion(pinia)
}

export function guardarTokens(tokenAcceso, tokenActualizacion) {
  authStore().guardarTokens(tokenAcceso, tokenActualizacion)
}

export function obtenerToken() {
  return authStore().tokenAcceso
}

export function tieneToken() {
  return authStore().sesionActiva
}

export function guardarRolAplicacion(rolAplicacion) {
  authStore().guardarRolAplicacion(rolAplicacion)
}

export function obtenerRolAplicacion() {
  return authStore().rolAplicacion
}

export function limpiarAutenticacion() {
  authStore().limpiarAutenticacion()
}
