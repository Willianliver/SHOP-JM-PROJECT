<template>
  <div class="card">
    <h1>Bem-vindo ao Vue 🚀</h1>
    <p>{{ message }}</p>
    <button @click="count++">Cliquei {{ count }} vezes</button>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const count = ref(0)
const message = 'Frontend conectado ao Django Backend!'
</script>

<style scoped>
.card {
  padding: 2rem;
  border: 1px solid #ccc;
  border-radius: 10px;
}
</style>
