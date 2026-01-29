<script setup>
import { ref, onMounted } from 'vue'
import { usuariosService } from '../services/api'

const usuarios = ref([])
const loading = ref(true)
const showModal = ref(false)
const editMode = ref(false)
const currentUsuario = ref({
  nombre: '', usuario: '', password: '', rol: 'CAJERO', estado: 'ACTIVO'
})
const message = ref({ text: '', type: '' })

const roles = ['ADMINISTRADOR', 'CAJERO', 'INVENTARIO']
const estados = ['ACTIVO', 'INACTIVO']

const loadUsuarios = async () => {
  try {
    loading.value = true
    const response = await usuariosService.getAll()
    usuarios.value = response.data.data || []
  } catch (error) {
    showMessage('Error al cargar usuarios', 'danger')
  } finally {
    loading.value = false
  }
}

const openCreateModal = () => {
  editMode.value = false
  currentUsuario.value = { nombre: '', usuario: '', password: '', rol: 'CAJERO', estado: 'ACTIVO' }
  showModal.value = true
}

const openEditModal = (usuario) => {
  editMode.value = true
  currentUsuario.value = { ...usuario, password: '' }
  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
}

const saveUsuario = async () => {
  try {
    if (editMode.value) {
      const data = {
        nombre: currentUsuario.value.nombre,
        rol: currentUsuario.value.rol,
        estado: currentUsuario.value.estado
      }
      if (currentUsuario.value.password) {
        data.password = currentUsuario.value.password
      }
      await usuariosService.update(currentUsuario.value.id, data)
      showMessage('Usuario actualizado correctamente', 'success')
    } else {
      await usuariosService.create(currentUsuario.value)
      showMessage('Usuario creado correctamente', 'success')
    }
    closeModal()
    loadUsuarios()
  } catch (error) {
    showMessage('Error al guardar usuario', 'danger')
  }
}

const deleteUsuario = async (id) => {
  if (confirm('Esta seguro de eliminar este usuario?')) {
    try {
      await usuariosService.delete(id)
      showMessage('Usuario eliminado correctamente', 'success')
      loadUsuarios()
    } catch (error) {
      showMessage('Error al eliminar usuario', 'danger')
    }
  }
}

const showMessage = (text, type) => {
  message.value = { text, type }
  setTimeout(() => { message.value = { text: '', type: '' } }, 3000)
}

const getRolBadgeClass = (rol) => {
  const classes = {
    'ADMINISTRADOR': 'badge badge-admin',
    'CAJERO': 'badge badge-cajero',
    'INVENTARIO': 'badge badge-inventario'
  }
  return classes[rol] || 'badge'
}

onMounted(loadUsuarios)
</script>

<template>
  <div>
    <div class="page-header">
      <h1>Usuarios</h1>
    </div>

    <div v-if="message.text" :class="['alert', `alert-${message.type}`]">
      {{ message.text }}
    </div>

    <div class="card">
      <div class="card-header">
        <h2 class="card-title">Lista de Usuarios</h2>
        <button class="btn btn-primary" @click="openCreateModal">Nuevo Usuario</button>
      </div>

      <div v-if="loading" class="loading">Cargando...</div>

      <div v-else class="table-container">
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Nombre</th>
              <th>Usuario</th>
              <th>Rol</th>
              <th>Estado</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="usuario in usuarios" :key="usuario.id">
              <td>{{ usuario.id }}</td>
              <td>{{ usuario.nombre }}</td>
              <td>{{ usuario.usuario }}</td>
              <td><span :class="getRolBadgeClass(usuario.rol)">{{ usuario.rol }}</span></td>
              <td>
                <span :class="usuario.estado === 'ACTIVO' ? 'badge badge-activo' : 'badge badge-inactivo'">
                  {{ usuario.estado }}
                </span>
              </td>
              <td class="actions">
                <button class="btn btn-warning btn-sm" @click="openEditModal(usuario)">Editar</button>
                <button class="btn btn-danger btn-sm" @click="deleteUsuario(usuario.id)">Eliminar</button>
              </td>
            </tr>
            <tr v-if="usuarios.length === 0">
              <td colspan="6" style="text-align: center;">No hay usuarios registrados</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Modal -->
    <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal">
        <div class="modal-header">
          <h3>{{ editMode ? 'Editar Usuario' : 'Nuevo Usuario' }}</h3>
          <button class="modal-close" @click="closeModal">&times;</button>
        </div>
        <form @submit.prevent="saveUsuario">
          <div class="form-group">
            <label>Nombre completo</label>
            <input type="text" class="form-control" v-model="currentUsuario.nombre" required>
          </div>
          <div class="form-group">
            <label>Usuario</label>
            <input type="text" class="form-control" v-model="currentUsuario.usuario" required :disabled="editMode">
          </div>
          <div class="form-group">
            <label>{{ editMode ? 'Nueva contrasena (dejar vacio para no cambiar)' : 'Contrasena' }}</label>
            <input type="password" class="form-control" v-model="currentUsuario.password" :required="!editMode">
          </div>
          <div class="grid-2">
            <div class="form-group">
              <label>Rol</label>
              <select class="form-control" v-model="currentUsuario.rol" required>
                <option v-for="rol in roles" :key="rol" :value="rol">{{ rol }}</option>
              </select>
            </div>
            <div class="form-group" v-if="editMode">
              <label>Estado</label>
              <select class="form-control" v-model="currentUsuario.estado">
                <option v-for="estado in estados" :key="estado" :value="estado">{{ estado }}</option>
              </select>
            </div>
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

<style scoped>
.badge {
  padding: 4px 10px;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 600;
  color: white;
}
.badge-admin { background-color: #e74c3c; }
.badge-cajero { background-color: #3498db; }
.badge-inventario { background-color: #f39c12; }
.badge-activo { background-color: #2ecc71; }
.badge-inactivo { background-color: #95a5a6; }
</style>
