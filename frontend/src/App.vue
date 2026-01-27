<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <aside class="sidebar">
    <div class="sidebar-header">
      <h2>MiTienda</h2>
      <small>Sistema de Gestion</small>
    </div>
    <nav>
      <ul>
        <li><RouterLink to="/">Inicio</RouterLink></li>
        <li><RouterLink to="/categorias">Categorias</RouterLink></li>
        <li><RouterLink to="/productos">Productos</RouterLink></li>
        <li><RouterLink to="/proveedores">Proveedores</RouterLink></li>
        <li><RouterLink to="/clientes">Clientes</RouterLink></li>
        <li><RouterLink to="/usuarios">Usuarios</RouterLink></li>
        <li><RouterLink to="/ventas">Ventas</RouterLink></li>
        <li><RouterLink to="/caja">Caja</RouterLink></li>
        <li><RouterLink to="/reportes">Reportes</RouterLink></li>
      </ul>
    </nav>
  </aside>
  <main class="main-content">
    <RouterView />
  </main>
</template>
