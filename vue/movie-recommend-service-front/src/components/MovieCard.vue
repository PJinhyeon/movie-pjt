<template>
  <div>
    <div class="movie-card">
      <!-- movie.poster: /t/p/w500/8UlWHLMpgZm9bx6QYh0NFoq67TZ.jpg -->
      <img :src="'https://image.tmdb.org/t/p/w500' + movie.poster" alt="img" class="movie-image">
    </div>
  </div>
</template>

<script setup>
defineProps({
  movie: Object
})


</script>

<style scoped>
.movie-card {
  border: 1px solid #ccc;
  padding: 10px;
  border-radius: 8px;
  width: 200px;
  height: 300px;
}
.movie-image {
  width: 100%;
}

</style>