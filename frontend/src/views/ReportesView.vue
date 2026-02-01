<script setup>
import { ref, onMounted } from 'vue'
import { reportesService } from '../services/api'

const activeTab = ref('bajo-stock')
const loading = ref(false)
const message = ref({ text: '', type: '' })

const bajosStock = ref(null)
const ventasDia = ref(null)

const loadBajosStock = async () => {
  try {
    loading.value = true
    const response = await reportesService.productosBajoStock()
    bajosStock.value = response.data.data || null
  } catch (error) {
    showMessage('Error al cargar reporte de bajo stock', 'danger')
  } finally {
    loading.value = false
  }
}

const loadVentasDia = async () => {
  try {
    loading.value = true
    const response = await reportesService.ventasDelDia()
    ventasDia.value = response.data.data || null
  } catch (error) {
    showMessage('Error al cargar reporte de ventas del dia', 'danger')
  } finally {
    loading.value = false
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

const changeTab = (tab) => {
  activeTab.value = tab
  if (tab === 'bajo-stock') loadBajosStock()
  if (tab === 'ventas-dia') loadVentasDia()
}

onMounted(loadBajosStock)
</script>

<template>
  <div>
    <div class="page-header">
      <h1>Reportes</h1>
    </div>

    <div v-if="message.text" :class="['alert', `alert-${message.type}`]">
      {{ message.text }}
    </div>

    <!-- Tabs -->
    <div class="tabs">
      <button :class="['tab', activeTab === 'bajo-stock' ? 'tab-active' : '']" @click="changeTab('bajo-stock')">
        Productos Bajo Stock
      </button>
      <button :class="['tab', activeTab === 'ventas-dia' ? 'tab-active' : '']" @click="changeTab('ventas-dia')">
        Ventas del Dia
      </button>
    </div>

    <!-- Productos Bajo Stock -->
    <div class="card" v-if="activeTab === 'bajo-stock'">
      <div class="card-header">
        <h2 class="card-title">{{ bajosStock?.titulo || 'Productos con Bajo Stock' }}</h2>
        <button class="btn btn-primary" @click="loadBajosStock">Actualizar</button>
      </div>

      <div v-if="loading" class="loading">Cargando...</div>

      <div v-else-if="bajosStock">
        <div class="stats-grid" style="margin-bottom: 15px;">
          <div class="stat-card">
            <h3>{{ bajosStock.total || 0 }}</h3>
            <p>Productos bajo stock</p>
          </div>
        </div>

        <div class="table-container" v-if="bajosStock.productos && bajosStock.productos.length > 0">
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Nombre</th>
                <th>Codigo</th>
                <th>Stock Actual</th>
                <th>Stock Minimo</th>
                <th>Diferencia</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="producto in bajosStock.productos" :key="producto.id">
                <td>{{ producto.id }}</td>
                <td>{{ producto.nombre }}</td>
                <td>{{ producto.codigo }}</td>
                <td>
                  <span class="stock-badge stock-bajo">{{ producto.stock_actual }}</span>
                </td>
                <td>{{ producto.stock_minimo }}</td>
                <td style="color: #e74c3c; font-weight: bold;">{{ producto.diferencia }}</td>
              </tr>
            </tbody>
          </table>
        </div>
        <div v-else style="text-align: center; padding: 30px; color: #2ecc71;">
          Todos los productos tienen stock suficiente
        </div>
      </div>
    </div>

    <!-- Ventas del Dia -->
    <div class="card" v-if="activeTab === 'ventas-dia'">
      <div class="card-header">
        <h2 class="card-title">{{ ventasDia?.titulo || 'Ventas del Dia' }}</h2>
        <button class="btn btn-primary" @click="loadVentasDia">Actualizar</button>
      </div>

      <div v-if="loading" class="loading">Cargando...</div>

      <div v-else-if="ventasDia">
        <div class="stats-grid" style="margin-bottom: 15px;">
          <div class="stat-card">
            <h3>{{ ventasDia.cantidad_ventas || 0 }}</h3>
            <p>Ventas realizadas</p>
          </div>
          <div class="stat-card">
            <h3>${{ ventasDia.total_vendido?.toFixed(2) || '0.00' }}</h3>
            <p>Total vendido</p>
          </div>
        </div>

        <div class="table-container" v-if="ventasDia.ventas && ventasDia.ventas.length > 0">
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Fecha</th>
                <th>Total</th>
                <th>Estado</th>
                <th>Productos</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="venta in ventasDia.ventas" :key="venta.id">
                <td>{{ venta.id }}</td>
                <td>{{ formatDate(venta.fecha) }}</td>
                <td><strong>${{ venta.total?.toFixed(2) }}</strong></td>
                <td>
                  <span :class="venta.estado === 'COMPLETADA' ? 'stock-badge stock-ok' : 'stock-badge stock-bajo'">
                    {{ venta.estado }}
                  </span>
                </td>
                <td>{{ venta.cantidad_productos }}</td>
              </tr>
            </tbody>
          </table>
        </div>
        <div v-else style="text-align: center; padding: 30px; color: #95a5a6;">
          No hay ventas registradas hoy
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.tabs {
  display: flex;
  gap: 0;
  margin-bottom: 20px;
  background-color: #fff;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
.tab {
  flex: 1;
  padding: 12px 20px;
  border: none;
  background-color: #fff;
  cursor: pointer;
  font-size: 0.95rem;
  font-weight: 500;
  color: #95a5a6;
  transition: all 0.3s;
}
.tab:hover {
  background-color: #f8f9fa;
}
.tab-active {
  background-color: #3498db;
  color: white;
}
.stock-badge {
  padding: 3px 8px;
  border-radius: 10px;
  font-weight: 600;
  font-size: 0.85rem;
}
.stock-bajo {
  background-color: #f8d7da;
  color: #721c24;
}
.stock-ok {
  background-color: #d4edda;
  color: #155724;
}
</style>
