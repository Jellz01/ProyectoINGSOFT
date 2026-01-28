<script setup>
import { ref, onMounted } from 'vue'
import { reportesService, productosService, clientesService } from '../services/api'

const stats = ref({
  totalProductos: 0,
  valorInventario: 0,
  productosBajoStock: 0,
  totalClientes: 0
})
const loading = ref(true)

onMounted(async () => {
  try {
    const [inventarioRes, clientesRes] = await Promise.all([
      reportesService.resumenInventario(),
      clientesService.getAll()
    ])

    stats.value = {
      totalProductos: inventarioRes.data.total_productos || 0,
      valorInventario: inventarioRes.data.valor_total_inventario || 0,
      productosBajoStock: inventarioRes.data.productos_bajo_stock || 0,
      totalClientes: clientesRes.data.data?.length || 0
    }
  } catch (error) {
    console.error('Error loading stats:', error)
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div>
    <div class="page-header">
      <h1>Dashboard - MiTienda</h1>
    </div>

    <div v-if="loading" class="loading">
      Cargando estadisticas...
    </div>

    <div v-else class="stats-grid">
      <div class="stat-card">
        <h3>{{ stats.totalProductos }}</h3>
        <p>Total Productos</p>
      </div>
      <div class="stat-card">
        <h3>${{ stats.valorInventario.toFixed(2) }}</h3>
        <p>Valor del Inventario</p>
      </div>
      <div class="stat-card">
        <h3>{{ stats.productosBajoStock }}</h3>
        <p>Productos Bajo Stock</p>
      </div>
      <div class="stat-card">
        <h3>{{ stats.totalClientes }}</h3>
        <p>Total Clientes</p>
      </div>
    </div>

    <div class="card">
      <div class="card-header">
        <h2 class="card-title">Bienvenido al Sistema de Gestion</h2>
      </div>
      <p>Utilice el menu lateral para navegar entre los diferentes modulos del sistema:</p>
      <ul style="margin-top: 15px; margin-left: 20px;">
        <li><strong>Categorias:</strong> Gestionar categorias de productos</li>
        <li><strong>Productos:</strong> Administrar inventario de productos</li>
        <li><strong>Proveedores:</strong> Gestionar proveedores</li>
        <li><strong>Clientes:</strong> Administrar clientes</li>
        <li><strong>Usuarios:</strong> Gestionar usuarios del sistema</li>
        <li><strong>Ventas:</strong> Realizar y consultar ventas</li>
        <li><strong>Caja:</strong> Control de caja</li>
        <li><strong>Reportes:</strong> Ver reportes del sistema</li>
      </ul>
    </div>
  </div>
</template>
