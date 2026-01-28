<script setup>
import { ref, onMounted } from 'vue'
import { categoriasService } from '../services/api'

const categorias = ref([])
const loading = ref(true)
const showModal = ref(false)
const editMode = ref(false)
const currentCategoria = ref({ nombre: '', descripcion: '' })
const message = ref({ text: '', type: '' })

const loadCategorias = async () => {
  try {
    loading.value = true
    const response = await categoriasService.getAll()
    categorias.value = response.data.data || []
  } catch (error) {
    showMessage('Error al cargar categorias', 'danger')
  } finally {
    loading.value = false
  }
}

const openCreateModal = () => {
  editMode.value = false
  currentCategoria.value = { nombre: '', descripcion: '' }
  showModal.value = true
}

const openEditModal = (categoria) => {
  editMode.value = true
  currentCategoria.value = { ...categoria }
  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
  currentCategoria.value = { nombre: '', descripcion: '' }
}

const saveCategoria = async () => {
  try {
    if (editMode.value) {
      await categoriasService.update(currentCategoria.value.id, {
        nombre: currentCategoria.value.nombre,
        descripcion: currentCategoria.value.descripcion
      })
      showMessage('Categoria actualizada correctamente', 'success')
    } else {
      await categoriasService.create(currentCategoria.value)
      showMessage('Categoria creada correctamente', 'success')
    }
    closeModal()
    loadCategorias()
  } catch (error) {
    showMessage('Error al guardar categoria', 'danger')
  }
}

const deleteCategoria = async (id) => {
  if (confirm('Esta seguro de eliminar esta categoria?')) {
    try {
      await categoriasService.delete(id)
      showMessage('Categoria eliminada correctamente', 'success')
      loadCategorias()
    } catch (error) {
      showMessage('Error al eliminar categoria', 'danger')
    }
  }
}

const showMessage = (text, type) => {
  message.value = { text, type }
  setTimeout(() => {
    message.value = { text: '', type: '' }
  }, 3000)
}

onMounted(loadCategorias)
</script>

<template>
  <div>
    <div class="page-header">
      <h1>Categorias</h1>
    </div>

    <div v-if="message.text" :class="['alert', `alert-${message.type}`]">
      {{ message.text }}
    </div>

    <div class="card">
      <div class="card-header">
        <h2 class="card-title">Lista de Categorias</h2>
        <button class="btn btn-primary" @click="openCreateModal">Nueva Categoria</button>
      </div>

      <div v-if="loading" class="loading">Cargando...</div>

      <div v-else class="table-container">
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Nombre</th>
              <th>Descripcion</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="categoria in categorias" :key="categoria.id">
              <td>{{ categoria.id }}</td>
              <td>{{ categoria.nombre }}</td>
              <td>{{ categoria.descripcion || '-' }}</td>
              <td class="actions">
                <button class="btn btn-warning btn-sm" @click="openEditModal(categoria)">Editar</button>
                <button class="btn btn-danger btn-sm" @click="deleteCategoria(categoria.id)">Eliminar</button>
              </td>
            </tr>
            <tr v-if="categorias.length === 0">
              <td colspan="4" style="text-align: center;">No hay categorias registradas</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Modal -->
    <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal">
        <div class="modal-header">
          <h3>{{ editMode ? 'Editar Categoria' : 'Nueva Categoria' }}</h3>
          <button class="modal-close" @click="closeModal">&times;</button>
        </div>
        <form @submit.prevent="saveCategoria">
          <div class="form-group">
            <label>Nombre</label>
            <input type="text" class="form-control" v-model="currentCategoria.nombre" required>
          </div>
          <div class="form-group">
            <label>Descripcion</label>
            <textarea class="form-control" v-model="currentCategoria.descripcion" rows="3"></textarea>
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
