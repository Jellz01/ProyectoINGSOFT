<script setup>
import { ref, onMounted } from 'vue'
import { clientesService } from '../services/api'

const clientes = ref([])
const loading = ref(true)
const showModal = ref(false)
const editMode = ref(false)
const currentCliente = ref({
  nombre: '', cedula: '', telefono: '', email: '', direccion: ''
})
const message = ref({ text: '', type: '' })

const loadClientes = async () => {
  try {
    loading.value = true
    const response = await clientesService.getAll()
    clientes.value = response.data.data || []
  } catch (error) {
    showMessage('Error al cargar clientes', 'danger')
  } finally {
    loading.value = false
  }
}

const openCreateModal = () => {
  editMode.value = false
  currentCliente.value = { nombre: '', cedula: '', telefono: '', email: '', direccion: '' }
  showModal.value = true
}

const openEditModal = (cliente) => {
  editMode.value = true
  currentCliente.value = { ...cliente }
  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
}

const saveCliente = async () => {
  try {
    if (editMode.value) {
      await clientesService.update(currentCliente.value.id, {
        nombre: currentCliente.value.nombre,
        telefono: currentCliente.value.telefono,
        email: currentCliente.value.email,
        direccion: currentCliente.value.direccion
      })
      showMessage('Cliente actualizado correctamente', 'success')
    } else {
      await clientesService.create(currentCliente.value)
      showMessage('Cliente creado correctamente', 'success')
    }
    closeModal()
    loadClientes()
  } catch (error) {
    showMessage('Error al guardar cliente', 'danger')
  }
}

const deleteCliente = async (id) => {
  if (confirm('Esta seguro de eliminar este cliente?')) {
    try {
      await clientesService.delete(id)
      showMessage('Cliente eliminado correctamente', 'success')
      loadClientes()
    } catch (error) {
      showMessage('Error al eliminar cliente', 'danger')
    }
  }
}

const showMessage = (text, type) => {
  message.value = { text, type }
  setTimeout(() => { message.value = { text: '', type: '' } }, 3000)
}

onMounted(loadClientes)
</script>

<template>
  <div>
    <div class="page-header">
      <h1>Clientes</h1>
    </div>

    <div v-if="message.text" :class="['alert', `alert-${message.type}`]">
      {{ message.text }}
    </div>

    <div class="card">
      <div class="card-header">
        <h2 class="card-title">Lista de Clientes</h2>
        <button class="btn btn-primary" @click="openCreateModal">Nuevo Cliente</button>
      </div>

      <div v-if="loading" class="loading">Cargando...</div>

      <div v-else class="table-container">
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Nombre</th>
              <th>Cedula</th>
              <th>Telefono</th>
              <th>Email</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="cliente in clientes" :key="cliente.id">
              <td>{{ cliente.id }}</td>
              <td>{{ cliente.nombre }}</td>
              <td>{{ cliente.cedula }}</td>
              <td>{{ cliente.telefono || '-' }}</td>
              <td>{{ cliente.email || '-' }}</td>
              <td class="actions">
                <button class="btn btn-warning btn-sm" @click="openEditModal(cliente)">Editar</button>
                <button class="btn btn-danger btn-sm" @click="deleteCliente(cliente.id)">Eliminar</button>
              </td>
            </tr>
            <tr v-if="clientes.length === 0">
              <td colspan="6" style="text-align: center;">No hay clientes registrados</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Modal -->
    <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal">
        <div class="modal-header">
          <h3>{{ editMode ? 'Editar Cliente' : 'Nuevo Cliente' }}</h3>
          <button class="modal-close" @click="closeModal">&times;</button>
        </div>
        <form @submit.prevent="saveCliente">
          <div class="form-group">
            <label>Nombre</label>
            <input type="text" class="form-control" v-model="currentCliente.nombre" required>
          </div>
          <div class="form-group">
            <label>Cedula</label>
            <input type="text" class="form-control" v-model="currentCliente.cedula" required :disabled="editMode">
          </div>
          <div class="grid-2">
            <div class="form-group">
              <label>Telefono</label>
              <input type="text" class="form-control" v-model="currentCliente.telefono">
            </div>
            <div class="form-group">
              <label>Email</label>
              <input type="email" class="form-control" v-model="currentCliente.email">
            </div>
          </div>
          <div class="form-group">
            <label>Direccion</label>
            <textarea class="form-control" v-model="currentCliente.direccion" rows="2"></textarea>
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
