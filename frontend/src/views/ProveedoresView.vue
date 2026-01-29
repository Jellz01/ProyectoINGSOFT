<script setup>
import { ref, onMounted } from 'vue'
import { proveedoresService } from '../services/api'

const proveedores = ref([])
const loading = ref(true)
const showModal = ref(false)
const editMode = ref(false)
const currentProveedor = ref({
  nombre: '', ruc: '', telefono: '', email: '', direccion: ''
})
const message = ref({ text: '', type: '' })

const loadProveedores = async () => {
  try {
    loading.value = true
    const response = await proveedoresService.getAll()
    proveedores.value = response.data.data || []
  } catch (error) {
    showMessage('Error al cargar proveedores', 'danger')
  } finally {
    loading.value = false
  }
}

const openCreateModal = () => {
  editMode.value = false
  currentProveedor.value = { nombre: '', ruc: '', telefono: '', email: '', direccion: '' }
  showModal.value = true
}

const openEditModal = (proveedor) => {
  editMode.value = true
  currentProveedor.value = { ...proveedor }
  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
}

const saveProveedor = async () => {
  try {
    if (editMode.value) {
      await proveedoresService.update(currentProveedor.value.id, {
        nombre: currentProveedor.value.nombre,
        telefono: currentProveedor.value.telefono,
        email: currentProveedor.value.email,
        direccion: currentProveedor.value.direccion
      })
      showMessage('Proveedor actualizado correctamente', 'success')
    } else {
      await proveedoresService.create(currentProveedor.value)
      showMessage('Proveedor creado correctamente', 'success')
    }
    closeModal()
    loadProveedores()
  } catch (error) {
    showMessage('Error al guardar proveedor', 'danger')
  }
}

const deleteProveedor = async (id) => {
  if (confirm('Esta seguro de eliminar este proveedor?')) {
    try {
      await proveedoresService.delete(id)
      showMessage('Proveedor eliminado correctamente', 'success')
      loadProveedores()
    } catch (error) {
      showMessage('Error al eliminar proveedor', 'danger')
    }
  }
}

const showMessage = (text, type) => {
  message.value = { text, type }
  setTimeout(() => { message.value = { text: '', type: '' } }, 3000)
}

onMounted(loadProveedores)
</script>

<template>
  <div>
    <div class="page-header">
      <h1>Proveedores</h1>
    </div>

    <div v-if="message.text" :class="['alert', `alert-${message.type}`]">
      {{ message.text }}
    </div>

    <div class="card">
      <div class="card-header">
        <h2 class="card-title">Lista de Proveedores</h2>
        <button class="btn btn-primary" @click="openCreateModal">Nuevo Proveedor</button>
      </div>

      <div v-if="loading" class="loading">Cargando...</div>

      <div v-else class="table-container">
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Nombre</th>
              <th>RUC</th>
              <th>Telefono</th>
              <th>Email</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="proveedor in proveedores" :key="proveedor.id">
              <td>{{ proveedor.id }}</td>
              <td>{{ proveedor.nombre }}</td>
              <td>{{ proveedor.ruc }}</td>
              <td>{{ proveedor.telefono || '-' }}</td>
              <td>{{ proveedor.email || '-' }}</td>
              <td class="actions">
                <button class="btn btn-warning btn-sm" @click="openEditModal(proveedor)">Editar</button>
                <button class="btn btn-danger btn-sm" @click="deleteProveedor(proveedor.id)">Eliminar</button>
              </td>
            </tr>
            <tr v-if="proveedores.length === 0">
              <td colspan="6" style="text-align: center;">No hay proveedores registrados</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Modal -->
    <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal">
        <div class="modal-header">
          <h3>{{ editMode ? 'Editar Proveedor' : 'Nuevo Proveedor' }}</h3>
          <button class="modal-close" @click="closeModal">&times;</button>
        </div>
        <form @submit.prevent="saveProveedor">
          <div class="form-group">
            <label>Nombre</label>
            <input type="text" class="form-control" v-model="currentProveedor.nombre" required>
          </div>
          <div class="form-group">
            <label>RUC</label>
            <input type="text" class="form-control" v-model="currentProveedor.ruc" required :disabled="editMode">
          </div>
          <div class="grid-2">
            <div class="form-group">
              <label>Telefono</label>
              <input type="text" class="form-control" v-model="currentProveedor.telefono">
            </div>
            <div class="form-group">
              <label>Email</label>
              <input type="email" class="form-control" v-model="currentProveedor.email">
            </div>
          </div>
          <div class="form-group">
            <label>Direccion</label>
            <textarea class="form-control" v-model="currentProveedor.direccion" rows="2"></textarea>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn" @click="closeModal">Cancelar</button>
            <button type="submit" class="btn btn-primary">Guardar</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>
