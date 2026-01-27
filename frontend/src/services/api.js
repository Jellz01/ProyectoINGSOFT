import axios from 'axios'

const API_URL = 'http://localhost:8000/api'

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Categorias
export const categoriasService = {
  getAll: () => api.get('/categorias/'),
  getById: (id) => api.get(`/categorias/${id}`),
  create: (data) => api.post('/categorias/', data),
  update: (id, data) => api.put(`/categorias/${id}`, data),
  delete: (id) => api.delete(`/categorias/${id}`)
}

// Productos
export const productosService = {
  getAll: () => api.get('/productos/'),
  getById: (id) => api.get(`/productos/${id}`),
  getBajoStock: () => api.get('/productos/bajo-stock'),
  create: (data) => api.post('/productos/', data),
  update: (id, data) => api.put(`/productos/${id}`, data),
  delete: (id) => api.delete(`/productos/${id}`)
}

// Proveedores
export const proveedoresService = {
  getAll: () => api.get('/proveedores/'),
  getById: (id) => api.get(`/proveedores/${id}`),
  create: (data) => api.post('/proveedores/', data),
  update: (id, data) => api.put(`/proveedores/${id}`, data),
  delete: (id) => api.delete(`/proveedores/${id}`)
}

// Clientes
export const clientesService = {
  getAll: () => api.get('/clientes/'),
  getById: (id) => api.get(`/clientes/${id}`),
  create: (data) => api.post('/clientes/', data),
  update: (id, data) => api.put(`/clientes/${id}`, data),
  delete: (id) => api.delete(`/clientes/${id}`)
}

// Usuarios
export const usuariosService = {
  getAll: () => api.get('/usuarios/'),
  getById: (id) => api.get(`/usuarios/${id}`),
  create: (data) => api.post('/usuarios/', data),
  update: (id, data) => api.put(`/usuarios/${id}`, data),
  delete: (id) => api.delete(`/usuarios/${id}`)
}

// Ventas
export const ventasService = {
  getAll: () => api.get('/ventas/'),
  getById: (id) => api.get(`/ventas/${id}`),
  create: (data) => api.post('/ventas/', data),
  cancelar: (id) => api.post(`/ventas/${id}/cancelar`)
}

// Caja
export const cajaService = {
  getAll: () => api.get('/cajas/'),
  getById: (id) => api.get(`/cajas/${id}`),
  getAbierta: () => api.get('/cajas/abierta'),
  abrir: (data) => api.post('/cajas/abrir', data),
  cerrar: (id, data) => api.post(`/cajas/${id}/cerrar`, data),
  registrarMovimiento: (id, data) => api.post(`/cajas/${id}/movimientos`, data)
}

// Reportes
export const reportesService = {
  productosBajoStock: () => api.get('/reportes/productos-bajo-stock'),
  ventasDelDia: () => api.get('/reportes/ventas-del-dia'),
  resumenInventario: () => api.get('/reportes/resumen-inventario')
}

export default api
