<script setup>
import { ref, onMounted, computed } from 'vue'
import { ventasService, productosService, clientesService, usuariosService } from '../services/api'

const ventas = ref([])
const productos = ref([])
const clientes = ref([])
const usuarios = ref([])
const loading = ref(true)
const showModal = ref(false)
const message = ref({ text: '', type: '' })

const nuevaVenta = ref({
  usuario_id: '',
  cliente_id: '',
  detalles: []
})

const nuevoDetalle = ref({
  producto_id: '',
  cantidad: 1
})

const totalVenta = computed(() => {
  return nuevaVenta.value.detalles.reduce((sum, d) => sum + d.subtotal, 0)
})

const loadData = async () => {
  try {
    loading.value = true
    const [ventasRes, productosRes, clientesRes, usuariosRes] = await Promise.all([
      ventasService.getAll(),
      productosService.getAll(),
      clientesService.getAll(),
      usuariosService.getAll()
    ])
    ventas.value = ventasRes.data.data || []
    productos.value = productosRes.data.data || []
    clientes.value = clientesRes.data.data || []
    usuarios.value = usuariosRes.data.data || []
  } catch (error) {
    showMessage('Error al cargar datos', 'danger')
  } finally {
    loading.value = false
  }
}

const openCreateModal = () => {
  nuevaVenta.value = { usuario_id: '', cliente_id: '', detalles: [] }
  nuevoDetalle.value = { producto_id: '', cantidad: 1 }
  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
}

const agregarDetalle = () => {
  const producto = productos.value.find(p => p.id === Number(nuevoDetalle.value.producto_id))
  if (!producto) {
    showMessage('Seleccione un producto', 'warning')
    return
  }
  if (nuevoDetalle.value.cantidad <= 0) {
    showMessage('La cantidad debe ser mayor a 0', 'warning')
    return
  }

  const existe = nuevaVenta.value.detalles.find(d => d.producto_id === producto.id)
  if (existe) {
    existe.cantidad += Number(nuevoDetalle.value.cantidad)
    existe.subtotal = existe.cantidad * existe.precio_unitario
  } else {
    nuevaVenta.value.detalles.push({
      producto_id: producto.id,
      producto_nombre: producto.nombre,
      cantidad: Number(nuevoDetalle.value.cantidad),
      precio_unitario: producto.precio_venta,
      subtotal: Number(nuevoDetalle.value.cantidad) * producto.precio_venta
    })
  }
  nuevoDetalle.value = { producto_id: '', cantidad: 1 }
}

const quitarDetalle = (index) => {
  nuevaVenta.value.detalles.splice(index, 1)
}

const crearVenta = async () => {
  if (!nuevaVenta.value.usuario_id) {
    showMessage('Seleccione un usuario', 'warning')
    return
  }
  if (nuevaVenta.value.detalles.length === 0) {
    showMessage('Agregue al menos un producto', 'warning')
    return
  }

  try {
    const data = {
      usuario_id: Number(nuevaVenta.value.usuario_id),
      cliente_id: nuevaVenta.value.cliente_id ? Number(nuevaVenta.value.cliente_id) : null,
      detalles: nuevaVenta.value.detalles.map(d => ({
        producto_id: d.producto_id,
        cantidad: d.cantidad,
        precio_unitario: d.precio_unitario
      }))
    }
    await ventasService.create(data)
    showMessage('Venta creada correctamente', 'success')
    closeModal()
    loadData()
  } catch (error) {
    showMessage('Error al crear la venta', 'danger')
  }
}

const cancelarVenta = async (id) => {
  if (confirm('Esta seguro de cancelar esta venta?')) {
    try {
      await ventasService.cancelar(id)
      showMessage('Venta cancelada correctamente', 'success')
      loadData()
    } catch (error) {
      showMessage('Error al cancelar la venta', 'danger')
    }
  }
}

