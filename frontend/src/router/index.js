import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/HomeView.vue')
  },
  {
    path: '/categorias',
    name: 'Categorias',
    component: () => import('../views/CategoriasView.vue')
  },
  {
    path: '/productos',
    name: 'Productos',
    component: () => import('../views/ProductosView.vue')
  },
  {
    path: '/proveedores',
    name: 'Proveedores',
    component: () => import('../views/ProveedoresView.vue')
  },
  {
    path: '/clientes',
    name: 'Clientes',
    component: () => import('../views/ClientesView.vue')
  },
  {
    path: '/usuarios',
    name: 'Usuarios',
    component: () => import('../views/UsuariosView.vue')
  },
  {
    path: '/ventas',
    name: 'Ventas',
    component: () => import('../views/VentasView.vue')
  },
  {
    path: '/caja',
    name: 'Caja',
    component: () => import('../views/CajaView.vue')
  },
  {
    path: '/reportes',
    name: 'Reportes',
    component: () => import('../views/ReportesView.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
