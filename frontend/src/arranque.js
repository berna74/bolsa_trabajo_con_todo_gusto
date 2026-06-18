import { createApp } from 'vue'
import Aplicacion from './Aplicacion.vue'
import rutas from './rutas'
import { pinia } from './stores/instanciaPinia'
import './styles.css'

createApp(Aplicacion).use(pinia).use(rutas).mount('#app')