const getEstadoClass = (estado) => {
  const classes = {
    'COMPLETADA': 'badge badge-completada',
    'CANCELADA': 'badge badge-cancelada',
    'PENDIENTE_PAGO': 'badge badge-pendiente',
    'INICIADA': 'badge badge-iniciada',
    'EN_EDICION': 'badge badge-edicion'
  }
  return classes[estado] || 'badge'
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
      <h1>Ventas</h1>
    </div>

    <div v-if="message.text" :class="['alert', `alert-${message.type}`]">
      {{ message.text }}
    </div>

    <div class="card">
      <div class="card-header">
        <h2 class="card-title">Lista de Ventas</h2>
        <button class="btn btn-primary" @click="openCreateModal">Nueva Venta</button>
      </div>

      <div v-if="loading" class="loading">Cargando...</div>

      <div v-else class="table-container">
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Fecha</th>
              <th>Total</th>
              <th>Estado</th>
              <th>Items</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="venta in ventas" :key="venta.id">
              <td>{{ venta.id }}</td>
              <td>{{ formatDate(venta.fecha) }}</td>
              <td><strong>${{ venta.total?.toFixed(2) }}</strong></td>
              <td><span :class="getEstadoClass(venta.estado)">{{ venta.estado }}</span></td>
              <td>{{ venta.detalles?.length || 0 }} productos</td>
              <td class="actions">
                <button
                  v-if="venta.estado !== 'CANCELADA'"
                  class="btn btn-danger btn-sm"
                  @click="cancelarVenta(venta.id)"
                >Cancelar</button>
              </td>
            </tr>
            <tr v-if="ventas.length === 0">
              <td colspan="6" style="text-align: center;">No hay ventas registradas</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Modal Nueva Venta -->
    <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal" style="max-width: 700px;">
        <div class="modal-header">
          <h3>Nueva Venta</h3>
          <button class="modal-close" @click="closeModal">&times;</button>
        </div>
        <form @submit.prevent="crearVenta">
          <div class="grid-2">
            <div class="form-group">
              <label>Vendedor</label>
              <select class="form-control" v-model="nuevaVenta.usuario_id" required>
                <option value="">Seleccionar...</option>
                <option v-for="u in usuarios" :key="u.id" :value="u.id">{{ u.nombre }}</option>
              </select>
            </div>
            <div class="form-group">
              <label>Cliente (opcional)</label>
              <select class="form-control" v-model="nuevaVenta.cliente_id">
                <option value="">Consumidor final</option>
                <option v-for="c in clientes" :key="c.id" :value="c.id">{{ c.nombre }}</option>
              </select>
            </div>
          </div>

          <hr style="margin: 15px 0; border-color: #ecf0f1;">

          <h4 style="margin-bottom: 10px;">Agregar productos</h4>
          <div style="display: flex; gap: 10px; align-items: flex-end; margin-bottom: 15px;">
            <div class="form-group" style="flex: 2; margin-bottom: 0;">
              <label>Producto</label>
              <select class="form-control" v-model="nuevoDetalle.producto_id">
                <option value="">Seleccionar...</option>
                <option v-for="p in productos" :key="p.id" :value="p.id">
                  {{ p.nombre }} - ${{ p.precio_venta }}
                </option>
              </select>
            </div>
            <div class="form-group" style="flex: 1; margin-bottom: 0;">
              <label>Cantidad</label>
              <input type="number" class="form-control" v-model.number="nuevoDetalle.cantidad" min="1">
            </div>
            <button type="button" class="btn btn-success" @click="agregarDetalle">Agregar</button>
          </div>

          <div class="table-container" v-if="nuevaVenta.detalles.length > 0">
            <table>
              <thead>
                <tr>
                  <th>Producto</th>
                  <th>Cantidad</th>
                  <th>P. Unitario</th>
                  <th>Subtotal</th>
                  <th></th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(detalle, index) in nuevaVenta.detalles" :key="index">
                  <td>{{ detalle.producto_nombre }}</td>
                  <td>{{ detalle.cantidad }}</td>
                  <td>${{ detalle.precio_unitario?.toFixed(2) }}</td>
                  <td>${{ detalle.subtotal?.toFixed(2) }}</td>
                  <td>
                    <button type="button" class="btn btn-danger btn-sm" @click="quitarDetalle(index)">X</button>
                  </td>
                </tr>
              </tbody>
              <tfoot>
                <tr>
                  <td colspan="3" style="text-align: right; font-weight: bold;">TOTAL:</td>
                  <td style="font-weight: bold; font-size: 1.1rem;">${{ totalVenta.toFixed(2) }}</td>
                  <td></td>
                </tr>
              </tfoot>
            </table>
          </div>

          <div class="modal-footer">
            <button type="button" class="btn" @click="closeModal">Cancelar</button>
            <button type="submit" class="btn btn-primary">Crear Venta</button>
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
.badge-completada { background-color: #2ecc71; }
.badge-cancelada { background-color: #e74c3c; }
.badge-pendiente { background-color: #f39c12; }
.badge-iniciada { background-color: #3498db; }
.badge-edicion { background-color: #9b59b6; }

table tfoot tr {
  background-color: #f8f9fa;
}
</style>
