<template>
  <div class="movie-card">
    <img 
      :src="'https://image.tmdb.org/t/p/w500' + movie.poster_path" 
      alt="movie poster" 
      class="movie-image" 
    />
  </div>
</template>

<script setup>
defineProps({
  movie: Object
})
</script>

<style scoped>
.movie-card {
  width: 200px; /* 고정된 카드 너비 */
  height: 300px; /* 고정된 카드 높이 */
  overflow: hidden; /* 이미지 넘침 방지 */
  display: flex;
  justify-content: center;
  align-items: center;
}
.movie-image {
  width: 100%; /* 카드에 맞게 이미지 크기 조정 */
  height: 100%; /* 카드 높이에 맞게 이미지 조정 */
  object-fit: cover; /* 이미지 비율 유지하며 채우기 */
}
</style>
