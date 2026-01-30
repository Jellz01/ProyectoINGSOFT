<script setup>
import { ref, onMounted } from 'vue'
import { cajaService, usuariosService } from '../services/api'

const cajas = ref([])
const usuarios = ref([])
const cajaAbierta = ref(null)
const loading = ref(true)
const showAbrirModal = ref(false)
const showCerrarModal = ref(false)
const message = ref({ text: '', type: '' })

const nuevaCaja = ref({
  monto_inicial: 0,
  usuario_id: ''
})

const cierreCaja = ref({
  monto_final: 0
})

const loadData = async () => {
  try {
    loading.value = true
    const [cajasRes, usuariosRes] = await Promise.all([
      cajaService.getAll(),
      usuariosService.getAll()
    ])
    cajas.value = cajasRes.data.data || []
    usuarios.value = usuariosRes.data.data || []

    try {
      const abiertaRes = await cajaService.getAbierta()
      cajaAbierta.value = abiertaRes.data.data || null
    } catch {
      cajaAbierta.value = null
    }
  } catch (error) {
    showMessage('Error al cargar datos', 'danger')
  } finally {
    loading.value = false
  }
}

const openAbrirModal = () => {
  nuevaCaja.value = { monto_inicial: 0, usuario_id: '' }
  showAbrirModal.value = true
}

const abrirCaja = async () => {
  if (!nuevaCaja.value.usuario_id) {
    showMessage('Seleccione un usuario', 'warning')
    return
  }
  try {
    await cajaService.abrir({
      monto_inicial: Number(nuevaCaja.value.monto_inicial),
      usuario_id: Number(nuevaCaja.value.usuario_id)
    })
    showMessage('Caja abierta correctamente', 'success')
    showAbrirModal.value = false
    loadData()
  } catch (error) {
    showMessage('Error al abrir caja. Puede que ya haya una caja abierta.', 'danger')
  }
}

const openCerrarModal = () => {
  cierreCaja.value = { monto_final: 0 }
  showCerrarModal.value = true
}

const cerrarCaja = async () => {
  if (!cajaAbierta.value) return
  try {
    await cajaService.cerrar(cajaAbierta.value.id, {
      monto_final: Number(cierreCaja.value.monto_final)
    })
    showMessage('Caja cerrada correctamente', 'success')
    showCerrarModal.value = false
    loadData()
  } catch (error) {
    showMessage('Error al cerrar caja', 'danger')
  }
}

const formatDate = (dateStr) => {
  if (!dateStr) return '-'
  const date = new Date(dateStr)
  return date.toLocaleDateString('es-EC', { day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit' })
}

const showMessage = (text, type) => {
  message.value = { text, type }
  setTimeout(() => { message.value = { text: '', type: '' } }, 3000)
}

onMounted(loadData)
</script>

<template>
  <div>
    <div class="page-header">
      <h1>Caja</h1>
    </div>

    <div v-if="message.text" :class="['alert', `alert-${message.type}`]">
      {{ message.text }}
    </div>

    <!-- Estado actual de la caja -->
    <div class="card" v-if="!loading">
      <div class="card-header">
        <h2 class="card-title">Estado Actual</h2>
        <div>
          <button v-if="!cajaAbierta" class="btn btn-success" @click="openAbrirModal">Abrir Caja</button>
          <button v-else class="btn btn-danger" @click="openCerrarModal">Cerrar Caja</button>
        </div>
      </div>

      <div v-if="cajaAbierta" class="stats-grid">
        <div class="stat-card">
          <h3>${{ cajaAbierta.monto_inicial?.toFixed(2) }}</h3>
          <p>Monto Inicial</p>
        </div>
        <div class="stat-card">
          <h3>{{ formatDate(cajaAbierta.fecha_apertura) }}</h3>
          <p>Fecha Apertura</p>
        </div>
        <div class="stat-card">
          <h3>{{ cajaAbierta.movimientos?.length || 0 }}</h3>
          <p>Movimientos</p>
        </div>
      </div>

      <div v-else style="text-align: center; padding: 30px; color: #95a5a6;">
        No hay caja abierta actualmente
      </div>
    </div>

    <!-- Historial de cajas -->
    <div class="card">
      <div class="card-header">
        <h2 class="card-title">Historial de Cajas</h2>
      </div>

      <div v-if="loading" class="loading">Cargando...</div>

      <div v-else class="table-container">
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Apertura</th>
              <th>Cierre</th>
              <th>Monto Inicial</th>
              <th>Monto Final</th>
              <th>Estado</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="caja in cajas" :key="caja.id">
              <td>{{ caja.id }}</td>
              <td>{{ formatDate(caja.fecha_apertura) }}</td>
              <td>{{ formatDate(caja.fecha_cierre) }}</td>
              <td>${{ caja.monto_inicial?.toFixed(2) }}</td>
              <td>{{ caja.monto_final != null ? '$' + caja.monto_final.toFixed(2) : '-' }}</td>
              <td>
                <span :class="caja.estado === 'ABIERTA' ? 'badge badge-abierta' : 'badge badge-cerrada'">
                  {{ caja.estado }}
                </span>
              </td>
            </tr>
            <tr v-if="cajas.length === 0">
              <td colspan="6" style="text-align: center;">No hay registros de caja</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Modal Abrir Caja -->
    <div v-if="showAbrirModal" class="modal-overlay" @click.self="showAbrirModal = false">
      <div class="modal">
        <div class="modal-header">
          <h3>Abrir Caja</h3>
          <button class="modal-close" @click="showAbrirModal = false">&times;</button>
        </div>
        <form @submit.prevent="abrirCaja">
          <div class="form-group">
            <label>Usuario responsable</label>
            <select class="form-control" v-model="nuevaCaja.usuario_id" required>
              <option value="">Seleccionar...</option>
              <option v-for="u in usuarios" :key="u.id" :value="u.id">{{ u.nombre }}</option>
            </select>
          </div>
          <div class="form-group">
            <label>Monto inicial ($)</label>
            <input type="number" class="form-control" v-model.number="nuevaCaja.monto_inicial" step="0.01" min="0" required>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn" @click="showAbrirModal = false">Cancelar</button>
            <button type="submit" class="btn btn-success">Abrir Caja</button>
          </div>
        </form>
      </div>
    </div>

    <!-- Modal Cerrar Caja -->
    <div v-if="showCerrarModal" class="modal-overlay" @click.self="showCerrarModal = false">
      <div class="modal">
        <div class="modal-header">
          <h3>Cerrar Caja</h3>
          <button class="modal-close" @click="showCerrarModal = false">&times;</button>
        </div>
        <form @submit.prevent="cerrarCaja">
          <div class="form-group">
            <label>Monto final en caja ($)</label>
            <input type="number" class="form-control" v-model.number="cierreCaja.monto_final" step="0.01" min="0" required>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn" @click="showCerrarModal = false">Cancelar</button>
            <button type="submit" class="btn btn-danger">Cerrar Caja</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<style scoped>
.badge {
  padding: 4px 10px;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 600;
  color: white;
}
.badge-abierta { background-color: #2ecc71; }
.badge-cerrada { background-color: #95a5a6; }
</style>
