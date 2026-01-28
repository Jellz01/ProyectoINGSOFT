<script setup>
import { ref, onMounted } from 'vue'
import { productosService, categoriasService, proveedoresService } from '../services/api'

const productos = ref([])
const categorias = ref([])
const proveedores = ref([])
const loading = ref(true)
const showModal = ref(false)
const editMode = ref(false)
const currentProducto = ref({
  nombre: '', codigo: '', precio_compra: 0, precio_venta: 0,
  stock: 0, stock_minimo: 5, categoria_id: null, proveedor_id: null
})
const message = ref({ text: '', type: '' })

const loadProductos = async () => {
  try {
    loading.value = true
    const response = await productosService.getAll()
    productos.value = response.data.data || []
  } catch (error) {
    showMessage('Error al cargar productos', 'danger')
  } finally {
    loading.value = false
  }
}

const loadCategorias = async () => {
  try {
    const response = await categoriasService.getAll()
    categorias.value = response.data.data || []
  } catch (error) {
    console.error('Error loading categorias')
  }
}

const loadProveedores = async () => {
  try {
    const response = await proveedoresService.getAll()
    proveedores.value = response.data.data || []
  } catch (error) {
    console.error('Error loading proveedores')
  }
}

const openCreateModal = () => {
  editMode.value = false
  currentProducto.value = {
    nombre: '', codigo: '', precio_compra: 0, precio_venta: 0,
    stock: 0, stock_minimo: 5, categoria_id: null, proveedor_id: null
  }
  showModal.value = true
}

const openEditModal = (producto) => {
  editMode.value = true
  currentProducto.value = { ...producto }
  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
}

const saveProducto = async () => {
  try {
    const data = {
      nombre: currentProducto.value.nombre,
      codigo: currentProducto.value.codigo,
      precio_compra: parseFloat(currentProducto.value.precio_compra),
      precio_venta: parseFloat(currentProducto.value.precio_venta),
      stock: parseInt(currentProducto.value.stock),
      stock_minimo: parseInt(currentProducto.value.stock_minimo),
      categoria_id: currentProducto.value.categoria_id || null,
      proveedor_id: currentProducto.value.proveedor_id || null
    }

    if (editMode.value) {
      await productosService.update(currentProducto.value.id, data)
      showMessage('Producto actualizado correctamente', 'success')
    } else {
      await productosService.create(data)
      showMessage('Producto creado correctamente', 'success')
    }
    closeModal()
    loadProductos()
  } catch (error) {
    showMessage('Error al guardar producto', 'danger')
  }
}

const deleteProducto = async (id) => {
  if (confirm('Esta seguro de eliminar este producto?')) {
    try {
      await productosService.delete(id)
      showMessage('Producto eliminado correctamente', 'success')
      loadProductos()
    } catch (error) {
      showMessage('Error al eliminar producto', 'danger')
    }
  }
}

const showMessage = (text, type) => {
  message.value = { text, type }
  setTimeout(() => { message.value = { text: '', type: '' } }, 3000)
}

const getCategoriaNombre = (id) => {
  const cat = categorias.value.find(c => c.id === id)
  return cat ? cat.nombre : '-'
}

onMounted(() => {
  loadProductos()
  loadCategorias()
  loadProveedores()
})
</script>

<template>
  <div>
    <div class="page-header">
      <h1>Productos</h1>
    </div>

    <div v-if="message.text" :class="['alert', `alert-${message.type}`]">
      {{ message.text }}
    </div>

    <div class="card">
      <div class="card-header">
        <h2 class="card-title">Lista de Productos</h2>
        <button class="btn btn-primary" @click="openCreateModal">Nuevo Producto</button>
      </div>

      <div v-if="loading" class="loading">Cargando...</div>

      <div v-else class="table-container">
        <table>
          <thead>
            <tr>
              <th>Codigo</th>
              <th>Nombre</th>
              <th>Categoria</th>
              <th>P. Compra</th>
              <th>P. Venta</th>
              <th>Stock</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="producto in productos" :key="producto.id"
                :class="{ 'alert-warning': producto.stock <= producto.stock_minimo }">
              <td>{{ producto.codigo }}</td>
              <td>{{ producto.nombre }}</td>
              <td>{{ getCategoriaNombre(producto.categoria_id) }}</td>
              <td>${{ producto.precio_compra.toFixed(2) }}</td>
              <td>${{ producto.precio_venta.toFixed(2) }}</td>
              <td>{{ producto.stock }}</td>
              <td class="actions">
                <button class="btn btn-warning btn-sm" @click="openEditModal(producto)">Editar</button>
                <button class="btn btn-danger btn-sm" @click="deleteProducto(producto.id)">Eliminar</button>
              </td>
            </tr>
            <tr v-if="productos.length === 0">
              <td colspan="7" style="text-align: center;">No hay productos registrados</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Modal -->
    <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal">
        <div class="modal-header">
          <h3>{{ editMode ? 'Editar Producto' : 'Nuevo Producto' }}</h3>
          <button class="modal-close" @click="closeModal">&times;</button>
        </div>
        <form @submit.prevent="saveProducto">
          <div class="grid-2">
            <div class="form-group">
              <label>Nombre</label>
              <input type="text" class="form-control" v-model="currentProducto.nombre" required>
            </div>
            <div class="form-group">
              <label>Codigo</label>
              <input type="text" class="form-control" v-model="currentProducto.codigo" required :disabled="editMode">
            </div>
          </div>
          <div class="grid-2">
            <div class="form-group">
              <label>Precio Compra</label>
              <input type="number" step="0.01" class="form-control" v-model="currentProducto.precio_compra" required>
            </div>
            <div class="form-group">
              <label>Precio Venta</label>
              <input type="number" step="0.01" class="form-control" v-model="currentProducto.precio_venta" required>
            </div>
          </div>
          <div class="grid-2">
            <div class="form-group">
              <label>Stock</label>
              <input type="number" class="form-control" v-model="currentProducto.stock" required>
            </div>
            <div class="form-group">
              <label>Stock Minimo</label>
              <input type="number" class="form-control" v-model="currentProducto.stock_minimo" required>
            </div>
          </div>
          <div class="grid-2">
            <div class="form-group">
              <label>Categoria</label>
              <select class="form-control" v-model="currentProducto.categoria_id">
                <option :value="null">Sin categoria</option>
                <option v-for="cat in categorias" :key="cat.id" :value="cat.id">{{ cat.nombre }}</option>
              </select>
            </div>
            <div class="form-group">
              <label>Proveedor</label>
              <select class="form-control" v-model="currentProducto.proveedor_id">
                <option :value="null">Sin proveedor</option>
                <option v-for="prov in proveedores" :key="prov.id" :value="prov.id">{{ prov.nombre }}</option>
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
