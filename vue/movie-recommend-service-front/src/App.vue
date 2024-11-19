
<template>
  <div>
    <AppNavbar/>
  </div>
<RouterView/>
</template>

<script setup>
import { RouterLink, RouterView } from 'vue-router'
import AppNavbar from '@/components/Common/AppNavbar.vue'
</script>

<style scoped>

</style>
