
<template>
  <header>
    <AppNavbar/>
  </header>

  <RouterView/>
</template>

<script setup>
import { RouterView } from 'vue-router'
import AppNavbar from '@/components/Common/AppNavbar.vue'
</script>

<style scoped>

</style>
