<template>
  <div>
    <p>MovieCard-movietitle</p>
    <div>
      <img :src="movie.poster" alt="" style="width: 200px; height: 350px;">
    </div>
  </div>
</template>

<script setup>
import { defineProps } from 'vue';

defineProps({
  movie: Object
})


</script>

<style scoped>

</style>